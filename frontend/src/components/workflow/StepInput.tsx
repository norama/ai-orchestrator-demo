import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { StatusMarker } from '@/components/ui/StatusMarker'
import { Confidence } from '@/components/workflow/Confidence'
import type { UICurrentStep } from '@/types/fe'
import { useState } from 'react'

interface StepInputProps {
  step: UICurrentStep
  onAnswer(answer: string): void
  onSkip(): void
  workflowConfidence: number | null
  disabled?: boolean
  loading?: boolean
}

export function StepInput({
  step,
  onAnswer,
  onSkip,
  workflowConfidence,
  disabled = false,
  loading = false,
}: StepInputProps) {
  const [value, setValue] = useState('')

  function submit() {
    if (!value.trim() || disabled) return
    onAnswer(value.trim())
    setValue('')
  }

  return (
    <div className='relative px-4 py-5 bg-white'>
      {/* Main interactive content */}
      <div className={['space-y-4 transition-opacity', disabled ? 'opacity-80' : ''].join(' ')}>
        {/* Prompt */}
        <div className='text-base font-medium text-gray-900'>{step.prompt}</div>

        {/* Input */}
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder='Type your answer…'
          disabled={disabled}
          onKeyDown={(e) => e.key === 'Enter' && submit()}
        />

        {/* Confidence */}
        {workflowConfidence !== null && (
          <Confidence label='Workflow confidence' confidence={workflowConfidence} />
        )}

        {/* Actions */}
        <div className='flex items-center gap-3'>
          <Button onClick={submit} disabled={disabled || !value.trim()}>
            Submit
          </Button>

          <Button variant='ghost' onClick={onSkip} disabled={disabled}>
            Skip to solution
          </Button>
        </div>
      </div>

      {/* Status layer (never dimmed) */}
      {loading && (
        <div className='absolute bottom-3 right-4'>
          <StatusMarker variant='pending'>Processing…</StatusMarker>
        </div>
      )}
    </div>
  )
}
