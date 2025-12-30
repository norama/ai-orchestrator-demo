import { StartWorkflowForm } from '@/components/StartWorkflowForm'
import { WorkflowListPanel } from '@/components/WorkflowListPanel'
import { WorkflowView } from '@/components/WorkflowView'
import { useWorkflowController } from '@/data/workflowController'
import { useWorkflowListController } from '@/data/workflowListController'
import type { UIWorkflowCreateForm } from '@/types/fe'
import { useState } from 'react'

function App() {
  const listController = useWorkflowListController()
  const controller = useWorkflowController()

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const withListRefresh = <T extends (...args: any[]) => Promise<void>>(fn: T): T =>
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (async (...args: any[]) => {
      await fn(...args)
      await listController.refresh()
    }) as T

  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null)

  const reset = () => {
    //setSelectedWorkflowId(null)
    controller.reset()
  }

  const startNewWorkflow = (req: UIWorkflowCreateForm) => {
    controller.start(req).then(() => listController.refresh())
  }

  const selectWorkflow = (id: string) => {
    controller.reset()
    controller.load(id)
    setSelectedWorkflowId(id)
  }

  /* ---------- initial screen ---------- */

  if (!controller.chatHistory || !controller.workflowData || !controller.ticket) {
    return (
      <StartWorkflowForm
        loading={controller.loading}
        error={controller.error}
        onStart={startNewWorkflow}
      />
    )
  }

  /* ---------- workflow screen ---------- */

  return (
    <div className='flex h-screen'>
      <WorkflowListPanel
        workflows={listController.items}
        selectedId={selectedWorkflowId}
        onSelect={selectWorkflow}
        onNew={() => {
          setSelectedWorkflowId(null)
          controller.reset()
        }}
      />

      <div className='flex-1 overflow-y-auto bg-gray-50 py-8'>
        <WorkflowView
          ticket={controller.ticket}
          workflowData={controller.workflowData}
          currentStep={controller.currentStep}
          chatHistory={controller.chatHistory}
          loading={controller.loading}
          confidence={controller.workflowConfidence}
          onAnswer={withListRefresh(controller.answer)}
          onSkip={withListRefresh(controller.skip)}
          onSendChatMessage={withListRefresh(controller.chat)}
          onReset={reset}
        />

        {controller.error && (
          <div className='mt-4 text-center text-sm text-red-600'>{controller.error}</div>
        )}
      </div>
    </div>
  )
}

export default App
