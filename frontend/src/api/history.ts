import { API_WORKFLOWS_URL } from '@/api/constants'
import { handleResponse } from '@/api/utils'
import type {
  SnapshotDetailResponse,
  WorkflowDetailResponse,
  WorkflowHistoryResponse,
} from '@/types/be'

/**
 * Fetch snapshots for a workflow
 */
export async function getWorkflowHistory(workflowId: string): Promise<WorkflowHistoryResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/history`, {
    method: 'GET',
  })

  return handleResponse<WorkflowHistoryResponse>(res)
}

/**
 * Fetch snapshot by ID
 */
export async function getSnapshot(
  workflowId: string,
  snapshotId: string,
): Promise<SnapshotDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/snapshots/${snapshotId}`, {
    method: 'GET',
  })

  return handleResponse<SnapshotDetailResponse>(res)
}

/**
 * Create a new workflow from a snapshot (branching)
 */
export async function branchFromSnapshot(
  workflowId: string,
  snapshotId: string,
): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/snapshots/${snapshotId}/branch`, {
    method: 'POST',
  })

  return handleResponse<WorkflowDetailResponse>(res)
}
