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
  reset(): void
}

export function useWorkflowHistoryController() {
  const [history, setHistory] = useState<UIWorkflowHistory | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function load(workflowId: string): Promise<void> {
    setLoading(true)
    setError(null)

    try {
      const res = await getWorkflowHistory(workflowId)
      setHistory(workflowHistoryToUI(res))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  function reset() {
    setHistory(null)
    setLoading(false)
    setError(null)
  }

  return {
    history,
    loading,
    error,
    load,
    reset,
  } as WorkflowHistoryController
}
