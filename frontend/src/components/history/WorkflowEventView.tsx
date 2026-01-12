import { Badge, type BadgeVariant } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { EventDisplayTypeEnum, type WorkflowEventTypeEnum } from '@/types/enums'
import type { UIEventDisplayItem, UIWorkflowEvent } from '@/types/fe'

const EVENT_STYLE: Record<
  WorkflowEventTypeEnum,
  {
    icon: string
    badge: BadgeVariant
  }
> = {
  WORKFLOW_CREATED: { icon: '🧩', badge: 'info' },
  WORKFLOW_BRANCHED: { icon: '🌱', badge: 'info' },
  CLARIFICATION_UPDATED: { icon: '🔁', badge: 'warning' },
  SOLUTION_GENERATED: { icon: '💡', badge: 'success' },
  SOLUTION_UPDATED: { icon: '✏️', badge: 'info' },
  CHAT_REPLIED: { icon: '💬', badge: 'neutral' },
  WORKFLOW_COMPLETED: { icon: '✅', badge: 'success' },
}

function EventDisplayValue({ item }: { item: UIEventDisplayItem }) {
  const baseText = 'line-clamp-2 break-words'

  switch (item.type) {
    case EventDisplayTypeEnum.CONFIDENCE:
      return <Badge variant='success'>{Math.round(Number(item.value) * 100)}%</Badge>

    case EventDisplayTypeEnum.BOOLEAN:
      return (
        <span
          className={[
            'inline-flex items-center justify-center font-semibold',
            item.value ? 'text-green-600' : 'text-gray-400',
          ].join(' ')}
          title={item.value ? 'Yes' : 'No'}>
          {item.value ? '✔' : '✖'}
        </span>
      )

    case EventDisplayTypeEnum.FLAG:
      return <Badge variant='info'>{String(item.value)}</Badge>

    case EventDisplayTypeEnum.CODE:
      return (
        <pre
          className={['text-xs bg-gray-100 rounded px-2 py-1', 'overflow-hidden', baseText].join(
            ' ',
          )}>
          {String(item.value)}
        </pre>
      )

    default:
      return <div className={baseText}>{String(item.value)}</div>
  }
}

interface Props {
  event: UIWorkflowEvent
  expanded?: boolean
  previewing?: boolean
  onExpandCollapse: () => void
  onPreview: () => void
  onBranch: () => Promise<void>
  disabled?: boolean
}

export function WorkflowEventView({
  event,
  expanded,
  previewing,
  onExpandCollapse,
  onPreview,
  onBranch,
  disabled,
}: Props) {
  const style = EVENT_STYLE[event.type]

  return (
    <div
      data-snapshot-id={event.snapshotId}
      className={[
        'border rounded-md px-3 py-2 ',
        'transition-colors',
        previewing
          ? 'border-yellow-400 bg-yellow-50'
          : event.isCurrent
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-200 bg-white',
      ].join(' ')}>
      {/* Header */}
      <div
        className={[
          'flex items-center gap-2 select-none',
          expanded ? 'pb-2 border-b border-gray-200' : '',
          disabled ? 'cursor-default' : 'cursor-pointer',
        ].join(' ')}
        onClick={!disabled ? () => onExpandCollapse() : undefined}>
        <span className='text-lg'>{style.icon}</span>

        <div className='flex-1 min-w-0'>
          <div className='text-sm font-medium text-gray-900 truncate'>{event.label}</div>
          <div className='text-xs text-gray-500'>{event.createdAt.toLocaleString()}</div>
        </div>

        {!previewing && event.isCurrent && <Badge variant='info'>Live</Badge>}
        {previewing && <Badge variant='warning'>Preview</Badge>}

        <span className='text-gray-400 text-sm'>{expanded ? '▲' : '▼'}</span>
      </div>

      {/* Expanded details */}
      <div
        className={[
          'overflow-hidden transition-[max-height,opacity]',
          'duration-200 ease-out',
          expanded ? 'max-h-125 opacity-100 delay-80' : 'max-h-0 opacity-0 delay-80',
        ].join(' ')}>
        <div className='mt-3 space-y-3 text-sm'>
          {event.display &&
            event.display.map((item, i) => (
              <div key={i} className='space-y-1'>
                {/* Label */}
                <div className='text-xs font-medium text-gray-600'>{item.label}</div>

                {/* Value */}
                <div className={item.emphasis ? 'font-medium' : ''}>
                  <EventDisplayValue item={item} />
                </div>
              </div>
            ))}

          <div className='pb-1 flex justify-end'>
            {previewing ? (
              <Button variant='primary' onClick={() => onBranch()} disabled={disabled}>
                🌱 Branch from here
              </Button>
            ) : (
              <Button variant='secondary' onClick={() => onPreview()} disabled={disabled}>
                👁️ Preview snapshot
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
