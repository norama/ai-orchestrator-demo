import { apiGet, apiPost } from '@/api/api'
import { API_CATALOG_URL } from '@/api/constants'
import type { CatalogResponse, CreateFromCatalogRequest, WorkflowDetailResponse } from '@/types/be'

/**
 * Create a new workflow from catalog item
 */
export async function createWorkflowFromCatalog(
  req: CreateFromCatalogRequest,
): Promise<WorkflowDetailResponse> {
  return apiPost<WorkflowDetailResponse>(`${API_CATALOG_URL}/workflows`, req)
}

/**
 * Fetch catalog
 */
export async function getCatalog(): Promise<CatalogResponse> {
  return apiGet<CatalogResponse>(API_CATALOG_URL)
}
