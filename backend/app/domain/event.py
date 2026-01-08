from datetime import datetime
from enum import Enum
from typing import Any, Protocol, runtime_checkable
from uuid import UUID

from pydantic import BaseModel

from app.domain.chat import ChatRole
from app.domain.config import DomainType


class WorkflowEventType(str, Enum):
    WORKFLOW_CREATED = "WORKFLOW_CREATED"
    WORKFLOW_BRANCHED = "WORKFLOW_BRANCHED"
    CLARIFICATION_UPDATED = "CLARIFICATION_UPDATED"
    SOLUTION_GENERATED = "SOLUTION_GENERATED"
    CHAT_REPLIED = "CHAT_REPLIED"
    SOLUTION_UPDATED = "SOLUTION_UPDATED"
    WORKFLOW_COMPLETED = "WORKFLOW_COMPLETED"


class SolutionGeneratedReason(str, Enum):
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    MAX_STEPS_REACHED = "MAX_STEPS_REACHED"
    MANUAL_TRIGGER = "MANUAL_TRIGGER"


class EventDisplayType(str, Enum):
    TEXT = "text"
    CONFIDENCE = "confidence"
    BOOLEAN = "boolean"
    FLAG = "flag"
    CODE = "code"


class EventDisplayItem(BaseModel):
    type: EventDisplayType = EventDisplayType.TEXT
    label: str
    value: str | float | bool
    emphasis: bool = False


@runtime_checkable
class DisplayableEventData(Protocol):
    def to_display(self) -> list[EventDisplayItem]: ...


class WorkflowCreatedEventData(BaseModel):
    ticket_title: str
    domain_type: DomainType
    name: str | None

    def __str__(self) -> str:
        return f"""
            ticket title: {self.ticket_title},
            domain type: {self.domain_type},
            name: {self.name or "N/A"},
        """

    def to_display(self) -> list[EventDisplayItem]:
        items = [
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label="Ticket Title",
                value=self.ticket_title,
            ),
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label="Domain Type",
                value=self.domain_type.value,
            ),
        ]
        if self.name:
            items.append(
                EventDisplayItem(
                    type=EventDisplayType.TEXT,
                    label="Workflow Name",
                    value=self.name,
                )
            )
        return items


class WorkflowBranchedEventData(WorkflowCreatedEventData):
    parent_workflow_id: UUID
    parent_snapshot_id: UUID
    parent_name: str | None = None

    def __str__(self) -> str:
        return f"""
            parent workflow: {self.parent_name or "N/A"},
            ticket title: {self.ticket_title},
            domain type: {self.domain_type},
            name: {self.name or "N/A"},
        """

    def to_display(self) -> list[EventDisplayItem]:
        items = super().to_display()
        items.insert(
            0,
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label="Parent Workflow",
                value=self.parent_name or str(self.parent_workflow_id),
                emphasis=True,
            ),
        )
        return items


class ClarificationUpdatedEventData(BaseModel):
    prompt: str
    workflow_confidence: float
    reason: str

    def __str__(self) -> str:
        return f"""
            workflow confidence: {self.workflow_confidence * 100}%,
            reason: {self.reason}
            prompt: {self.prompt or "N/A"}
            {"further clarification needed" if self.prompt else "solution can be generated"}
        """

    def to_display(self) -> list[EventDisplayItem]:
        items = [
            EventDisplayItem(
                type=EventDisplayType.CONFIDENCE,
                label="Workflow Confidence",
                value=self.workflow_confidence,
            ),
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label="Reason",
                value=self.reason,
            ),
        ]
        if self.prompt:
            items.append(
                EventDisplayItem(
                    type=EventDisplayType.TEXT,
                    label="Clarification Prompt",
                    value=self.prompt,
                )
            )
        else:
            items.append(
                EventDisplayItem(
                    type=EventDisplayType.FLAG,
                    label="Clarification Status",
                    value="Solution can be generated",
                )
            )
        return items


class SolutionGeneratedEventData(BaseModel):
    reason: SolutionGeneratedReason
    confidence: float
    rationale: str | None = None

    def reason_label(self) -> str:
        if self.reason == SolutionGeneratedReason.HIGH_CONFIDENCE:
            return "High Confidence"
        if self.reason == SolutionGeneratedReason.MAX_STEPS_REACHED:
            return "Max Steps Reached"
        if self.reason == SolutionGeneratedReason.MANUAL_TRIGGER:
            return "Manual Trigger"
        return "Unknown Reason"

    def __str__(self) -> str:
        return f"""
            confidence: {self.confidence * 100}%,
            reason: {self.reason_label()},
            rationale: {self.rationale or "N/A"}
        """

    def to_display(self) -> list[EventDisplayItem]:
        items = [
            EventDisplayItem(
                type=EventDisplayType.CONFIDENCE,
                label="Confidence",
                value=self.confidence,
            ),
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label="Reason",
                value=self.reason_label(),
            ),
        ]
        if self.rationale:
            items.append(
                EventDisplayItem(
                    type=EventDisplayType.TEXT,
                    label="Rationale",
                    value=self.rationale,
                )
            )
        return items


class ChatRepliedEventData(BaseModel):
    message_role: ChatRole
    message_content: str
    reply_role: ChatRole
    reply_content: str
    requires_solution_update: bool

    def __str__(self) -> str:
        return f"""
            {self.message_role}: {self.message_content},
            {self.reply_role}: {self.reply_content},
            solution will be updated: {self.requires_solution_update}
        """

    def to_display(self) -> list[EventDisplayItem]:
        items = [
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label=f"{self.message_role} Message",
                value=self.message_content,
            ),
            EventDisplayItem(
                type=EventDisplayType.TEXT,
                label=f"{self.reply_role} Reply",
                value=self.reply_content,
            ),
            EventDisplayItem(
                type=EventDisplayType.BOOLEAN,
                label="Requires Solution Update",
                value=self.requires_solution_update,
                emphasis=True,
            ),
        ]
        return items


EVENT_DATA_MODELS: dict[WorkflowEventType, type[BaseModel]] = {
    WorkflowEventType.WORKFLOW_CREATED: WorkflowCreatedEventData,
    WorkflowEventType.WORKFLOW_BRANCHED: WorkflowBranchedEventData,
    WorkflowEventType.CLARIFICATION_UPDATED: ClarificationUpdatedEventData,
    WorkflowEventType.SOLUTION_GENERATED: SolutionGeneratedEventData,
    WorkflowEventType.CHAT_REPLIED: ChatRepliedEventData,
}


class WorkflowEventCreate(BaseModel):
    type: WorkflowEventType
    data: dict[str, Any] | None = None


class WorkflowEvent(WorkflowEventCreate):
    id: UUID
    workflow_id: UUID

    snapshot_id: UUID
    previous_snapshot_id: UUID | None = None

    created_at: datetime
