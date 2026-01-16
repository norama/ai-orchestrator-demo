import { apiGet, apiPost } from '@/api/api'
import { API_WORKFLOWS_URL } from '@/api/constants'
import type {
  AnswerStepRequest,
  ChatMessageRequest,
  CreateWorkflowRequest,
  WorkflowDetailResponse,
  WorkflowListResponse,
} from '@/types/be'

/* ---------- API functions ---------- */

/**
 * Create a new workflow
 */
export async function createWorkflow(req: CreateWorkflowRequest): Promise<WorkflowDetailResponse> {
  return apiPost<WorkflowDetailResponse>(API_WORKFLOWS_URL, req)
}

/**
 * Fetch workflow by ID
 */
export async function getWorkflow(workflowId: string): Promise<WorkflowDetailResponse> {
  return apiGet<WorkflowDetailResponse>(`${API_WORKFLOWS_URL}/${workflowId}`)
}

/**
 * Fetch workflows
 */
export async function getWorkflows(): Promise<WorkflowListResponse> {
  return apiGet<WorkflowListResponse>(API_WORKFLOWS_URL)
}

/**
 * Answer a clarification step
 */
export async function answerStep(
  workflowId: string,
  req: AnswerStepRequest,
): Promise<WorkflowDetailResponse> {
  return apiPost<WorkflowDetailResponse>(`${API_WORKFLOWS_URL}/${workflowId}/answer`, req)
}

/**
 * Skip to solution
 */
export async function skipToSolution(workflowId: string): Promise<WorkflowDetailResponse> {
  return apiPost<WorkflowDetailResponse>(`${API_WORKFLOWS_URL}/${workflowId}/skip`)
}

/**
 * Send chat message
 */
export async function sendChatMessage(
  workflowId: string,
  req: ChatMessageRequest,
): Promise<WorkflowDetailResponse> {
  return apiPost<WorkflowDetailResponse>(`${API_WORKFLOWS_URL}/${workflowId}/chat`, req)
}
