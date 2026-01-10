import type { Workflow, WorkflowState } from '@/types/be'
import { ChatRoleEnum, UIHistoryItemTypeEnum, WorkflowPhaseEnum } from '@/types/enums'
import type {
  UIChat,
  UIChatItem,
  UICurrentStep,
  UISolution,
  UITicket,
  UIWorkflowData,
  UIWorkflowState,
} from '@/types/fe'

export function stateToOpenStep(state: WorkflowState): UICurrentStep | null {
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
export function stateToChatHistory(state: WorkflowState): UIChat {
  const items: UIChatItem[] = []

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

export function stateToSolution(state: WorkflowState): UISolution | null {
  const solution = state.solution
  if (solution) {
    return {
      content: solution.content,
      confidence: solution.confidence,
      rationale: solution.rationale || undefined,
    }
  }
  return null
}

export function workflowToWorkflowData(workflow: Workflow): UIWorkflowData {
  return {
    id: workflow.id,
    domainType: workflow.domain_type,
    name: workflow.name,
    description: workflow.description,
    maxSteps: workflow.max_steps,
  }
}

export function workflowToTicket(workflow: Workflow): UITicket {
  return {
    id: workflow.ticket.id,
    title: workflow.ticket.title,
    description: workflow.ticket.description,
  }
}

export function stateToWorkflowState(state: WorkflowState): UIWorkflowState {
  return {
    phase: state.phase,
    chat: stateToChatHistory(state),
    currentStep: stateToOpenStep(state),
    solution: stateToSolution(state),
    solutionUpdated: state.discussion_result ? state.discussion_result.solution_updated : null,
  }
}
