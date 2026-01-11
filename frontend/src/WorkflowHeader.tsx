import { Button } from '@/components/ui/Button'

interface WorkflowHeaderProps {
  workflowName: string | null
  historyCount: number | null
  historyOpen: boolean

  onMobileOpenWorkflows(): void
  onToggleHistory(): void
}

export function WorkflowHeader({
  workflowName,
  historyCount,
  historyOpen,
  onMobileOpenWorkflows,
  onToggleHistory,
}: WorkflowHeaderProps) {
  return (
    <div className='fixed top-0 inset-x-0 z-30 flex items-center gap-3 px-4 h-12 border-b border-gray-300 bg-white'>
      {/* Mobile: workflow list */}
      <button
        onClick={onMobileOpenWorkflows}
        className='lg:hidden text-sm px-2 py-1 rounded hover:bg-gray-100'
        aria-label='Open workflows'
        disabled={historyOpen}>
        ☰
      </button>

      {/* Title */}
      <div className='flex-1 min-w-0'>
        <div className='text-sm font-medium text-gray-800 truncate'>
          {workflowName || 'AI Orchestrator Demo'}
        </div>
      </div>

      {/* History trigger */}
      <Button
        onClick={onToggleHistory}
        disabled={!historyCount}
        variant='ghost'
        aria-pressed={historyOpen}
        aria-expanded={historyOpen}>
        History
        {historyCount !== null && <span className='ml-1 text-gray-500'>· {historyCount}</span>}
        {historyOpen ? ' ▲' : ' ▼'}
      </Button>
    </div>
  )
}
