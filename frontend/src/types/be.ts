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

export interface ChatMutationResult {
  solution_updated: boolean
  solution_version: number | null
}

export interface Ticket {
  id: string
  title: string
  description: string
}

export interface WorkflowState {
  id: string
  ticket: Ticket
  domain_type: DomainTypeEnum
  name: string
  description: string
  max_steps: number
  phase: WorkflowPhaseEnum
  steps: ClarificationStep[]
  solution: Solution | null
  skipped: boolean
  chat_history: ChatHistory
  discussion_result: ChatMutationResult | null
}

/* ---------- API envelope ---------- */

export interface WorkflowDetailResponse {
  workflow_id: string
  status: string
  state: WorkflowState
  waiting_reason?: WaitingReasonEnum | null
  workflow_confidence?: number | null
}

export interface WorkflowListResponse {
  workflows: WorkflowState[]
  status: string
}

/* ---------- request payloads ---------- */

export interface CreateWorkflowRequest {
  domain_type: DomainTypeEnum
  name?: string
  description?: string
  max_steps?: number
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
