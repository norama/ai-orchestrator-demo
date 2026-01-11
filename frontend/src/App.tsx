import { StartWorkflowForm } from '@/components/StartWorkflowForm'
import { Drawer } from '@/components/ui/Drawer'
import { WorkflowListPanel } from '@/components/WorkflowListPanel'
import { WorkflowView } from '@/components/WorkflowView'
import { useCatalogController } from '@/data/catalogController'
import { useWorkflowController } from '@/data/workflowController'
import { useWorkflowHistoryController } from '@/data/workflowHistoryController'
import { useWorkflowListController } from '@/data/workflowListController'
import type { UICreateFromCatalog } from '@/types/fe'
import { WorkflowHeader } from '@/WorkflowHeader'
import { useEffect, useRef, useState } from 'react'

function App() {
  const catalogController = useCatalogController()
  const listController = useWorkflowListController()
  const historyController = useWorkflowHistoryController()
  const controller = useWorkflowController()
  const hasBootstrappedRef = useRef(false)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)

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

  const loading =
    controller.loading ||
    listController.loading ||
    catalogController.loading ||
    historyController.loading
  const error =
    controller.error || listController.error || catalogController.error || historyController.error
  const selectedWorkflowId = controller.workflowData?.id ?? null

  const startNewWorkflow = async (req: UICreateFromCatalog) => {
    const workflowId = await controller.start(req)
    if (workflowId) {
      await listController.refresh()
      await historyController.load(workflowId)
    } else {
      historyController.reset()
    }
  }

  /*
  const branchFromHistory = async () => {
    const newWorkflowId = await controller.branch()
    if (newWorkflowId) {
      await listController.refresh()
      await historyController.load(newWorkflowId)
    } else {
      historyController.reset()
    }
  }
  */

  const selectWorkflow = (id: string) => {
    controller.load(id)
    historyController.load(id)
  }

  const resetControllers = () => {
    controller.reset()
    historyController.reset()
  }

  /* ---------- initial loading state ---------- */

  if (!listController.hasLoaded) {
    return <div className='p-6'>Loading workflows...</div>
  }

  /* ---------- initial screen ---------- */

  if (!controller.workflowData || !controller.ticket || !controller.workflowState) {
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
    <>
      {/* Fixed header */}
      <WorkflowHeader
        workflowName={controller.workflowData?.name ?? null}
        historyCount={historyController.history?.events.length ?? null}
        isHistoryOpen={historyOpen}
        onOpenWorkflows={() => setDrawerOpen(true)}
        onToggleHistory={() => setHistoryOpen((v) => !v)}
      />

      {/* Global layout wrapper */}
      <div className='flex h-screen pt-12'>
        {/* Desktop rail */}
        <div className='hidden lg:block h-[calc(100vh-3rem)]'>
          <WorkflowListPanel
            items={listController.items}
            selectedId={selectedWorkflowId}
            onSelect={selectWorkflow}
            onNew={resetControllers}
          />
        </div>

        {/* Mobile drawer */}
        <Drawer open={drawerOpen} onClose={() => setDrawerOpen(false)} className='lg:hidden'>
          <WorkflowListPanel
            items={listController.items}
            selectedId={selectedWorkflowId}
            onSelect={(id) => {
              selectWorkflow(id)
              setDrawerOpen(false)
            }}
            onNew={() => {
              resetControllers()
              setDrawerOpen(false)
            }}
          />
        </Drawer>

        <div className='flex-1 overflow-y-auto bg-gray-50 py-10'>
          <WorkflowView
            ticket={controller.ticket}
            workflowData={controller.workflowData}
            workflowState={controller.workflowState}
            loading={loading}
            onAnswer={withListRefresh(controller.answerStream)}
            onSkip={withListRefresh(controller.skipStream)}
            onSendChatMessage={withListRefresh(controller.chat)}
            isStreaming={controller.isStreaming}
            streamedText={controller.streamedText}
          />

          {error && <div className='mt-4 text-center text-sm text-red-600'>{error}</div>}
        </div>
      </div>
    </>
  )
}

export default App
