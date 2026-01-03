import { StatusMarker } from '@/components/ui/StatusMarker'
import { ChatRoleEnum } from '@/types/enums'
import type { UIChatMessage } from '@/types/fe'

interface Props {
  message: UIChatMessage
  pending?: boolean
}

export function ChatMessageView({ message, pending }: Props) {
  const isUser = message.role === ChatRoleEnum.USER

  return (
    <div className={['relative flex', isUser ? 'justify-end' : 'justify-start'].join(' ')}>
      <div
        className={[
          'relative max-w-[70%] rounded-lg px-3 py-2 text-sm whitespace-pre-wrap',
          isUser ? 'bg-blue-100 text-blue-900' : 'bg-gray-100 text-gray-900',
        ].join(' ')}>
        <p>{message.content}</p>

        {/* Status marker – absolutely positioned */}
        <StatusMarker
          variant='pending'
          className={[
            'absolute -bottom-7',
            isUser ? 'right-0' : 'left-0',
            'transition-opacity',
            pending ? 'opacity-100' : 'opacity-0 pointer-events-none',
          ].join(' ')}>
          Sending…
        </StatusMarker>
      </div>
    </div>
  )
}
