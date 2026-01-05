from uuid import UUID

from app.application.commands import (
    AddChatMessageCommand,
    AnswerStepCommand,
)
from app.application.exceptions import InvalidWorkflowOperation, WorkflowNotFound
from app.application.registry import WorkflowDomain
from app.domain.chat import ChatMessage, ChatRole
from app.domain.streaming import StreamSink
from app.domain.workflow import (
    ChatMutationResult,
    WaitingReason,
    Workflow,
    WorkflowContext,
    WorkflowCreate,
    WorkflowPhase,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

#  ------------- Behavior / Use Cases ----------------
#
# COLLECTING
# - steps allowed
# - chat_history ignored
# SOLVING
# - no new steps
# - solution generated
# DISCUSSION
# - chat_history active
# - no new steps
# - solution immutable (for now)
# DONE
# - immutable, final state
# - set when solution shown and no chat service is set


class WorkflowService:
    def __init__(self, repo: WorkflowRepository, domain: WorkflowDomain):
        self.repo = repo
        self.domain = domain

    def _build_context(self, wf: Workflow) -> WorkflowContext:
        return WorkflowContext(
            workflow_id=wf.id,
            domain_type=wf.domain_type,
            ticket=wf.ticket,
            steps=wf.state.steps,
            last_decision=wf.state.last_decision,
            solution=wf.state.solution,
            chat_history=wf.state.chat_history,
            skipped=wf.state.skipped,
            max_steps=wf.max_steps,
            phase=wf.state.phase,
        )

    # ------- Engine loop --------

    def _process_workflow(self, workflow: Workflow, stream: StreamSink | None = None) -> Workflow:
        # Clear phase-local outcomes
        state = workflow.state
        state.last_decision = None
        state.discussion_result = None

        # hard stop
        if state.phase == WorkflowPhase.DONE:
            return workflow

        # process COLLECTING phase
        if state.phase == WorkflowPhase.COLLECTING:
            if state.skipped or len(state.steps) >= workflow.max_steps:
                # move to SOLVING phase if max steps reached
                state.phase = WorkflowPhase.SOLVING
                return workflow

            ctx = self._build_context(workflow)
            decision = self.domain.step_generator.propose_next(ctx)

            state.last_decision = decision
            if decision.next_step:
                state.steps.append(decision.next_step)
                return workflow

            state.phase = WorkflowPhase.SOLVING
            return workflow

        # process SOLVING phase
        if state.phase == WorkflowPhase.SOLVING:
            ctx = self._build_context(workflow)
            state.solution = self.domain.solution_service.generate_solution(ctx, stream)
            state.phase = WorkflowPhase.DISCUSSION if self.domain.chat_service else WorkflowPhase.DONE
            return workflow

        # process DISCUSSION phase
        if state.phase == WorkflowPhase.DISCUSSION:
            discussion_result = ChatMutationResult(solution_updated=False)
            if self.domain.chat_service and state.chat_history.messages:
                last_msg = state.chat_history.messages[-1]
                if last_msg.role == ChatRole.USER:
                    ctx = self._build_context(workflow)
                    reply = self.domain.chat_service.reply(ctx, last_msg)
                    state.chat_history.add_message(reply.message)
                    if reply.requires_solution_update:
                        ctx = self._build_context(workflow)
                        state.solution = self.domain.solution_service.generate_solution(ctx)
                        discussion_result = ChatMutationResult(solution_updated=True)
            state.discussion_result = discussion_result
            return workflow

        return workflow

    def _process_until_waiting_or_done(self, workflow: Workflow, stream: StreamSink | None = None) -> Workflow:
        while not self._is_waiting_for_user(workflow) and workflow.state.phase != WorkflowPhase.DONE:
            workflow = self._process_workflow(workflow, stream)
        return workflow

    def _has_open_step(self, workflow: Workflow) -> bool:
        return any(step.answer is None for step in workflow.state.steps)

    def _is_waiting_for_chat_input(self, workflow: Workflow) -> bool:
        if not self.domain.chat_service:
            return False
        if not workflow.state.chat_history.messages:
            return True
        last_msg = workflow.state.chat_history.messages[-1]
        return last_msg.role != ChatRole.USER

    def get_waiting_reason(self, workflow: Workflow) -> WaitingReason | None:
        state = workflow.state
        if state.phase == WorkflowPhase.COLLECTING and state.skipped:
            return None
        if state.phase == WorkflowPhase.COLLECTING and self._has_open_step(workflow):
            return WaitingReason.ANSWER_NEEDED
        if state.phase == WorkflowPhase.DISCUSSION and self._is_waiting_for_chat_input(workflow):
            return WaitingReason.CHAT
        return None

    def get_workflow_confidence(self, workflow: Workflow) -> float | None:
        state = workflow.state
        if state.last_decision:
            return state.last_decision.workflow_confidence
        return None

    def _is_waiting_for_user(self, workflow: Workflow) -> bool:
        return self.get_waiting_reason(workflow) is not None

    # ------- Commands with processing --------

    def answer_step(self, workflow_id: UUID, cmd: AnswerStepCommand, stream: StreamSink | None = None) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        state = workflow.state

        if state.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation("Answers can only be added in COLLECTING phase")

        step = next(
            (s for s in state.steps if s.id == cmd.step_id),
            None,
        )

        if step is None:
            raise InvalidWorkflowOperation("Step not found")

        if step.answer is not None:
            raise InvalidWorkflowOperation("Step already answered")

        step.answer = cmd.answer

        # domain-specific interpretation hook
        if self.domain.answer_parser:
            self.domain.answer_parser.parse_answer(step)

        workflow = self._process_until_waiting_or_done(workflow, stream)
        return self.repo.save(workflow)

    def skip_to_solution(self, workflow_id: UUID, stream: StreamSink | None = None) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        state = workflow.state

        if state.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation("Can only skip to solution in COLLECTING phase")

        state.skipped = True

        workflow = self._process_until_waiting_or_done(workflow, stream)
        return self.repo.save(workflow)

    # ------- Creation --------

    def create(self, workflow_create: WorkflowCreate) -> Workflow:
        workflow = self.repo.create(workflow_create)

        workflow = self._process_until_waiting_or_done(workflow)
        return self.repo.save(workflow)

    # -------- Queries --------

    def get_workflow(self, workflow_id: UUID) -> Workflow:
        workflow = self.repo.get(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow {workflow_id} not found")
        return workflow

    def list_workflows(self) -> list[Workflow]:
        return self.repo.list()

    def add_chat_message(
        self,
        workflow_id: UUID,
        cmd: AddChatMessageCommand,
    ) -> Workflow:
        workflow = self.get_workflow(workflow_id)

        if not cmd.content.strip():
            raise InvalidWorkflowOperation("Chat message content cannot be empty")

        user_message = ChatMessage(
            role=cmd.role,
            content=cmd.content,
        )

        workflow.state.chat_history.add_message(user_message)

        workflow = self._process_until_waiting_or_done(workflow)
        return self.repo.save(workflow)
