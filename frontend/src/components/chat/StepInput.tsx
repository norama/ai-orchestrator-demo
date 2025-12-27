import { Confidence } from '@/components/chat/Confidence'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import type { UICurrentStep } from '@/types/fe'
import { useState } from 'react'

interface StepInputProps {
  step: UICurrentStep
  onAnswer(answer: string): void
  onSkip(): void
  workflowConfidence: number | null
  disabled?: boolean
}

export function StepInput({
  step,
  onAnswer,
  onSkip,
  workflowConfidence,
  disabled = false,
}: StepInputProps) {
  const [value, setValue] = useState('')

  function submit() {
    if (!value.trim()) return
    onAnswer(value.trim())
    setValue('')
  }

  return (
    <div className='space-y-4 p-4 border rounded bg-white'>
      {/* Prompt */}
      <div className='text-lg font-medium'>{step.prompt}</div>

      {/* Input */}
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder='Type your answer…'
        disabled={disabled}
        onKeyDown={(e) => {
          if (e.key === 'Enter') submit()
        }}
      />
      <Confidence label='Workflow confidence' confidence={workflowConfidence} />

      {/* Actions */}
      <div className='flex gap-2'>
        <Button onClick={submit} disabled={disabled || !value.trim()}>
          Submit
        </Button>

        <Button onClick={onSkip} disabled={disabled}>
          Skip to solution
        </Button>
      </div>
    </div>
  )
}
