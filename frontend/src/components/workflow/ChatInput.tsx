import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { StatusMarker } from '@/components/ui/StatusMarker'
import { useState } from 'react'

interface Props {
  onSend: (text: string) => void
  placeholder?: string
  disabled?: boolean
  loading?: boolean
}

export function ChatInput({ onSend, placeholder, disabled, loading }: Props) {
  const [text, setText] = useState('')

  function submit() {
    if (!text.trim() || disabled) return
    onSend(text)
    setText('')
  }

  return (
    <div className='relative px-4 pt-2 pb-6 bg-white'>
      <div className={['space-y-4 transition-opacity', disabled ? 'opacity-60' : ''].join(' ')}>
        <div className='text-base font-medium text-gray-900'>Continue the discussion</div>
        <div className='flex items-center gap-2'>
          <Input
            value={text}
            placeholder={placeholder}
            disabled={disabled}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && submit()}
          />

          <Button disabled={disabled || !text.trim()} onClick={submit}>
            Send
          </Button>
        </div>
      </div>

      {loading && (
        <StatusMarker className='absolute -bottom-1 right-4' variant='pending'>
          Waiting for response…
        </StatusMarker>
      )}
    </div>
  )
}
