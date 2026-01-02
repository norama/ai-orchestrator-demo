import { ChatRoleEnum } from '@/types/enums'
import type { UIChatMessage } from '@/types/fe'

interface Props {
  message: UIChatMessage
  pending?: boolean
}

export function ChatMessageView({ message, pending }: Props) {
  return (
    <div
      className={`max-w-[70%] rounded-lg px-3 py-2 text-sm whitespace-pre-wrap
            ${
              message.role === ChatRoleEnum.USER
                ? 'self-end bg-blue-100 text-blue-900'
                : 'self-start bg-gray-100 text-gray-900'
            }`}>
      <p>{message.content}</p>
      {pending && <div className='mt-1 text-xs text-gray-400'>Sending…</div>}
    </div>
  )
}
