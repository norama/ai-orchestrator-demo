from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.event import EVENT_DATA_MODELS, DisplayableEventData, EventDisplayItem, WorkflowEvent, WorkflowEventType


class WorkflowEventView(BaseModel):
    id: UUID
    snapshot_id: UUID
    previous_snapshot_id: UUID | None
    created_at: datetime

    type: WorkflowEventType
    label: str
    display: list[EventDisplayItem] | None


def event_label(event_type: WorkflowEventType) -> str:
    labels = {
        WorkflowEventType.WORKFLOW_CREATED: "Workflow Created",
        WorkflowEventType.WORKFLOW_BRANCHED: "Workflow Branched",
        WorkflowEventType.CLARIFICATION_UPDATED: "Clarification Updated",
        WorkflowEventType.SOLUTION_GENERATED: "Solution Generated",
        WorkflowEventType.CHAT_REPLIED: "Chat Replied",
        WorkflowEventType.WORKFLOW_COMPLETED: "Workflow Completed",
        WorkflowEventType.SOLUTION_UPDATED: "Solution Updated",
    }
    return labels.get(event_type, "Unknown Event")


def event_to_view(event: WorkflowEvent) -> WorkflowEventView:
    data_model = EVENT_DATA_MODELS.get(event.type)

    if data_model and not event.data:
        raise ValueError(f"Event data is missing for event type {event.type}")
    if not data_model and event.data:
        raise ValueError(f"No data model found for event type {event.type} with data")

    display = None
    if data_model and event.data:
        data_obj = data_model.model_validate(event.data)

        if not isinstance(data_obj, DisplayableEventData):
            raise ValueError(f"Event data model for type {event.type} does not support display")

        display = data_obj.to_display()

    return WorkflowEventView(
        id=event.id,
        snapshot_id=event.snapshot_id,
        previous_snapshot_id=event.previous_snapshot_id,
        created_at=event.created_at,
        type=event.type,
        label=event_label(event.type),
        display=display,
    )
