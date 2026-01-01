import type { UIWorkflowListItem } from '@/types/fe'

interface Props {
  item: UIWorkflowListItem
  selected: boolean
  onSelect: () => void
}

export function WorkflowListItem({ item, selected, onSelect }: Props) {
  return (
    <div
      key={item.id}
      onClick={onSelect}
      className={`p-3 cursor-pointer border-b text-sm
              ${selected ? 'bg-blue-200' : 'hover:bg-gray-100'}
            `}>
      <div className='font-medium truncate'>
        {item.ticketTitle} ({item.domainType})
      </div>
      <div className='text-xs text-gray-500 truncate'>
        {item.name || '(unnamed)'} · {item.phase}
      </div>
    </div>
  )
}
