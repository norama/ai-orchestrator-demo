import type {
  ChatRoleEnum,
  DomainTypeEnum,
  EventDisplayTypeEnum,
  WaitingReasonEnum,
  WorkflowEventTypeEnum,
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

export interface NextStepDecision {
  next_step: ClarificationStep | null
  workflow_confidence: number | null
  reason: string
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
  last_decision: NextStepDecision | null
  solution: Solution | null
  skipped: boolean
  chat_history: ChatHistory
  discussion_result: ChatMutationResult | null
}

export interface Workflow {
  id: string
  parent_id: string | null
  parent_snapshot_id: string | null
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
  workflow: Workflow
  waiting_reason?: WaitingReasonEnum | null
  workflow_confidence?: number | null
  status: string
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

export interface EventDisplayItem {
  type: EventDisplayTypeEnum
  label: string
  value: string | number | boolean
  emphasis: boolean
}

export interface WorkflowEventView {
  id: string
  snapshot_id: string
  previous_snapshot_id: string | null
  created_at: string

  type: WorkflowEventTypeEnum
  label: string
  display: EventDisplayItem[] | null
}

export interface WorkflowHistoryResponse {
  workflow_id: string
  parent_workflow_id: string | null
  current_snapshot_id: string
  events: WorkflowEventView[]
  status: string
}

export interface SnapshotDetailResponse {
  workflow_id: string
  snapshot_id: string
  snapshot: WorkflowState
  waiting_reason?: WaitingReasonEnum | null
  workflow_confidence?: number | null
  status: string
}
