import { HeaderLayout } from '@/components/layout/HeaderLayout'
import { WorkflowListItem } from '@/components/sidebar/WorkflowListItem'
import { Button } from '@/components/ui/Button'
import type { UIWorkflowListItem } from '@/types/fe'

interface Props {
  items: UIWorkflowListItem[]
  selectedId: string | null
  onSelect(id: string): void
  onNew(): void
  onSelectParent(item: UIWorkflowListItem): Promise<void>
  disabled?: boolean
}

export function WorkflowListPanel({
  items,
  selectedId,
  onSelect,
  onNew,
  onSelectParent,
  disabled,
}: Props) {
  return (
    <div className='w-60 border-r border-gray-300 bg-white flex flex-col h-full'>
      <HeaderLayout>Workflows</HeaderLayout>

      <div className='flex-1 overflow-y-auto'>
        {items.map((item) => (
          <WorkflowListItem
            key={item.id}
            item={item}
            selected={selectedId === item.id}
            onSelect={() => onSelect(item.id)}
            onSelectParent={() => onSelectParent(item)}
            disabled={disabled}
          />
        ))}
      </div>

      <div className='p-3 border-t border-gray-300'>
        <Button
          variant='secondary'
          className='w-full justify-start'
          onClick={onNew}
          disabled={disabled}>
          🧩 New workflow
        </Button>
      </div>
    </div>
  )
}
