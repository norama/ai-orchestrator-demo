import { WorkflowEventView } from '@/components/history/WorkflowEventView'
import { HeaderLayout } from '@/components/layout/HeaderLayout'
import type { UIWorkflowHistory } from '@/types/fe'
import { useState } from 'react'

interface Props {
  history: UIWorkflowHistory
  previewingSnapshotId: string | null
  onPreviewSnapshot: (snapshotId: string) => Promise<void>
}

export function WorkflowHistoryPanel({ history, previewingSnapshotId, onPreviewSnapshot }: Props) {
  const [expandedEventId, setExpandedEventId] = useState<string | null>(null)

  const handleExpandCollapse = (eventId: string) => {
    setExpandedEventId((prevId) => (prevId === eventId ? null : eventId))
  }

  return (
    <div className='h-full flex flex-col'>
      {/* Header */}
      <HeaderLayout>History · {history.events.length} events</HeaderLayout>
      {/* Timeline */}
      <div className='flex-1 overflow-y-auto p-3 space-y-2'>
        {history.events.map((event) => (
          <WorkflowEventView
            key={event.id}
            event={event}
            expanded={expandedEventId === event.id}
            previewing={previewingSnapshotId === event.snapshotId}
            onExpandCollapse={() => handleExpandCollapse(event.id)}
            onPreview={() => onPreviewSnapshot(event.snapshotId)}
          />
        ))}
      </div>
    </div>
  )
}
