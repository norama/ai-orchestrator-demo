import { DomainBadge } from '@/components/workflow/DomainBadge'
import { WorkflowPhaseBadge } from '@/components/workflow/WorkflowPhaseBadge'
import type { UIWorkflowListItem } from '@/types/fe'
import { useEffect, useRef } from 'react'

interface Props {
  item: UIWorkflowListItem
  selected: boolean
  onSelect: () => void
  onSelectParent: () => void
  disabled?: boolean
}

export function WorkflowListItem({ item, selected, onSelect, onSelectParent, disabled }: Props) {
  const ref = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (selected && ref.current) {
      ref.current.scrollIntoView({
        block: 'nearest',
        behavior: 'auto', // important: no animation
      })
    }
  }, [selected])

  const hasParent = item.parentId && item.parentSnapshotId

  return (
    <div
      ref={ref}
      onClick={disabled ? undefined : onSelect}
      className={[
        'relative px-3 py-2 transition',
        'border-b border-gray-100',
        selected ? 'bg-blue-50' : !disabled ? 'hover:bg-gray-100' : '',
        disabled ? 'opacity-80' : '',
        disabled || selected ? 'cursor-default' : 'cursor-pointer',
      ].join(' ')}>
      {/* Selected accent */}
      {selected && <div className='absolute left-0 top-0 bottom-0 w-1 bg-blue-500' />}

      <div className='space-y-1'>
        {/* Row 1: Ticket title */}
        <div className='flex items-center gap-1 min-w-0'>
          <div className='text-sm font-medium text-gray-900 truncate flex-1'>
            {item.ticketTitle}
          </div>

          {hasParent && (
            <span className='text-xs text-green-600 shrink-0' aria-label='Branched workflow'>
              🌱
            </span>
          )}
        </div>

        {/* Row 2: Workflow name */}
        <div className='text-xs text-gray-600 truncate'>{item.name || '(unnamed)'}</div>

        {/* Row 3: Badges, Parent action */}
        <div className='flex items-center justify-between gap-2 pt-0.5 h-6'>
          {/* Left side: badges */}
          <div className='flex items-center gap-1.5'>
            <DomainBadge domainType={item.domainType} />
            <WorkflowPhaseBadge phase={item.phase} />
          </div>

          {/* Right side: reserved action slot */}
          <button
            onClick={(e) => {
              e.stopPropagation()
              onSelectParent()
            }}
            disabled={!selected || !hasParent || disabled}
            className={[
              'text-gray-500 hover:text-gray-800',
              'mb-1 leading-none',
              'transition-opacity',
              selected && hasParent
                ? 'cursor-pointer opacity-75 hover:opacity-100'
                : 'invisible pointer-events-none',
            ].join(' ')}
            aria-label='Go to parent snapshot'>
            ↩️
          </button>
        </div>
      </div>
    </div>
  )
}
