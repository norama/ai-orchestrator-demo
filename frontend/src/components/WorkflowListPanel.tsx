import { Button } from '@/components/ui/Button'
import { WorkflowListItem } from '@/components/WorkflowListItem'
import type { UIWorkflowListItem } from '@/types/fe'

interface Props {
  items: UIWorkflowListItem[]
  selectedId: string | null
  onSelect(id: string): void
  onNew(): void
}

export function WorkflowListPanel({ items: workflows, selectedId, onSelect, onNew }: Props) {
  return (
    <div className='w-64 border-r bg-white flex flex-col'>
      <div className='p-3 font-semibold border-b'>Workflows</div>

      <div className='flex-1 overflow-y-auto'>
        {workflows.map((item) => (
          <WorkflowListItem
            key={item.id}
            item={item}
            selected={selectedId === item.id}
            onSelect={() => onSelect(item.id)}
          />
        ))}
      </div>

      <Button className='m-3' onClick={onNew}>
        + New workflow
      </Button>
    </div>
  )
}
