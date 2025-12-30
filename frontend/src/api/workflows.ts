import type {
  AnswerStepRequest,
  ChatMessageRequest,
  CreateWorkflowRequest,
  WorkflowDetailResponse,
  WorkflowListResponse,
} from '@/types/be'

const API_BASE_URL = 'http://localhost:8000'

/* ---------- helpers ---------- */

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  const data = await res.json()
  return data as T
}

/* ---------- API functions ---------- */

/**
 * Create a new workflow
 */
export async function createWorkflow(req: CreateWorkflowRequest): Promise<WorkflowDetailResponse> {
  const res = await fetch(`${API_BASE_URL}/workflows`, {
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
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}`, {
    method: 'GET',
  })

  return handleResponse<WorkflowDetailResponse>(res)
}

/**
 * Fetch workflows
 */
export async function getWorkflows(): Promise<WorkflowListResponse> {
  const res = await fetch(`${API_BASE_URL}/workflows`, {
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
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}/answer`, {
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
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}/skip`, {
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
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowDetailResponse>(res)
}
