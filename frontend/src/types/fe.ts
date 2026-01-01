import type { ChatRoleEnum, DomainTypeEnum, WorkflowPhaseEnum } from '@/types/enums'
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

export interface UIChatHistoryItem {
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
  phase: WorkflowPhaseEnum
  solution: UISolution | null
  solutionUpdated: boolean | null
}

export interface UIChatHistory {
  items: UIChatHistoryItem[]
}

export interface UICurrentStep {
  step_id: string
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
  name: string
  ticketTitle: string
  domainType: DomainTypeEnum
  phase: WorkflowPhaseEnum
}
