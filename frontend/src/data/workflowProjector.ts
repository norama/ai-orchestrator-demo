import type { WorkflowState } from '@/types/be'
import { ChatRoleEnum, UIHistoryItemTypeEnum, WorkflowPhaseEnum } from '@/types/enums'
import type { UIChatHistory, UIChatHistoryItem, UICurrentStep } from '@/types/fe'

export function workflowToOpenStep(state: WorkflowState): UICurrentStep | null {
  if (state.solution) {
    return null
  }
  const openStep = state.steps.find((step) => step.answer === null)
  if (openStep) {
    return {
      stepId: openStep.id,
      prompt: openStep.prompt,
    }
  }
  return null
}

// Assumption: discussion messages only appear after solution
export function workflowToChatHistory(state: WorkflowState): UIChatHistory {
  const items: UIChatHistoryItem[] = []

  state.steps.forEach((step, i) => {
    if (step.answer) {
      items.push({
        type: UIHistoryItemTypeEnum.MESSAGE,
        phase: WorkflowPhaseEnum.COLLECTING,
        message: {
          id: `q-${i}`,
          role: ChatRoleEnum.AI,
          content: step.prompt,
        },
      })

      items.push({
        type: UIHistoryItemTypeEnum.MESSAGE,
        phase: WorkflowPhaseEnum.COLLECTING,
        message: {
          id: `a-${i}`,
          role: ChatRoleEnum.USER,
          content: step.answer,
        },
      })
    }
  })

  state.chat_history.messages.forEach((m, i) => {
    items.push({
      type: UIHistoryItemTypeEnum.MESSAGE,
      phase: WorkflowPhaseEnum.DISCUSSION,
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

export function workflowToSolution(state: WorkflowState) {
  if (state.solution) {
    return {
      content: state.solution.content,
      confidence: state.solution.confidence,
      rationale: state.solution.rationale || undefined,
    }
  }
  return null
}
