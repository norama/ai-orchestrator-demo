import type { EventDisplayItem, WorkflowEventView, WorkflowHistoryResponse } from '@/types/be'
import type { UIEventDisplayItem, UIWorkflowEvent, UIWorkflowHistory } from '@/types/fe'

export function workflowHistoryToUI(res: WorkflowHistoryResponse): UIWorkflowHistory {
  return {
    workflowId: res.workflow_id,
    parentWorkflowId: res.parent_workflow_id,
    currentSnapshotId: res.current_snapshot_id,
    events: res.events.map((e) => workflowEventToUI(e, res.current_snapshot_id)),
  }
}

function workflowEventToUI(event: WorkflowEventView, currentSnapshotId: string): UIWorkflowEvent {
  return {
    id: event.id,
    snapshotId: event.snapshot_id,
    previousSnapshotId: event.previous_snapshot_id,
    createdAt: new Date(event.created_at),

    type: event.type,
    label: event.label,
    display: event.display ? event.display.map(eventDisplayItemToUI) : null,

    isCurrent: event.snapshot_id === currentSnapshotId,
  }
}

function eventDisplayItemToUI(item: EventDisplayItem): UIEventDisplayItem {
  return {
    type: item.type,
    label: item.label,
    value: item.value,
    emphasis: item.emphasis,
  }
}
