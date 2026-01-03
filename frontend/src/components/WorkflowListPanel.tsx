import { WorkflowListItem } from '@/components/sidebar/WorkflowListItem'
import { Button } from '@/components/ui/Button'
import type { UIWorkflowListItem } from '@/types/fe'

interface Props {
  items: UIWorkflowListItem[]
  selectedId: string | null
  onSelect(id: string): void
  onNew(): void
}

export function WorkflowListPanel({ items, selectedId, onSelect, onNew }: Props) {
  return (
    <div className='w-60 border-r border-gray-300 bg-white flex flex-col'>
      <div className='px-3 py-2 text-sm font-medium border-b border-gray-300 text-gray-700'>
        Workflows
      </div>

      <div className='flex-1 overflow-y-auto'>
        {items.map((item) => (
          <WorkflowListItem
            key={item.id}
            item={item}
            selected={selectedId === item.id}
            onSelect={() => onSelect(item.id)}
          />
        ))}
      </div>

      <div className='p-3 border-t border-gray-300'>
        <Button variant='secondary' className='w-full justify-start' onClick={onNew}>
          + New workflow
        </Button>
      </div>
    </div>
  )
}
