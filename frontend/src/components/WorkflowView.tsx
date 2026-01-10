import { BottomFixedLayout } from '@/components/layout/BottomFixedLayout'
import { MainLayout } from '@/components/layout/MainLayout'
import { TimelineLayout } from '@/components/layout/TimelineLayout'
import { ChatInput } from '@/components/workflow/ChatInput'
import { ChatMessageView } from '@/components/workflow/ChatMessageView'
import { SolutionView } from '@/components/workflow/SolutionView'
import { StepInput } from '@/components/workflow/StepInput'
import { WorkflowHeader } from '@/components/workflow/WorkflowHeader'
import { ChatRoleEnum, WorkflowPhaseEnum } from '@/types/enums'
import type { UIChatMessage, UITicket, UIWorkflowData, UIWorkflowState } from '@/types/fe'
import { useState } from 'react'

interface WorkflowViewProps {
  ticket: UITicket
  workflowData: UIWorkflowData
  workflowState: UIWorkflowState
  loading: boolean
  onAnswer: (stepId: string, answer: string) => Promise<void>
  onSendChatMessage: (message: string) => Promise<void>
  onSkip: () => Promise<void>
  isStreaming: boolean
  streamedText: string
}

export function WorkflowView({
  ticket,
  workflowData,
  workflowState,
  loading,
  onAnswer,
  onSendChatMessage,
  onSkip,
  isStreaming,
  streamedText,
}: WorkflowViewProps) {
  const [pendingMessages, setPendingMessages] = useState<UIChatMessage[]>([])
  const pendingIds = new Set(pendingMessages.map((m) => m.id))

  const handleSendStepAnswer = (message: string) => {
    const idUser = crypto.randomUUID()
    const idSystem = crypto.randomUUID()
    setPendingMessages((prev) => [
      ...prev,
      { id: idSystem, role: ChatRoleEnum.SYSTEM, content: workflowState.currentStep!.prompt },
      { id: idUser, role: ChatRoleEnum.USER, content: message },
    ])
    onAnswer(workflowState.currentStep!.stepId, message).finally(() => {
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

  const messages = [...workflowState.chat.items.map((item) => item.message), ...pendingMessages]

  return (
    <MainLayout>
      <TimelineLayout>
        <WorkflowHeader ticket={ticket} workflowData={workflowData} workflowState={workflowState} />
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
        {(workflowState.solution || isStreaming) && (
          <SolutionView
            solution={workflowState.solution}
            updated={workflowState.solutionUpdated}
            domainType={workflowData.domainType}
            isStreaming={isStreaming}
            streamedText={streamedText}
          />
        )}

        {(workflowState.currentStep || workflowState.phase === WorkflowPhaseEnum.DISCUSSION) && (
          <div className='my-3 border-t text-gray-300' />
        )}

        {workflowState.currentStep && (
          <StepInput
            step={workflowState.currentStep}
            onAnswer={handleSendStepAnswer}
            onSkip={onSkip}
            workflowConfidence={workflowState.workflowConfidence}
            loading={isStreaming || loading}
            disabled={isStreaming || loading}
          />
        )}

        {workflowState.phase === WorkflowPhaseEnum.DISCUSSION && (
          <ChatInput
            placeholder='Enter your message...'
            onSend={handleSendChatMessage}
            loading={isStreaming || loading}
            disabled={isStreaming || loading}
          />
        )}
      </BottomFixedLayout>
    </MainLayout>
  )
}
