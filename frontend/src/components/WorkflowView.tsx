import { ChatInput } from '@/components/chat/ChatInput'
import { ChatMessageView } from '@/components/chat/ChatMessageView'
import { SolutionView } from '@/components/chat/SolutionView'
import { StepInput } from '@/components/chat/StepInput'
import { Button } from '@/components/ui/Button'
import { UIHistoryItemTypeEnum } from '@/types/enums'
import type { UIChatHistory, UICurrentStep, UIWorkflowData } from '@/types/fe'

interface WorkflowViewProps {
  workflowData: UIWorkflowData
  currentStep: UICurrentStep | null
  chatHistory: UIChatHistory
  loading: boolean
  confidence: number | null
  onAnswer(stepId: string, answer: string): void
  onSendChatMessage(message: string): void
  onSkip(): void
  onReset(): void
}

export function WorkflowView({
  workflowData,
  currentStep,
  chatHistory,
  loading,
  confidence,
  onAnswer,
  onSendChatMessage,
  onSkip,
  onReset,
}: WorkflowViewProps) {
  return (
    <div className='space-y-4 p-4 max-w-2xl mx-auto'>
      <h1 className='text-2xl font-bold'>
        Workflow: {workflowData.name} ({workflowData.domain})
      </h1>
      <p className='text-gray-700'>{workflowData.description}</p>
      <p className='text-sm text-gray-500'>Max steps: {workflowData.maxSteps}</p>
      <p className='text-sm text-blue-500'>Phase: {workflowData.phase}</p>

      <div className='flex flex-col gap-3'>
        {chatHistory.items.map((item, index) => {
          switch (item.type) {
            case UIHistoryItemTypeEnum.MESSAGE:
              return <ChatMessageView key={item.message.id} message={item.message} />
            case UIHistoryItemTypeEnum.SOLUTION:
              return <SolutionView key={index} solution={item.solution} />
            default:
              return null
          }
        })}
      </div>

      {currentStep && (
        <StepInput
          step={currentStep}
          onAnswer={(text) => onAnswer(currentStep.step_id, text)}
          onSkip={onSkip}
          workflowConfidence={confidence}
          disabled={loading}
        />
      )}

      {workflowData.phase === 'DISCUSSION' && (
        <ChatInput
          placeholder='Enter your message...'
          onSend={onSendChatMessage}
          disabled={loading}
        />
      )}

      <div className='flex justify-end items-center'>
        <Button onClick={onReset}>Start new workflow</Button>
      </div>
    </div>
  )
}
