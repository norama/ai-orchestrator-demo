import { BottomFixedLayout } from '@/components/layout/BottomFixedLayout'
import { MainLayout } from '@/components/layout/MainLayout'
import { TimelineLayout } from '@/components/layout/TimelineLayout'
import { ChatInput } from '@/components/workflow/ChatInput'
import { ChatMessageView } from '@/components/workflow/ChatMessageView'
import { SolutionView } from '@/components/workflow/SolutionView'
import { StepInput } from '@/components/workflow/StepInput'
import { TicketView } from '@/components/workflow/TicketView'
import { WorkflowPhaseEnum } from '@/types/enums'
import type { UIChatHistory, UICurrentStep, UITicket, UIWorkflowData } from '@/types/fe'

interface WorkflowViewProps {
  ticket: UITicket
  workflowData: UIWorkflowData
  currentStep: UICurrentStep | null
  chatHistory: UIChatHistory
  loading: boolean
  confidence: number | null
  onAnswer(stepId: string, answer: string): void
  onSendChatMessage(message: string): void
  onSkip(): void
}

export function WorkflowView({
  ticket,
  workflowData,
  currentStep,
  chatHistory,
  loading,
  confidence,
  onAnswer,
  onSendChatMessage,
  onSkip,
}: WorkflowViewProps) {
  return (
    <MainLayout>
      <TimelineLayout>
        <h1 className='text-2xl font-bold'>
          Workflow: {workflowData.name} ({workflowData.domainType})
        </h1>
        <p className='text-gray-700'>{workflowData.description}</p>
        <p className='text-sm text-gray-500'>Max steps: {workflowData.maxSteps}</p>
        <p className='text-sm text-blue-500'>Phase: {workflowData.phase}</p>
        <TicketView ticket={ticket} />
        <div className='flex flex-col gap-3'>
          {chatHistory.items.map((item) => (
            <ChatMessageView key={item.message.id} message={item.message} />
          ))}
        </div>
      </TimelineLayout>

      <BottomFixedLayout>
        {workflowData.solution && (
          <SolutionView
            solution={workflowData.solution}
            updated={workflowData.solutionUpdated}
            domainType={workflowData.domainType}
          />
        )}

        {(currentStep || workflowData.phase === WorkflowPhaseEnum.DISCUSSION) && (
          <div className='my-3 border-t text-gray-300' />
        )}

        {currentStep && (
          <StepInput
            step={currentStep}
            onAnswer={(text) => onAnswer(currentStep.step_id, text)}
            onSkip={onSkip}
            workflowConfidence={confidence}
            disabled={loading}
          />
        )}

        {workflowData.phase === WorkflowPhaseEnum.DISCUSSION && (
          <ChatInput
            placeholder='Enter your message...'
            onSend={onSendChatMessage}
            disabled={loading}
          />
        )}
      </BottomFixedLayout>
    </MainLayout>
  )
}
