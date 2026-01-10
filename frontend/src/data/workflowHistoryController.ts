import { getWorkflowHistory } from '@/api/history'
import { workflowHistoryToUI } from '@/data/workflowHistoryProjector'
import type { UIWorkflowHistory } from '@/types/fe'
import { useState } from 'react'

export interface WorkflowHistoryController {
  history: UIWorkflowHistory | null
  loading: boolean
  error: string | null

  selectedSnapshotId: string | null

  load(workflowId: string): Promise<void>
  selectSnapshot(snapshotId: string): void
  clearSelection(): void
  reset(): void
}

export function useWorkflowHistoryController() {
  const [history, setHistory] = useState<UIWorkflowHistory | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedSnapshotId, setSelectedSnapshotId] = useState<string | null>(null)

  async function load(workflowId: string): Promise<void> {
    setLoading(true)
    setError(null)
    setSelectedSnapshotId(null)

    try {
      const res = await getWorkflowHistory(workflowId)
      setHistory(workflowHistoryToUI(res))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  function selectSnapshot(snapshotId: string) {
    setSelectedSnapshotId(snapshotId)
  }

  function clearSelection() {
    setSelectedSnapshotId(null)
  }

  function reset() {
    setHistory(null)
    setLoading(false)
    setError(null)
    setSelectedSnapshotId(null)
  }

  return {
    history,
    loading,
    error,
    selectedSnapshotId,
    load,
    selectSnapshot,
    clearSelection,
    reset,
  } as WorkflowHistoryController
}
