import type {
  ChatRoleEnum,
  DomainTypeEnum,
  EventDisplayTypeEnum,
  WorkflowEventTypeEnum,
  WorkflowPhaseEnum,
} from '@/types/enums'
import { UIHistoryItemTypeEnum } from '@/types/enums'

export interface UICatalogItem {
  id: string
  name: string
  description: string
  category?: string
  domainType: DomainTypeEnum
}

export interface UIChatMessage {
  id: string
  role: ChatRoleEnum
  content: string
}

export interface UISolution {
  content: string
  confidence: number
  rationale?: string
}

export interface UIChatItem {
  type: typeof UIHistoryItemTypeEnum.MESSAGE
  phase: typeof WorkflowPhaseEnum.COLLECTING | typeof WorkflowPhaseEnum.DISCUSSION
  message: UIChatMessage
}

export interface UITicket {
  id: string
  title: string
  description: string
}

export interface UIWorkflowData {
  id: string
  domainType: DomainTypeEnum
  name: string
  description: string
  maxSteps: number
}

export interface UIChat {
  items: UIChatItem[]
}

export interface UICurrentStep {
  stepId: string
  prompt: string
}

export interface UICreateFromCatalog {
  itemId: string
  name?: string
  description?: string
  maxSteps?: number
}

export interface UIWorkflowCreateForm {
  domainType: DomainTypeEnum
  name?: string
  description?: string
  maxSteps?: number
}

export interface UIWorkflowListItem {
  id: string
  parentId: string | null
  parentSnapshotId: string | null
  name: string
  ticketTitle: string
  domainType: DomainTypeEnum
  phase: WorkflowPhaseEnum
}

export interface UIEventDisplayItem {
  type: EventDisplayTypeEnum
  label: string
  value: string | number | boolean
  emphasis: boolean
}

export interface UIWorkflowEvent {
  id: string
  snapshotId: string
  previousSnapshotId: string | null
  createdAt: Date

  type: WorkflowEventTypeEnum
  label: string
  display: UIEventDisplayItem[] | null

  isCurrent: boolean
}

export interface UIWorkflowHistory {
  workflowId: string
  parentWorkflowId: string | null
  currentSnapshotId: string
  events: UIWorkflowEvent[]
}

export interface UIWorkflowState {
  phase: WorkflowPhaseEnum
  chat: UIChat
  currentStep: UICurrentStep | null
  solution: UISolution | null
  solutionUpdated: boolean | null
  workflowConfidence: number | null
}
