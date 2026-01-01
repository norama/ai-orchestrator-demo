import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useState } from 'react'

interface Props {
  disabled?: boolean
  onSend: (text: string) => void
  placeholder?: string
}

export function ChatInput({ disabled, onSend, placeholder }: Props) {
  const [text, setText] = useState('')

  function submit() {
    if (!text.trim()) return
    onSend(text)
    setText('')
  }

  return (
    <div className='flex gap-2 p-3 border-t'>
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
  )
}
