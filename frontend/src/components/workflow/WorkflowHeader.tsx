import { Badge } from '@/components/ui/Badge'
import { TicketSummary } from '@/components/workflow/TicketSummary'
import { WorkflowPhaseBadge } from '@/components/workflow/WorkflowPhaseBadge'
import type { UITicket, UIWorkflowData } from '@/types/fe'

interface WorkflowHeaderProps {
  workflow: UIWorkflowData
  ticket: UITicket
}

export function WorkflowHeader({ workflow, ticket }: WorkflowHeaderProps) {
  const title = workflow.name?.trim() || ticket.title || 'Workflow'

  return (
    <div className='space-y-4'>
      {/* Workflow title */}
      <div>
        <h1 className='text-2xl font-semibold text-gray-900'>{title}</h1>
        {workflow.description && (
          <p className='mt-1 text-sm text-gray-600'>{workflow.description}</p>
        )}
      </div>

      {/* Metadata row */}
      <div className='flex flex-wrap items-center gap-3 text-sm'>
        <Badge variant='info'>{workflow.domainType}</Badge>
        <WorkflowPhaseBadge phase={workflow.phase} />

        <span className='text-gray-500'>Max steps: {workflow.maxSteps}</span>
      </div>

      {/* Ticket */}
      <TicketSummary ticket={ticket} />
    </div>
  )
}
