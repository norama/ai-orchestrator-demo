from uuid import UUID

from app.domain.workflow import Workflow, WorkflowCreate
from app.infrastructure.persistence.workflow_repository import WorkflowRepository


class FakeWorkflowRepository(WorkflowRepository):
    def __init__(self):
        self._store: dict[UUID, Workflow] = {}

    def create(self, workflow_create: WorkflowCreate) -> Workflow:
        workflow = Workflow(**workflow_create.model_dump())
        self._store[workflow.id] = workflow
        return workflow

    def get(self, workflow_id: UUID) -> Workflow:
        return self._store[workflow_id]

    def save(self, workflow: Workflow) -> Workflow:
        self._store[workflow.id] = workflow
        return workflow

    def list(self):
        return list(self._store.values())

    def branch(self, snapshot_id: UUID) -> Workflow:
        raise NotImplementedError()
