import { Badge } from '@/components/ui/Badge'
import type { UIWorkflowListItem } from '@/types/fe'
import { useEffect, useRef } from 'react'

interface Props {
  item: UIWorkflowListItem
  selected: boolean
  onSelect: () => void
}

export function WorkflowListItem({ item, selected, onSelect }: Props) {
  const ref = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (selected && ref.current) {
      ref.current.scrollIntoView({
        block: 'nearest',
        behavior: 'auto', // important: no animation
      })
    }
  }, [selected])

  const phaseVariant =
    item.phase === 'DONE' ? 'success' : item.phase === 'SOLVING' ? 'warning' : 'info'

  return (
    <div
      ref={ref}
      onClick={onSelect}
      className={[
        'relative px-3 py-2 cursor-pointer transition',
        'border-b border-gray-100',
        selected ? 'bg-blue-50' : 'hover:bg-gray-100',
      ].join(' ')}>
      {/* Selected accent */}
      {selected && <div className='absolute left-0 top-0 bottom-0 w-1 bg-blue-500' />}

      <div className='space-y-0.5'>
        {/* Row 1: Ticket title */}
        <div className='text-sm font-medium text-gray-900 truncate'>{item.ticketTitle}</div>

        {/* Row 2: Workflow name */}
        <div className='text-xs text-gray-600 truncate'>{item.name || '(unnamed)'}</div>

        {/* Row 3: Badges */}
        <div className='flex items-center gap-1.5 pt-0.5'>
          <Badge>{item.domainType}</Badge>
          <Badge variant={phaseVariant}>{item.phase}</Badge>
        </div>
      </div>
    </div>
  )
}
