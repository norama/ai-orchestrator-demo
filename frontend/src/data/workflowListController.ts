import { getWorkflows } from '@/api/workflows'
import { workflowToListItem } from '@/data/workflowListProjector'
import type { UIWorkflowListItem } from '@/types/fe'
import { useEffect, useState } from 'react'

export function useWorkflowListController() {
  const [items, setItems] = useState<UIWorkflowListItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    setLoading(true)
    try {
      const res = await getWorkflows()
      setItems(res.workflows.map(workflowToListItem))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  return { items, loading, error, refresh }
}
