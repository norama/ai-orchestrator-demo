import { API_CATALOG_URL } from '@/api/constants'
import { handleResponse } from '@/api/utils'
import type { CatalogResponse, CreateFromCatalogRequest, WorkflowDetailResponse } from '@/types/be'

/**
 * Create a new workflow from catalog item
 */
export async function createWorkflowFromCatalog(
  req: CreateFromCatalogRequest,
): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_CATALOG_URL}/workflows`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowDetailResponse>(res)
}

/**
 * Fetch catalog
 */
export async function getCatalog(): Promise<CatalogResponse> {
  const res = await fetch(API_CATALOG_URL, {
    method: 'GET',
  })

  return handleResponse<CatalogResponse>(res)
}
