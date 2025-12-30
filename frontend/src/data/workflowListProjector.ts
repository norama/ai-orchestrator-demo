import type { WorkflowState } from '@/types/be'
import type { UIWorkflowListItem } from '@/types/fe'

export function workflowToListItem(w: WorkflowState): UIWorkflowListItem {
  return {
    id: w.id,
    name: w.name ?? '(unnamed)',
    ticketTitle: w.ticket.title,
    phase: w.phase,
  }
}
