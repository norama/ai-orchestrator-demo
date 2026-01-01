import { StartWorkflowForm } from '@/components/StartWorkflowForm'
import { WorkflowListPanel } from '@/components/WorkflowListPanel'
import { WorkflowView } from '@/components/WorkflowView'
import { useCatalogController } from '@/data/catalogController'
import { useWorkflowController } from '@/data/workflowController'
import { useWorkflowListController } from '@/data/workflowListController'
import type { UICreateFromCatalog } from '@/types/fe'
import { useEffect, useRef } from 'react'

function App() {
  const catalogController = useCatalogController()
  const listController = useWorkflowListController()
  const controller = useWorkflowController()
  const hasBootstrappedRef = useRef(false)

  // Auto-load the first workflow when the list is loaded
  useEffect(() => {
    if (hasBootstrappedRef.current) return
    if (!controller.workflowData && listController.items.length > 0 && !controller.loading) {
      hasBootstrappedRef.current = true
      controller.load(listController.items[0].id)
    }
  }, [controller, listController.items])

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const withListRefresh = <T extends (...args: any[]) => Promise<void>>(fn: T): T =>
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (async (...args: any[]) => {
      await fn(...args)
      await listController.refresh()
    }) as T

  const loading = controller.loading || listController.loading || catalogController.loading
  const error = controller.error || listController.error || catalogController.error
  const selectedWorkflowId = controller.workflowData?.id ?? null

  const reset = () => {
    controller.reset()
  }

  const startNewWorkflow = (req: UICreateFromCatalog) => {
    controller.start(req).then(listController.refresh)
  }

  const selectWorkflow = (id: string) => {
    controller.reset()
    controller.load(id)
  }

  /* ---------- initial loading state ---------- */

  if (!listController.hasLoaded) {
    return <div className='p-6'>Loading workflows...</div>
  }

  /* ---------- initial screen ---------- */

  if (!controller.chatHistory || !controller.workflowData || !controller.ticket) {
    return (
      <StartWorkflowForm
        loading={loading}
        error={error}
        catalogItems={catalogController.items}
        onStart={startNewWorkflow}
      />
    )
  }

  /* ---------- workflow screen ---------- */

  return (
    <div className='flex h-screen'>
      <WorkflowListPanel
        items={listController.items}
        selectedId={selectedWorkflowId}
        onSelect={selectWorkflow}
        onNew={controller.reset}
      />

      <div className='flex-1 overflow-y-auto bg-gray-50 py-8'>
        <WorkflowView
          ticket={controller.ticket}
          workflowData={controller.workflowData}
          currentStep={controller.currentStep}
          chatHistory={controller.chatHistory}
          loading={loading}
          confidence={controller.workflowConfidence}
          onAnswer={withListRefresh(controller.answer)}
          onSkip={withListRefresh(controller.skip)}
          onSendChatMessage={withListRefresh(controller.chat)}
          onReset={reset}
        />

        {error && <div className='mt-4 text-center text-sm text-red-600'>{error}</div>}
      </div>
    </div>
  )
}

export default App
