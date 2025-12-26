import type { AnswerStepRequest, CreateWorkflowRequest, WorkflowResponse } from '@/types/workflow'

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
export async function createWorkflow(req: CreateWorkflowRequest): Promise<WorkflowResponse> {
  const res = await fetch(`${API_BASE_URL}/workflows`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowResponse>(res)
}

/**
 * Fetch workflow by ID
 */
export async function getWorkflow(workflowId: string): Promise<WorkflowResponse> {
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}`, {
    method: 'GET',
  })

  return handleResponse<WorkflowResponse>(res)
}

/**
 * Answer a clarification step
 */
export async function answerStep(
  workflowId: string,
  req: AnswerStepRequest,
): Promise<WorkflowResponse> {
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}/answer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  })

  return handleResponse<WorkflowResponse>(res)
}

/**
 * Skip to solution
 */
export async function skipToSolution(workflowId: string): Promise<WorkflowResponse> {
  const res = await fetch(`${API_BASE_URL}/workflows/${workflowId}/skip`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  return handleResponse<WorkflowResponse>(res)
}
