import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'

interface WorkflowHeaderProps {
  workflowName: string | null
  historyCount: number | null
  historyOpen: boolean
  isPreview: boolean

  onMobileOpenWorkflows(): void
  onToggleHistory(): void
  onNewWorkflow(): void
  onBackToLive(): void
  onBranch(): void
  disabled?: boolean
}

export function WorkflowHeader({
  workflowName,
  historyCount,
  historyOpen,
  isPreview,
  onMobileOpenWorkflows,
  onToggleHistory,
  onNewWorkflow,
  onBackToLive,
  onBranch,
  disabled,
}: WorkflowHeaderProps) {
  return (
    <div
      className={[
        'fixed top-0 inset-x-0 z-30 flex items-center gap-4 px-4 h-16 border-b',
        isPreview ? 'bg-yellow-50 border-yellow-300' : 'bg-white border-gray-300',
      ].join(' ')}>
      {/* Mobile workflows */}
      <Button
        variant='ghost'
        onClick={onMobileOpenWorkflows}
        className='lg:hidden text-sm px-2 py-1 rounded hover:bg-gray-100'
        aria-label='Open workflows'
        disabled={historyOpen || disabled}>
        ☰
      </Button>

      {/* Title */}
      <div className='flex-1 min-w-0 flex items-center gap-2'>
        <div className='text-sm font-medium text-gray-800 truncate'>
          {workflowName || 'AI Orchestrator Demo'}
        </div>

        {isPreview && <Badge variant='warning'>Preview</Badge>}
      </div>

      {/* Desktop actions */}
      <div className='hidden lg:flex items-center gap-4'>
        {isPreview ? (
          <>
            <Button variant='secondary' onClick={onBackToLive} disabled={disabled}>
              ↩️ Back to live
            </Button>

            <Button variant='primary' onClick={onBranch} disabled={disabled}>
              🌱 Branch from here
            </Button>
          </>
        ) : (
          <Button variant='secondary' onClick={onNewWorkflow} disabled={disabled}>
            🧩 New workflow
          </Button>
        )}
      </div>

      {/* Mobile actions */}
      <div className='flex lg:hidden items-center gap-4'>
        {isPreview ? (
          <Button variant='secondary' onClick={onBackToLive} disabled={disabled}>
            ↩️ Live
          </Button>
        ) : (
          <Button variant='secondary' onClick={onNewWorkflow} disabled={disabled}>
            🧩 New
          </Button>
        )}
      </div>

      {/* History */}
      <Button
        onClick={onToggleHistory}
        disabled={!historyCount || disabled}
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
