import { Button } from '@/components/ui/Button'
import type { UIWorkflowListItem } from '@/types/fe'

interface Props {
  workflows: UIWorkflowListItem[]
  selectedId: string | null
  onSelect(id: string): void
  onNew(): void
}

export function WorkflowListPanel({ workflows, selectedId, onSelect, onNew }: Props) {
  return (
    <div className='w-64 border-r bg-white flex flex-col'>
      <div className='p-3 font-semibold border-b'>Workflows</div>

      <div className='flex-1 overflow-y-auto'>
        {workflows.map((w) => (
          <div
            key={w.id}
            onClick={() => onSelect(w.id)}
            className={`p-3 cursor-pointer border-b text-sm
              ${w.id === selectedId ? 'bg-blue-200' : 'hover:bg-gray-100'}
            `}>
            <div className='font-medium truncate'>{w.ticketTitle}</div>
            <div className='text-xs text-gray-500 truncate'>
              {w.name || '(unnamed)'} · {w.phase}
            </div>
          </div>
        ))}
      </div>

      <Button className='m-3' onClick={onNew}>
        + New workflow
      </Button>
    </div>
  )
}
