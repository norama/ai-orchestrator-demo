import { API_WORKFLOWS_URL } from '@/api/constants'
import { handleResponse } from '@/api/utils'
import type {
  AnswerStepRequest,
  ChatMessageRequest,
  CreateWorkflowRequest,
  SnapshotDetailResponse,
  WorkflowDetailResponse,
  WorkflowHistoryResponse,
  WorkflowListResponse,
} from '@/types/be'

/* ---------- API functions ---------- */

/**
 * Create a new workflow
 */
export async function createWorkflow(req: CreateWorkflowRequest): Promise<WorkflowDetailResponse> {
  const res = await fetch(API_WORKFLOWS_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowDetailResponse>(res)
}

/**
 * Fetch workflow by ID
 */
export async function getWorkflow(workflowId: string): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}`, {
    method: 'GET',
  })

  return handleResponse<WorkflowDetailResponse>(res)
}

/**
 * Fetch workflows
 */
export async function getWorkflows(): Promise<WorkflowListResponse> {
  const res = await fetch(API_WORKFLOWS_URL, {
    method: 'GET',
  })

  return handleResponse<WorkflowListResponse>(res)
}

/**
 * Answer a clarification step
 */
export async function answerStep(
  workflowId: string,
  req: AnswerStepRequest,
): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/answer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowDetailResponse>(res)
}

/**
 * Skip to solution
 */
export async function skipToSolution(workflowId: string): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/skip`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  return handleResponse<WorkflowDetailResponse>(res)
}

/**
 * Send chat message
 */
export async function sendChatMessage(
  workflowId: string,
  req: ChatMessageRequest,
): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowDetailResponse>(res)
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
 * Fetch snapshots for a workflow
 */
export async function getWorkflowHistory(workflowId: string): Promise<WorkflowHistoryResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/history`, {
    method: 'GET',
  })

  return handleResponse<WorkflowHistoryResponse>(res)
}

/**
 * Create a new workflow
 */
export async function branchWorkflow(
  workflowId: string,
  snapshotId: string,
): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_WORKFLOWS_URL}/${workflowId}/snapshots/${snapshotId}/branch`, {
    method: 'POST',
  })

  return handleResponse<WorkflowDetailResponse>(res)
}
