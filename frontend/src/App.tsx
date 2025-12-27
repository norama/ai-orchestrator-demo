import { WorkflowView } from '@/components/WorkflowView'
import { Button } from '@/components/ui/Button'
import { useWorkflowController } from '@/data/workflowController'

function App() {
  const controller = useWorkflowController()

  /* ---------- initial screen ---------- */

  if (!controller.chatHistory || !controller.workflowData) {
    return (
      <div className='min-h-screen flex items-center justify-center bg-gray-50'>
        <div className='space-y-4 p-6 bg-white rounded shadow max-w-sm w-full text-center'>
          <h1 className='text-xl font-semibold'>AI Orchestrator Demo</h1>

          <p className='text-sm text-gray-600'>Choose a demo workflow to start</p>

          <div className='flex gap-4 justify-center'>
            <Button onClick={() => controller.start('PRINTER')} disabled={controller.loading}>
              Printer demo
            </Button>

            <Button onClick={() => controller.start('PARROT')} disabled={controller.loading}>
              Parrot demo
            </Button>
          </div>

          {controller.error && <div className='text-sm text-red-600'>{controller.error}</div>}
        </div>
      </div>
    )
  }

  /* ---------- workflow screen ---------- */

  return (
    <div className='min-h-screen bg-gray-50 py-8'>
      <WorkflowView
        workflowData={controller.workflowData}
        currentStep={controller.currentStep}
        chatHistory={controller.chatHistory}
        loading={controller.loading}
        confidence={controller.workflowConfidence}
        onAnswer={controller.answer}
        onSkip={controller.skip}
        onSendChatMessage={controller.chat}
        onReset={controller.reset}
      />

      {controller.error && (
        <div className='mt-4 text-center text-sm text-red-600'>{controller.error}</div>
      )}
    </div>
  )
}

export default App
