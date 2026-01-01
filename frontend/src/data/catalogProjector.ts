import type { CatalogItemResponse } from '@/types/be'
import type { UICatalogItem } from '@/types/fe'

export function catalogResponseToItem(r: CatalogItemResponse): UICatalogItem {
  return {
    id: r.id,
    name: r.name,
    description: r.description,
    domainType: r.domain_type,
    category: r.category ?? undefined,
  }
}
