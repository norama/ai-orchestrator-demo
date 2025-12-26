export type WorkflowPhase = 'COLLECTING' | 'SOLVING' | 'DISCUSSION' | 'DONE'

export type WaitingReason = 'ANSWER_NEEDED' | 'CHAT'

export type DomainType = 'PARROT' | 'PRINTER'

export interface ClarificationStep {
  id: string
  prompt: string
  answer: string | null
  metadata?: Record<string, unknown>
}

export interface Solution {
  content: string
  confidence: number
  rationale?: string
}

export interface WorkflowState {
  id: string
  phase: WorkflowPhase
  steps: ClarificationStep[]
  solution: Solution | null
  skipped: boolean
}

/* ---------- API envelope ---------- */

export interface WorkflowResponse {
  workflow_id: string
  status: string
  state: WorkflowState
  waiting_reason?: WaitingReason | null
  confidence?: number | null
}

/* ---------- request payloads ---------- */

export interface CreateWorkflowRequest {
  domain: DomainType
  ticket: {
    id: string
    title: string
    description: string
  }
}

export interface AnswerStepRequest {
  step_id: string
  answer: string
}
