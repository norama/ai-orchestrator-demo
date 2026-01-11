interface WorkflowHeaderProps {
  workflowName: string | null
  historyCount: number | null
  isHistoryOpen: boolean

  onOpenWorkflows(): void
  onToggleHistory(): void
}

export function WorkflowHeader({
  workflowName,
  historyCount,
  isHistoryOpen,
  onOpenWorkflows,
  onToggleHistory,
}: WorkflowHeaderProps) {
  return (
    <div className='fixed top-0 inset-x-0 z-30 flex items-center gap-3 px-4 h-12 border-b border-gray-300 bg-white'>
      {/* Mobile: workflow list */}
      <button
        onClick={onOpenWorkflows}
        className='lg:hidden text-sm px-2 py-1 rounded hover:bg-gray-100'
        aria-label='Open workflows'>
        ☰
      </button>

      {/* Title */}
      <div className='flex-1 min-w-0'>
        <div className='text-sm font-medium text-gray-800 truncate'>
          {workflowName || 'AI Orchestrator Demo'}
        </div>
      </div>

      {/* History trigger */}
      <button
        onClick={onToggleHistory}
        className={`
          text-xs px-2 py-1 rounded border
          ${isHistoryOpen ? 'bg-gray-100 border-gray-400' : 'border-gray-300'}
          hover:bg-gray-100
        `}>
        History
        {historyCount !== null && <span className='ml-1 text-gray-500'>· {historyCount}</span>}
      </button>
    </div>
  )
}
