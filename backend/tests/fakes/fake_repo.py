from uuid import UUID

from app.domain.event import WorkflowEvent, WorkflowEventCreate
from app.domain.workflow import Workflow, WorkflowState
from app.infrastructure.persistence.workflow_repository import WorkflowRepository


class FakeWorkflowRepository(WorkflowRepository):
    def __init__(self):
        self._store: dict[UUID, Workflow] = {}
        self._events: dict[UUID, list[WorkflowEventCreate]] = {}

    def insert_workflow(self, workflow: Workflow, events: list[WorkflowEventCreate] | None = None) -> Workflow:
        self._store[workflow.id] = workflow
        if events:
            self._events.setdefault(workflow.id, []).extend(events)
        return workflow

    def get_workflow(self, workflow_id: UUID) -> Workflow:
        return self._store[workflow_id]

    def update_workflow(self, workflow: Workflow, events: list[WorkflowEventCreate] | None = None) -> Workflow:
        self._store[workflow.id] = workflow
        if events:
            self._events.setdefault(workflow.id, []).extend(events)
        return workflow

    def get_workflows(self):
        return list(self._store.values())

    def get_events(self, workflow_id: UUID) -> list[WorkflowEvent]:
        raise NotImplementedError()

    def get_current_snapshot_id(self, workflow_id: UUID) -> UUID:
        raise NotImplementedError()

    def get_snapshot(self, workflow_id: UUID, snapshot_id: UUID) -> WorkflowState:
        return self._store[workflow_id].state
