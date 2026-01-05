import type { Workflow } from '@/types/be'
import { ChatRoleEnum, UIHistoryItemTypeEnum, WorkflowPhaseEnum } from '@/types/enums'
import type {
  UIChatHistory,
  UIChatHistoryItem,
  UICurrentStep,
  UISolution,
  UITicket,
  UIWorkflowData,
} from '@/types/fe'

export function workflowToOpenStep(workflow: Workflow): UICurrentStep | null {
  if (workflow.state.solution) {
    return null
  }
  const openStep = workflow.state.steps.find((step) => step.answer === null)
  if (openStep) {
    return {
      stepId: openStep.id,
      prompt: openStep.prompt,
    }
  }
  return null
}

// Assumption: discussion messages only appear after solution
export function workflowToChatHistory(workflow: Workflow): UIChatHistory {
  const items: UIChatHistoryItem[] = []

  workflow.state.steps.forEach((step, i) => {
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

  workflow.state.chat_history.messages.forEach((m, i) => {
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

export function workflowToSolution(workflow: Workflow): UISolution | null {
  const solution = workflow.state.solution
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
    phase: workflow.state.phase,
    solution: workflowToSolution(workflow),
    solutionUpdated: workflow.state.discussion_result
      ? workflow.state.discussion_result.solution_updated
      : null,
  }
}

export function workflowToTicket(workflow: Workflow): UITicket {
  return {
    id: workflow.ticket.id,
    title: workflow.ticket.title,
    description: workflow.ticket.description,
  }
}
