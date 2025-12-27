import type {
  ChatRoleEnum,
  DomainTypeEnum,
  WaitingReasonEnum,
  WorkflowPhaseEnum,
} from '@/types/enums'

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

export interface ChatMessage {
  role: ChatRoleEnum
  content: string
}

export interface ChatHistory {
  messages: ChatMessage[]
}

export interface WorkflowState {
  id: string
  domain: DomainTypeEnum
  name: string
  description: string
  phase: WorkflowPhaseEnum
  steps: ClarificationStep[]
  solution: Solution | null
  skipped: boolean
  chat_history: ChatHistory
}

/* ---------- API envelope ---------- */

export interface WorkflowResponse {
  workflow_id: string
  status: string
  state: WorkflowState
  waiting_reason?: WaitingReasonEnum | null
  workflow_confidence?: number | null
}

/* ---------- request payloads ---------- */

export interface CreateWorkflowRequest {
  domain: DomainTypeEnum
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

export interface ChatMessageRequest {
  role: ChatRoleEnum
  content: string
}
