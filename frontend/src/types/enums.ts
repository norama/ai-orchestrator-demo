export const WorkflowPhaseEnum = {
  COLLECTING: 'COLLECTING',
  SOLVING: 'SOLVING',
  DISCUSSION: 'DISCUSSION',
  DONE: 'DONE',
} as const

export type WorkflowPhaseEnum = (typeof WorkflowPhaseEnum)[keyof typeof WorkflowPhaseEnum]

export const WaitingReasonEnum = {
  ANSWER_NEEDED: 'ANSWER_NEEDED',
  CHAT: 'CHAT',
} as const

export type WaitingReasonEnum = (typeof WaitingReasonEnum)[keyof typeof WaitingReasonEnum]

export const DomainTypeEnum = {
  PARROT: 'PARROT',
  PRINTER: 'PRINTER',
  LLM_SUPPORT: 'LLM_SUPPORT',
} as const

export type DomainTypeEnum = (typeof DomainTypeEnum)[keyof typeof DomainTypeEnum]

export const ChatRoleEnum = {
  USER: 'USER',
  AI: 'AI',
  SYSTEM: 'SYSTEM',
} as const

export type ChatRoleEnum = (typeof ChatRoleEnum)[keyof typeof ChatRoleEnum]

export const UIHistoryItemTypeEnum = {
  MESSAGE: 'MESSAGE',
  SOLUTION: 'SOLUTION',
} as const

export type UIHistoryItemTypeEnum =
  (typeof UIHistoryItemTypeEnum)[keyof typeof UIHistoryItemTypeEnum]
