import type { Workflow } from '@/types/be'
import type { UIWorkflowListItem } from '@/types/fe'

export function workflowToListItem(w: Workflow): UIWorkflowListItem {
  return {
    id: w.id,
    name: w.name ?? '(unnamed)',
    ticketTitle: w.ticket.title,
    domainType: w.domain_type,
    phase: w.state.phase,
  }
}
