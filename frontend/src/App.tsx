import { ResetDemoButton } from '@/components/ResetDemoButton'
import { StartWorkflowForm } from '@/components/StartWorkflowForm'
import { Drawer } from '@/components/ui/Drawer'
import { WorkflowHeader } from '@/components/WorkflowHeader'
import { WorkflowHistoryPanel } from '@/components/WorkflowHistoryPanel'
import { WorkflowListPanel } from '@/components/WorkflowListPanel'
import { WorkflowView } from '@/components/WorkflowView'
import { useCatalogController } from '@/data/catalogController'
import { useWorkflowController } from '@/data/workflowController'
import { useWorkflowHistoryController } from '@/data/workflowHistoryController'
import { useWorkflowListController } from '@/data/workflowListController'
import type { UICreateFromCatalog, UIWorkflowListItem } from '@/types/fe'
import { useCallback, useEffect, useRef, useState } from 'react'

type AppMode = 'start' | 'workflow'

function App() {
  const catalogController = useCatalogController()
  const listController = useWorkflowListController()
  const historyController = useWorkflowHistoryController()
  const controller = useWorkflowController()
  const hasBootstrappedRef = useRef(false)
  const [mobileWorkflowListOpen, setMobileWorkflowListOpen] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [appMode, setAppMode] = useState<AppMode>('start')

  const selectWorkflow = useCallback(
    async (id: string, snapshotId: string | null = null) => {
      await controller.load(id, snapshotId)
      await historyController.load(id)
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
    historyController.loading ||
    controller.isStreaming
  const error =
    controller.error || listController.error || catalogController.error || historyController.error
  const selectedWorkflowId = controller.workflowData?.id ?? null
  const previewing = controller.previewingSnapshotId !== null

  const startNewWorkflow = async (req: UICreateFromCatalog) => {
    const workflowId = await controller.start(req)
    if (workflowId) {
      await listController.refresh()
      await historyController.load(workflowId)
    } else {
      historyController.reset()
    }
    setAppMode('workflow')
  }

  const branchFromHistory = async () => {
    const newWorkflowId = await controller.branch()
    if (newWorkflowId) {
      await listController.refresh()
      await historyController.load(newWorkflowId)
      setHistoryOpen(false)
    } else {
      historyController.reset()
    }
  }

  const reset = () => {
    setAppMode('start')
    controller.reset()
    historyController.reset()
    setHistoryOpen(false)
  }

  async function selectParentSnapshot(item: UIWorkflowListItem) {
    if (!item.parentId || !item.parentSnapshotId) return

    await selectWorkflow(item.parentId, item.parentSnapshotId)

    setHistoryOpen(true)
  }

  /* ---------- initial loading state ---------- */

  if (!listController.hasLoaded) {
    return <div className='p-6'>Loading workflows...</div>
  }

  /* ---------- initial screen ---------- */

  if (appMode === 'start') {
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
        isPreview={controller.previewingSnapshotId !== null}
        onMobileOpenWorkflows={() => {
          setMobileWorkflowListOpen(true)
          setHistoryOpen(false)
        }}
        onToggleHistory={() => {
          setHistoryOpen((v) => !v)
          setMobileWorkflowListOpen(false)
        }}
        onNewWorkflow={reset}
        onBackToLive={controller.refresh}
        onBranch={branchFromHistory}
        disabled={loading}
      />
      {previewing && <div className='pointer-events-none absolute inset-0 z-10 bg-stone-200/20' />}

      {/* Global layout wrapper */}
      <div className='flex h-screen pt-16'>
        {/* Desktop rail */}
        <div className='hidden lg:block h-[calc(100vh-4rem)]'>
          <WorkflowListPanel
            items={listController.items}
            selectedId={selectedWorkflowId}
            onSelect={selectWorkflow}
            onNew={reset}
            onSelectParent={selectParentSnapshot}
            disabled={loading || controller.previewingSnapshotId !== null}
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
              reset()
              setMobileWorkflowListOpen(false)
            }}
            onSelectParent={async (item: UIWorkflowListItem) => {
              await selectParentSnapshot(item)
              setMobileWorkflowListOpen(false)
            }}
            disabled={loading || controller.previewingSnapshotId !== null}
          />
        </Drawer>

        {/* Main content area */}

        {/* Center + right */}
        <div className='flex flex-1 overflow-hidden'>
          <div
            className={[
              'flex flex-col flex-1 min-h-0 bg-gray-50',
              'transition-[margin,background-color] duration-300 ease-in-out',
              historyOpen ? 'lg:mr-80' : 'lg:mr-0',
            ].join(' ')}>
            <div className='flex-1 min-h-0 overflow-y-auto pt-4'>
              {controller.ticket && controller.workflowData && controller.workflowState && (
                <WorkflowView
                  ticket={controller.ticket}
                  workflowData={controller.workflowData}
                  workflowState={controller.workflowState}
                  loading={loading}
                  previewing={previewing}
                  onAnswer={withRefresh(controller.answerStream)}
                  onSkip={withRefresh(controller.skipStream)}
                  onSendChatMessage={withRefresh(controller.chat)}
                  isStreaming={controller.isStreaming}
                  streamedText={controller.streamedText}
                />
              )}
            </div>
            <div className='h-16 px-6 flex items-center border-t border-gray-200 bg-gray-50'>
              {error && (
                <div className='mx-auto max-w-3xl rounded-md bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-2 text-center'>
                  {error}
                </div>
              )}
              <ResetDemoButton />
            </div>
          </div>

          {/* Desktop History panel */}
          <div className='hidden lg:block relative h-[calc(100vh-4rem)]'>
            <div
              className={[
                'absolute top-0 right-0 h-full w-80',
                'border-l border-gray-300 bg-white',
                'transform transition-transform duration-300 ease-in-out',
                historyOpen ? 'translate-x-0' : 'translate-x-full',
              ].join(' ')}>
              {historyController.history && (
                <WorkflowHistoryPanel
                  history={historyController.history}
                  previewingSnapshotId={controller.previewingSnapshotId}
                  onPreviewSnapshot={controller.previewSnapshot}
                  onBranch={branchFromHistory}
                  disabled={loading}
                />
              )}
            </div>
          </div>
        </div>

        {/* Mobile History drawer */}
        <div className='lg:hidden top-16 h-[calc(100vh-4rem)]'>
          <Drawer open={historyOpen} onClose={() => setHistoryOpen(false)} placement='top'>
            {historyController.history && (
              <WorkflowHistoryPanel
                history={historyController.history}
                previewingSnapshotId={controller.previewingSnapshotId}
                onPreviewSnapshot={controller.previewSnapshot}
                onBranch={branchFromHistory}
                disabled={loading}
              />
            )}
          </Drawer>
        </div>
      </div>
    </>
  )
}

export default App
