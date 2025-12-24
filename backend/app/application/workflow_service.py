from datetime import datetime, timezone
from uuid import UUID

from app.application.commands import (
    AddAnswerCommand,
    AddChatMessageCommand,
    AddStepCommand,
    ChangePhaseCommand,
)
from app.application.exceptions import InvalidWorkflowOperation, WorkflowNotFound
from app.application.solve_service import SolveService
from app.application.step_generator import StepGenerator
from app.domain.chat import ChatMessage
from app.domain.workflow import (
    ClarificationStep,
    WorkflowContext,
    WorkflowPhase,
    WorkflowState,
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
        solve_service: SolveService,
    ):
        self.repo = repo
        self.step_generator = step_generator
        self.solve_service = solve_service

    def _build_context(self, wf: WorkflowState) -> WorkflowContext:
        return WorkflowContext(
            workflow_id=wf.id,
            ticket=wf.ticket,
            steps=wf.steps,
            skipped=wf.skipped,
            max_steps=wf.max_steps,
            phase=wf.phase,
        )

    # ------- Creation --------

    def create(self, workflow_create: WorkflowState) -> WorkflowState:
        return self.repo.create(workflow_create)

    # -------- Queries --------

    def get_workflow(self, workflow_id: UUID) -> WorkflowState:
        workflow = self.repo.get(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow {workflow_id} not found")
        return workflow

    def list_workflows(self) -> list[WorkflowState]:
        return self.repo.list()

    # -------- Commands --------

    def change_phase(
        self,
        workflow_id: UUID,
        cmd: ChangePhaseCommand,
    ) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        # minimal domain rule (example)
        if workflow.phase == WorkflowPhase.DONE:
            raise InvalidWorkflowOperation("Cannot change phase of DONE workflow")

        workflow.phase = cmd.phase

        return self.repo.save(workflow)

    def add_step(
        self,
        workflow_id: UUID,
        cmd: AddStepCommand,
    ) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        if workflow.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation(
                "Steps can only be added in COLLECTING phase"
            )

        step = ClarificationStep(prompt=cmd.prompt)
        workflow.steps.append(step)

        return self.repo.save(workflow)

    def add_answer(
        self,
        workflow_id: UUID,
        cmd: AddAnswerCommand,
    ) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        if workflow.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation(
                "Answers can only be added in COLLECTING phase"
            )

        step = next(step for step in workflow.steps if step.id == cmd.clarification_id)
        step.answer = cmd.answer

        return self.repo.save(workflow)

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
