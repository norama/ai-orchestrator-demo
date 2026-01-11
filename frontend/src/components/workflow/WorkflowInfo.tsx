import { Badge } from '@/components/ui/Badge'
import { TicketSummary } from '@/components/workflow/TicketSummary'
import { WorkflowPhaseBadge } from '@/components/workflow/WorkflowPhaseBadge'
import type { UITicket, UIWorkflowData, UIWorkflowState } from '@/types/fe'

interface Props {
  ticket: UITicket
  workflowData: UIWorkflowData
  workflowState: UIWorkflowState
}

export function WorkflowInfo({ ticket, workflowData, workflowState }: Props) {
  const title = workflowData.name?.trim() || ticket.title || 'Workflow'

  return (
    <div className='space-y-4'>
      {/* Workflow title */}
      <div>
        <h1 className='text-2xl font-semibold text-gray-900'>{title}</h1>
        {workflowData.description && (
          <p className='mt-1 text-sm text-gray-600'>{workflowData.description}</p>
        )}
      </div>

      {/* Metadata row */}
      <div className='flex flex-wrap items-center gap-3 text-sm'>
        <Badge variant='info'>{workflowData.domainType}</Badge>
        <WorkflowPhaseBadge phase={workflowState.phase} />

        <span className='text-gray-500'>Max steps: {workflowData.maxSteps}</span>
      </div>

      {/* Ticket */}
      <TicketSummary ticket={ticket} />
    </div>
  )
}
