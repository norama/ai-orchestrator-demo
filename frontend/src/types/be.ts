import type {
  ChatRoleEnum,
  DomainTypeEnum,
  WaitingReasonEnum,
  WorkflowPhaseEnum,
} from '@/types/enums'

export interface CatalogItemResponse {
  id: string
  name: string
  description: string
  category: string | null
  domain_type: DomainTypeEnum
}

export interface ClarificationStep {
  id: string
  prompt: string
  answer: string | null
  metadata?: Record<string, unknown>
}

export interface Solution {
  content: string
  confidence: number
  rationale: string | null
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
  phase: WorkflowPhaseEnum
  steps: ClarificationStep[]
  solution: Solution | null
  skipped: boolean
  chat_history: ChatHistory
  discussion_result: ChatMutationResult | null
}

export interface Workflow {
  id: string
  parent_id: string | null
  ticket: Ticket
  domain_type: DomainTypeEnum
  name: string
  description: string
  max_steps: number
  state: WorkflowState
}

/* ---------- API envelope ---------- */

export interface CatalogResponse {
  items: CatalogItemResponse[]
  status: string
}

export interface WorkflowDetailResponse {
  workflow_id: string
  status: string
  workflow: Workflow
  waiting_reason?: WaitingReasonEnum | null
  workflow_confidence?: number | null
}

export interface WorkflowListResponse {
  workflows: Workflow[]
  status: string
}

/* ---------- request payloads ---------- */

export interface CreateFromCatalogRequest {
  item_id: string
  name?: string
  description?: string
  max_steps?: number
}

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
