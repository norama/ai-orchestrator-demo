import { BottomFixedLayout } from '@/components/layout/BottomFixedLayout'
import { MainLayout } from '@/components/layout/MainLayout'
import { TimelineLayout } from '@/components/layout/TimelineLayout'
import { ChatInput } from '@/components/workflow/ChatInput'
import { ChatMessageView } from '@/components/workflow/ChatMessageView'
import { SolutionView } from '@/components/workflow/SolutionView'
import { StepInput } from '@/components/workflow/StepInput'
import { WorkflowHeader } from '@/components/workflow/WorkflowHeader'
import { ChatRoleEnum, WorkflowPhaseEnum } from '@/types/enums'
import type {
  UIChatHistory,
  UIChatMessage,
  UICurrentStep,
  UITicket,
  UIWorkflowData,
} from '@/types/fe'
import { useState } from 'react'

interface WorkflowViewProps {
  ticket: UITicket
  workflowData: UIWorkflowData
  currentStep: UICurrentStep | null
  chatHistory: UIChatHistory
  loading: boolean
  confidence: number | null
  onAnswer: (stepId: string, answer: string) => Promise<void>
  onSendChatMessage: (message: string) => Promise<void>
  onSkip: () => Promise<void>
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
  const [pendingMessages, setPendingMessages] = useState<UIChatMessage[]>([])
  const pendingIds = new Set(pendingMessages.map((m) => m.id))

  const handleSendStepAnswer = (message: string) => {
    const idUser = crypto.randomUUID()
    const idSystem = crypto.randomUUID()
    setPendingMessages((prev) => [
      ...prev,
      { id: idSystem, role: ChatRoleEnum.SYSTEM, content: currentStep!.prompt },
      { id: idUser, role: ChatRoleEnum.USER, content: message },
    ])
    onAnswer(currentStep!.stepId, message).finally(() => {
      setPendingMessages((prev) => prev.filter((msg) => msg.id !== idUser && msg.id !== idSystem))
    })
  }

  const handleSendChatMessage = (message: string) => {
    const idUser = crypto.randomUUID()
    setPendingMessages((prev) => [
      ...prev,
      { id: idUser, role: ChatRoleEnum.USER, content: message },
    ])
    onSendChatMessage(message).finally(() => {
      setPendingMessages((prev) => prev.filter((msg) => msg.id !== idUser))
    })
  }

  const messages = [...chatHistory.items.map((item) => item.message), ...pendingMessages]

  return (
    <MainLayout>
      <TimelineLayout>
        <WorkflowHeader workflow={workflowData} ticket={ticket} />
        <div className='flex flex-col gap-3'>
          {messages.map((message) => (
            <ChatMessageView
              key={message.id}
              message={message}
              pending={message.role === ChatRoleEnum.USER && pendingIds.has(message.id)}
            />
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
            onAnswer={handleSendStepAnswer}
            onSkip={onSkip}
            workflowConfidence={confidence}
            disabled={loading}
          />
        )}

        {workflowData.phase === WorkflowPhaseEnum.DISCUSSION && (
          <ChatInput
            placeholder='Enter your message...'
            onSend={handleSendChatMessage}
            disabled={loading}
          />
        )}
      </BottomFixedLayout>
    </MainLayout>
  )
}
