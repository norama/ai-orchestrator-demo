import type { WorkflowState } from '@/types/be'
import { ChatRoleEnum, UIHistoryItemTypeEnum } from '@/types/enums'
import type { UIChatHistory, UIChatHistoryItem, UICurrentStep } from '@/types/fe'

export function workflowToOpenStep(state: WorkflowState): UICurrentStep | null {
  if (state.solution) {
    return null
  }
  const openStep = state.steps.find((step) => step.answer === null)
  if (openStep) {
    return {
      step_id: openStep.id,
      prompt: openStep.prompt,
    }
  }
  return null
}

export function workflowToChatHistory(state: WorkflowState): UIChatHistory {
  const items: UIChatHistoryItem[] = []

  state.steps.forEach((step, i) => {
    if (step.answer) {
      items.push({
        type: UIHistoryItemTypeEnum.MESSAGE,
        message: {
          id: `q-${i}`,
          role: ChatRoleEnum.AI,
          content: step.prompt,
        },
      })

      items.push({
        type: UIHistoryItemTypeEnum.MESSAGE,
        message: {
          id: `a-${i}`,
          role: ChatRoleEnum.USER,
          content: step.answer,
        },
      })
    }
  })

  if (state.solution) {
    items.push({
      type: UIHistoryItemTypeEnum.SOLUTION,
      solution: {
        content: state.solution.content,
        confidence: state.solution.confidence,
        rationale: state.solution.rationale,
      },
    })
  }

  state.chat_history.messages.forEach((m, i) => {
    items.push({
      type: UIHistoryItemTypeEnum.MESSAGE,
      message: {
        id: `c-${i}`,
        role: m.role,
        content: m.content,
      },
    })
  })

  return {
    items,
  }
}
