from uuid import UUID

from app.domain.workflow import WorkflowState, WorkflowStateCreate
from app.infrastructure.persistence.workflow_repository import WorkflowRepository


class FakeWorkflowRepository(WorkflowRepository):
    def __init__(self):
        self._store: dict[UUID, WorkflowState] = {}

    def create(self, workflow_create: WorkflowStateCreate) -> WorkflowState:
        workflow = WorkflowState(**workflow_create.model_dump())
        self._store[workflow.id] = workflow
        return workflow

    def get(self, workflow_id: UUID) -> WorkflowState:
        return self._store[workflow_id]

    def save(self, workflow: WorkflowState) -> WorkflowState:
        self._store[workflow.id] = workflow
        return workflow

    def list(self):
        return list(self._store.values())
