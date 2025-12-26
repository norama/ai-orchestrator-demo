import { StepInput } from '@/components/StepInput'
import { Button } from '@/components/ui/Button'
import type { WorkflowState } from '@/types/workflow'

interface WorkflowViewProps {
  workflow: WorkflowState
  loading: boolean
  confidence: number | null
  onAnswer(stepId: string, answer: string): void
  onSkip(): void
  onReset(): void
}

export function WorkflowView({
  workflow,
  loading,
  confidence,
  onAnswer,
  onSkip,
  onReset,
}: WorkflowViewProps) {
  const openStep = workflow.steps.find((step) => step.answer === null)

  /* ---------- solution view ---------- */

  if (workflow.solution) {
    return (
      <div className='space-y-4 p-4 max-w-2xl mx-auto'>
        <h2 className='text-xl font-semibold'>Solution</h2>

        <pre className='whitespace-pre-wrap bg-gray-100 p-4 rounded'>
          {workflow.solution.content}
        </pre>

        <div className='flex justify-between items-center'>
          {confidence !== null && (
            <div className='text-sm text-gray-600'>Confidence: {Math.round(confidence * 100)}%</div>
          )}

          <Button onClick={onReset}>Start new workflow</Button>
        </div>
      </div>
    )
  }

  /* ---------- clarification input ---------- */

  if (openStep) {
    return (
      <div className='max-w-xl mx-auto'>
        <StepInput
          step={openStep}
          onAnswer={(answer) => onAnswer(openStep.id, answer)}
          onSkip={onSkip}
          disabled={loading}
        />
      </div>
    )
  }

  /* ---------- transitional / waiting ---------- */

  return (
    <div className='p-4 text-center text-gray-500'>
      <p>Processing…</p>
    </div>
  )
}
