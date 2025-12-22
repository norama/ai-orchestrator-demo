from datetime import datetime, timezone
from uuid import UUID

from app.application.commands import (
    AddAnswerCommand,
    AddChatMessageCommand,
    ChangePhaseCommand,
)
from app.application.exceptions import InvalidWorkflowOperation, WorkflowNotFound
from app.domain.chat import ChatMessage
from app.domain.qa import Clarification
from app.domain.workflow import WorkflowPhase, WorkflowState
from app.infrastructure.persistence.workflow_repository import WorkflowRepository


class WorkflowService:
    def __init__(self, repo: WorkflowRepository):
        self.repo = repo

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

    def add_question(
        self,
        workflow_id: UUID,
        question: str,
    ) -> WorkflowState:
        workflow = self.get_workflow(workflow_id)

        if workflow.phase != WorkflowPhase.COLLECTING:
            raise InvalidWorkflowOperation(
                "Questions can only be added in COLLECTING phase"
            )

        qa = Clarification(question=question)
        workflow.clarifications.append(qa)

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

        qa = next(q for q in workflow.clarifications if q.id == cmd.clarification_id)
        qa.answer = cmd.answer

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
