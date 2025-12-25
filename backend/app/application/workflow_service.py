from datetime import datetime, timezone
from uuid import UUID

from app.application.answer_parser import AnswerParser
from app.application.commands import (
    AddChatMessageCommand,
    AnswerStepCommand,
)
from app.application.exceptions import InvalidWorkflowOperation, WorkflowNotFound
from app.application.solution_service import SolutionService
from app.application.step_generator import StepGenerator
from app.domain.chat import ChatMessage
from app.domain.workflow import (
    WaitingReason,
    WorkflowContext,
    WorkflowPhase,
    WorkflowState,
    WorkflowStateCreate,
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


class WorkflowService:
    def __init__(
        self,
        repo: WorkflowRepository,
        step_generator: StepGenerator,
        solution_service: SolutionService,
        answer_parser: AnswerParser,
    ):
        self.repo = repo
        self.step_generator = step_generator
        self.solution_service = solution_service
        self.answer_parser = answer_parser

    def _build_context(self, wf: WorkflowState) -> WorkflowContext:
        return WorkflowContext(
            workflow_id=wf.id,
            ticket=wf.ticket,
            steps=wf.steps,
            last_decision=wf.last_decision,
            skipped=wf.skipped,
            max_steps=wf.max_steps,
            phase=wf.phase,
        )

    # ------- Engine loop --------

    def _process_workflow(self, workflow: WorkflowState) -> WorkflowState:
        # hard stop
        if workflow.phase in {WorkflowPhase.DISCUSSION, WorkflowPhase.DONE}:
            return workflow

        # process COLLECTING phase
        if workflow.phase == WorkflowPhase.COLLECTING:
            if workflow.skipped or len(workflow.steps) >= workflow.max_steps:
                # move to SOLVING phase if max steps reached
                workflow.phase = WorkflowPhase.SOLVING
                return workflow

            ctx = self._build_context(workflow)
            decision = self.step_generator.propose_next(ctx)

            workflow.last_decision = decision
            if decision.next_step:
                workflow.steps.append(decision.next_step)
                return workflow

            workflow.phase = WorkflowPhase.SOLVING
            return workflow

        # process SOLVING phase
        if workflow.phase == WorkflowPhase.SOLVING:
            ctx = self._build_context(workflow)
            workflow.solution = self.solution_service.generate_solution(ctx)
            workflow.phase = WorkflowPhase.DISCUSSION
            return workflow

        return workflow

    def _process_until_waiting(self, workflow: WorkflowState) -> WorkflowState:
        while not self._is_waiting_for_user(workflow):
            workflow = self._process_workflow(workflow)
        return workflow

    def _has_open_step(self, workflow: WorkflowState) -> bool:
        return any(step.answer is None for step in workflow.steps)

    def get_waiting_reason(self, workflow: WorkflowState) -> WaitingReason | None:
        if workflow.phase == WorkflowPhase.COLLECTING and workflow.skipped:
            return None
        if workflow.phase == WorkflowPhase.COLLECTING and self._has_open_step(workflow):
            return WaitingReason.ANSWER_NEEDED
        if workflow.phase == WorkflowPhase.DISCUSSION:
            return WaitingReason.CHAT
        return None

    def get_confidence(self, workflow: WorkflowState) -> float | None:
        if workflow.solution:
            return workflow.solution.confidence
        if workflow.last_decision:
            return workflow.last_decision.confidence
        return None

    def _is_waiting_for_user(self, workflow: WorkflowState) -> bool:
        return self.get_waiting_reason(workflow) is not None

    # ------- Commands with processing --------

    def answer_step(
        self,
        workflow_id: UUID,
        cmd: AnswerStepCommand,
    ) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        if workflow.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation("Answers can only be added in COLLECTING phase")

        step = next(
            (s for s in workflow.steps if s.id == cmd.step_id),
            None,
        )

        if step is None:
            raise InvalidWorkflowOperation("Step not found")

        if step.answer is not None:
            raise InvalidWorkflowOperation("Step already answered")

        step.answer = cmd.answer

        # domain-specific interpretation hook
        self.answer_parser.parse_answer(step)

        workflow = self._process_until_waiting(workflow)
        return self.repo.save(workflow)

    def skip_to_solution(self, workflow_id: UUID) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        if workflow.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation("Can only skip to solution in COLLECTING phase")

        workflow.skipped = True

        workflow = self._process_until_waiting(workflow)
        return self.repo.save(workflow)

    # ------- Creation --------

    def create(self, workflow_create: WorkflowStateCreate) -> WorkflowState:
        workflow = self.repo.create(workflow_create)

        workflow = self._process_until_waiting(workflow)
        return self.repo.save(workflow)

    # -------- Queries --------

    def get_workflow(self, workflow_id: UUID) -> WorkflowState:
        workflow = self.repo.get(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow {workflow_id} not found")
        return workflow

    def list_workflows(self) -> list[WorkflowState]:
        return self.repo.list()

    def add_chat_message(
        self,
        workflow_id: UUID,
        cmd: AddChatMessageCommand,
    ) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        if not cmd.content.strip():
            raise InvalidWorkflowOperation("Chat message content cannot be empty")

        message = ChatMessage(
            role=cmd.role,
            content=cmd.content,
            created_at=datetime.now(timezone.utc),
        )

        workflow.chat_history.add_message(message)

        return self.repo.save(workflow)
