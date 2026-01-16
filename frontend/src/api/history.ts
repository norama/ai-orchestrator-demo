import { apiGet, apiPost } from '@/api/api'
import { API_WORKFLOWS_URL } from '@/api/constants'
import type {
  SnapshotDetailResponse,
  WorkflowDetailResponse,
  WorkflowHistoryResponse,
} from '@/types/be'

/**
 * Fetch snapshots for a workflow
 */
export async function getWorkflowHistory(workflowId: string): Promise<WorkflowHistoryResponse> {
  return apiGet<WorkflowHistoryResponse>(`${API_WORKFLOWS_URL}/${workflowId}/history`)
}

/**
 * Fetch snapshot by ID
 */
export async function getSnapshot(
  workflowId: string,
  snapshotId: string,
): Promise<SnapshotDetailResponse> {
  return apiGet<SnapshotDetailResponse>(
    `${API_WORKFLOWS_URL}/${workflowId}/snapshots/${snapshotId}`,
  )
}

/**
 * Create a new workflow from a snapshot (branching)
 */
export async function branchFromSnapshot(
  workflowId: string,
  snapshotId: string,
): Promise<WorkflowDetailResponse> {
  return apiPost<WorkflowDetailResponse>(
    `${API_WORKFLOWS_URL}/${workflowId}/snapshots/${snapshotId}/branch`,
  )
}
