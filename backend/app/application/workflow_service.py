from uuid import UUID

from app.application.commands import (
    AddChatMessageCommand,
    AnswerStepCommand,
)
from app.application.exceptions import InvalidWorkflowOperation, WorkflowNotFound
from app.application.registry import WorkflowDomain
from app.application.workflow_utils import is_waiting_for_user
from app.domain.chat import ChatMessage, ChatRole
from app.domain.event import (
    ChatRepliedEventData,
    ClarificationUpdatedEventData,
    SolutionGeneratedEventData,
    SolutionGeneratedReason,
    WorkflowBranchedEventData,
    WorkflowCreatedEventData,
    WorkflowEventCreate,
    WorkflowEventType,
)
from app.domain.streaming import StreamSink
from app.domain.workflow import (
    ChatMutationResult,
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

    @staticmethod
    def _build_context(wf: Workflow) -> WorkflowContext:
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
        while not is_waiting_for_user(workflow.state) and workflow.state.phase != WorkflowPhase.DONE:
            workflow = self._process_workflow(workflow, stream)
        return workflow

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

        events: list[WorkflowEventCreate] = []
        if workflow.state.phase == WorkflowPhase.COLLECTING:
            assert workflow.state.last_decision is not None
            assert workflow.state.last_decision.next_step is not None
            event = WorkflowEventCreate(
                type=WorkflowEventType.CLARIFICATION_UPDATED,
                data=ClarificationUpdatedEventData(
                    prompt=workflow.state.last_decision.next_step.prompt,
                    workflow_confidence=workflow.state.last_decision.workflow_confidence,
                    reason=workflow.state.last_decision.reason,
                ).model_dump(),
            )
            events.append(event)
        if workflow.state.phase == WorkflowPhase.DISCUSSION or workflow.state.phase == WorkflowPhase.DONE:
            assert workflow.state.solution is not None
            event = WorkflowEventCreate(
                type=WorkflowEventType.SOLUTION_GENERATED,
                data=SolutionGeneratedEventData(
                    reason=SolutionGeneratedReason.HIGH_CONFIDENCE
                    if len(workflow.state.steps) < workflow.max_steps
                    else SolutionGeneratedReason.MAX_STEPS_REACHED,
                    confidence=workflow.state.solution.confidence,
                    rationale=workflow.state.solution.rationale,
                ).model_dump(),
            )
            events.append(event)

        return self.repo.update_workflow(workflow, events)

    def skip_to_solution(self, workflow_id: UUID, stream: StreamSink | None = None) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        state = workflow.state

        if state.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation("Can only skip to solution in COLLECTING phase")

        state.skipped = True

        workflow = self._process_until_waiting_or_done(workflow, stream)

        assert workflow.state.solution is not None
        event = WorkflowEventCreate(
            type=WorkflowEventType.SOLUTION_GENERATED,
            data=SolutionGeneratedEventData(
                reason=SolutionGeneratedReason.MANUAL_TRIGGER,
                confidence=workflow.state.solution.confidence,
                rationale=workflow.state.solution.rationale,
            ).model_dump(),
        )

        return self.repo.update_workflow(workflow, [event])

    # ------- Creation --------

    def create(self, workflow_create: WorkflowCreate) -> Workflow:
        workflow = Workflow(**workflow_create.model_dump())
        event = WorkflowEventCreate(
            type=WorkflowEventType.WORKFLOW_CREATED,
            data=WorkflowCreatedEventData(
                ticket_title=workflow_create.ticket.title,
                domain_type=workflow_create.domain_type,
                name=workflow_create.name,
            ).model_dump(),
        )
        return self.start(workflow, initial_events=[event])

    def branch(self, workflow_id: UUID, snapshot_id: UUID) -> Workflow:
        parent_workflow = self.get_workflow(workflow_id)
        state = self.repo.get_snapshot(workflow_id, snapshot_id)

        workflow = Workflow(
            ticket=parent_workflow.ticket,
            domain_type=parent_workflow.domain_type,
            name=parent_workflow.name,
            description=parent_workflow.description,
            max_steps=parent_workflow.max_steps,
            parent_id=parent_workflow.id,
            parent_snapshot_id=snapshot_id,
            state=state,
        )

        event = WorkflowEventCreate(
            type=WorkflowEventType.WORKFLOW_BRANCHED,
            data=WorkflowBranchedEventData(
                ticket_title=parent_workflow.ticket.title,
                domain_type=parent_workflow.domain_type,
                parent_name=parent_workflow.name,
                name=parent_workflow.name,
                parent_workflow_id=parent_workflow.id,
                parent_snapshot_id=snapshot_id,
            ).model_dump(),
        )
        return self.start(workflow, initial_events=[event])

    def start(
        self,
        workflow: Workflow,
        *,
        initial_events: list[WorkflowEventCreate] | None = None,
    ) -> Workflow:
        workflow = self._process_until_waiting_or_done(workflow)

        events: list[WorkflowEventCreate] = []
        if initial_events:
            events.extend(initial_events)

        if workflow.state.phase == WorkflowPhase.COLLECTING:
            assert len(workflow.state.steps) >= 1  # at least one answered step and one new step
            assert workflow.state.last_decision is not None
            assert workflow.state.last_decision.next_step is not None
            event = WorkflowEventCreate(
                type=WorkflowEventType.CLARIFICATION_UPDATED,
                data=ClarificationUpdatedEventData(
                    prompt=workflow.state.last_decision.next_step.prompt,
                    workflow_confidence=workflow.state.last_decision.workflow_confidence,
                    reason=workflow.state.last_decision.reason,
                ).model_dump(),
            )
            events.append(event)
        else:
            assert workflow.state.solution is not None
            event = WorkflowEventCreate(
                type=WorkflowEventType.SOLUTION_GENERATED,
                data=SolutionGeneratedEventData(
                    reason=SolutionGeneratedReason.HIGH_CONFIDENCE
                    if len(workflow.state.steps) < workflow.max_steps
                    else SolutionGeneratedReason.MAX_STEPS_REACHED,
                    confidence=workflow.state.solution.confidence,
                    rationale=workflow.state.solution.rationale,
                ).model_dump(),
            )
            events.append(event)

        return self.repo.insert_workflow(workflow, events)

    # -------- Queries --------

    def get_workflow(self, workflow_id: UUID) -> Workflow:
        workflow = self.repo.get_workflow(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow {workflow_id} not found")
        return workflow

    def list_workflows(self) -> list[Workflow]:
        return self.repo.get_workflows()

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

        events: list[WorkflowEventCreate] = []
        requires_solution_update = (
            workflow.state.discussion_result.solution_updated if workflow.state.discussion_result else False
        )
        event = WorkflowEventCreate(
            type=WorkflowEventType.CHAT_REPLIED,
            data=ChatRepliedEventData(
                message_role=user_message.role,
                message_content=user_message.content,
                reply_role=workflow.state.chat_history.messages[-1].role,
                reply_content=workflow.state.chat_history.messages[-1].content,
                requires_solution_update=requires_solution_update,
            ).model_dump(),
        )
        events.append(event)
        if requires_solution_update:
            event = WorkflowEventCreate(type=WorkflowEventType.SOLUTION_UPDATED)
            events.append(event)

        return self.repo.update_workflow(workflow, events)
