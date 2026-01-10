import { getCatalog } from '@/api/catalog'
import { catalogResponseToItem } from '@/data/catalogProjector'
import type { UICatalogItem } from '@/types/fe'
import { useEffect, useState } from 'react'

export interface CatalogController {
  items: UICatalogItem[]
  loading: boolean
  error: string | null
  hasLoaded: boolean

  refresh(): Promise<void>
}

export function useCatalogController(): CatalogController {
  const [items, setItems] = useState<UICatalogItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasLoaded, setHasLoaded] = useState(false)

  async function refresh() {
    setLoading(true)
    try {
      const res = await getCatalog()
      setItems(res.items.map(catalogResponseToItem))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
      setHasLoaded(true)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  return { items, loading, error, refresh, hasLoaded }
}
