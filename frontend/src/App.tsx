import { StartWorkflowForm } from '@/components/StartWorkflowForm'
import { Drawer } from '@/components/ui/Drawer'
import { WorkflowHistoryPanel } from '@/components/WorkflowHistoryPanel'
import { WorkflowListPanel } from '@/components/WorkflowListPanel'
import { WorkflowView } from '@/components/WorkflowView'
import { useCatalogController } from '@/data/catalogController'
import { useWorkflowController } from '@/data/workflowController'
import { useWorkflowHistoryController } from '@/data/workflowHistoryController'
import { useWorkflowListController } from '@/data/workflowListController'
import type { UICreateFromCatalog } from '@/types/fe'
import { WorkflowHeader } from '@/WorkflowHeader'
import { useCallback, useEffect, useRef, useState } from 'react'

function App() {
  const catalogController = useCatalogController()
  const listController = useWorkflowListController()
  const historyController = useWorkflowHistoryController()
  const controller = useWorkflowController()
  const hasBootstrappedRef = useRef(false)
  const [mobileWorkflowListOpen, setMobileWorkflowListOpen] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)

  const selectWorkflow = useCallback(
    (id: string) => {
      controller.load(id)
      historyController.load(id)
    },
    [controller, historyController],
  )

  // Auto-load the first workflow when the list is loaded
  useEffect(() => {
    if (hasBootstrappedRef.current) return
    if (!controller.workflowData && listController.items.length > 0 && !controller.loading) {
      hasBootstrappedRef.current = true
      selectWorkflow(listController.items[0].id)
    }
  }, [controller, listController.items, selectWorkflow])

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const withRefresh = <T extends (...args: any[]) => Promise<void>>(fn: T): T =>
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (async (...args: any[]) => {
      await fn(...args)
      await listController.refresh()
      const selectedWorkflowId = controller.workflowData?.id ?? null
      if (selectedWorkflowId) {
        await historyController.load(selectedWorkflowId)
      }
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
        historyOpen={historyOpen}
        onMobileOpenWorkflows={() => {
          setMobileWorkflowListOpen(true)
          setHistoryOpen(false)
        }}
        onToggleHistory={() => {
          setHistoryOpen((v) => !v)
          setMobileWorkflowListOpen(false)
        }}
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
            disabled={loading || controller.isPreviewingSnapshot}
          />
        </div>

        {/* Mobile drawer */}
        <Drawer
          open={mobileWorkflowListOpen}
          onClose={() => setMobileWorkflowListOpen(false)}
          className='lg:hidden'>
          <WorkflowListPanel
            items={listController.items}
            selectedId={selectedWorkflowId}
            onSelect={(id) => {
              selectWorkflow(id)
              setMobileWorkflowListOpen(false)
            }}
            onNew={() => {
              resetControllers()
              setMobileWorkflowListOpen(false)
            }}
          />
        </Drawer>

        {/* Main content area */}

        {/* Center + right */}
        <div className='flex flex-1 overflow-hidden'>
          <div
            className={[
              'flex-1 overflow-y-auto bg-gray-50 py-12',
              'transition-[margin] duration-300 ease-in-out',
              historyOpen ? 'lg:mr-80' : 'lg:mr-0',
            ].join(' ')}>
            <WorkflowView
              ticket={controller.ticket}
              workflowData={controller.workflowData}
              workflowState={controller.workflowState}
              loading={loading}
              onAnswer={withRefresh(controller.answerStream)}
              onSkip={withRefresh(controller.skipStream)}
              onSendChatMessage={withRefresh(controller.chat)}
              isStreaming={controller.isStreaming}
              streamedText={controller.streamedText}
            />
          </div>

          {/* Desktop History panel */}
          <div className='hidden lg:block relative h-[calc(100vh-3rem)]'>
            <div
              className={[
                'absolute top-0 right-0 h-full w-80',
                'border-l border-gray-300 bg-white',
                'transform transition-transform duration-300 ease-in-out',
                historyOpen ? 'translate-x-0' : 'translate-x-full',
              ].join(' ')}>
              {historyController.history && (
                <WorkflowHistoryPanel history={historyController.history} />
              )}
            </div>
          </div>
        </div>

        {/* Mobile History drawer */}
        <div className='lg:hidden'>
          <Drawer open={historyOpen} onClose={() => setHistoryOpen(false)} placement='top'>
            {historyController.history && (
              <WorkflowHistoryPanel history={historyController.history} />
            )}
          </Drawer>
        </div>
        {error && (
          <div className='fixed bottom-2 inset-x-0 text-center text-sm text-red-600'>{error}</div>
        )}
      </div>
    </>
  )
}

export default App
