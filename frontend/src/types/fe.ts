import type { ChatRoleEnum, DomainTypeEnum, WorkflowPhaseEnum } from '@/types/enums'
import { UIHistoryItemTypeEnum } from '@/types/enums'

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

export type UIChatHistoryItem =
  | {
      type: typeof UIHistoryItemTypeEnum.MESSAGE
      message: UIChatMessage
    }
  | {
      type: typeof UIHistoryItemTypeEnum.SOLUTION
      solution: UISolution
    }

export interface UIWorkflowData {
  id: string
  domain: DomainTypeEnum
  name: string
  description: string
  phase: WorkflowPhaseEnum
}

export interface UIChatHistory {
  items: UIChatHistoryItem[]
}

export interface UICurrentStep {
  step_id: string
  prompt: string
}
