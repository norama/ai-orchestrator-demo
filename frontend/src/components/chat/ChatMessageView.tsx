import { ChatRoleEnum } from '@/types/enums'
import type { UIChatMessage } from '@/types/fe'

interface Props {
  message: UIChatMessage
}

export function ChatMessageView({ message }: Props) {
  return (
    <div className='flex flex-col gap-3 p-4 overflow-y-auto'>
      <div
        className={`max-w-[70%] rounded-lg px-3 py-2 text-sm whitespace-pre-wrap
            ${
              message.role === ChatRoleEnum.USER
                ? 'self-end bg-blue-100 text-blue-900'
                : 'self-start bg-gray-100 text-gray-900'
            }`}>
        {message.content}
      </div>
    </div>
  )
}
