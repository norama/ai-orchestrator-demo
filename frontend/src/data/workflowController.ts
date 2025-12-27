import { useState } from 'react'

import {
  answerStep,
  createWorkflow,
  getWorkflow,
  sendChatMessage,
  skipToSolution,
} from '@/api/workflows'
import { workflowToChatHistory, workflowToOpenStep } from '@/data/workflowProjector'
import type { WorkflowResponse, WorkflowState } from '@/types/be'
import { ChatRoleEnum, type DomainTypeEnum, type WaitingReasonEnum } from '@/types/enums'
import type { UIChatHistory, UICurrentStep, UIWorkflowData } from '@/types/fe'

/* ---------- controller API ---------- */

export interface WorkflowController {
  workflowData: UIWorkflowData | null
  currentStep: UICurrentStep | null
  chatHistory: UIChatHistory | null
  waitingReason: WaitingReasonEnum | null
  workflowConfidence: number | null
  loading: boolean
  error: string | null

  start(domain: DomainTypeEnum): Promise<void>
  answer(stepId: string, answer: string): Promise<void>
  chat(content: string): Promise<void>
  skip(): Promise<void>
  refresh(): Promise<void>
  reset(): void
}

/* ---------- implementation ---------- */

export function useWorkflowController(): WorkflowController {
  const [workflow, setWorkflow] = useState<WorkflowState | null>(null)
  const [waitingReason, setWaitingReason] = useState<WaitingReasonEnum | null>(null)
  const [workflowConfidence, setWorkflowConfidence] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /* ----- helpers ----- */

  function applyResponse(res: WorkflowResponse) {
    setWorkflow(res.state)
    setWaitingReason(res.waiting_reason ?? null)
    setWorkflowConfidence(res.workflow_confidence ?? null)
  }

  /* ----- actions ----- */

  async function start(domain: DomainTypeEnum): Promise<void> {
    setLoading(true)
    setError(null)

    try {
      const res = await createWorkflow({
        domain,
        ticket: {
          id: crypto.randomUUID(),
          title: 'Demo ticket',
          description: 'Printer problem',
        },
      })

      applyResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function answer(stepId: string, answer: string): Promise<void> {
    if (!workflow) return

    setLoading(true)
    setError(null)

    try {
      const res = await answerStep(workflow.id, {
        step_id: stepId,
        answer,
      })

      applyResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function chat(content: string): Promise<void> {
    if (!workflow) return

    setLoading(true)
    setError(null)

    try {
      const res = await sendChatMessage(workflow.id, {
        role: ChatRoleEnum.USER,
        content,
      })

      applyResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function skip(): Promise<void> {
    if (!workflow) return

    setLoading(true)
    setError(null)

    try {
      const res = await skipToSolution(workflow.id)

      applyResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function refresh(): Promise<void> {
    if (!workflow) return

    setLoading(true)
    setError(null)

    try {
      const res = await getWorkflow(workflow.id)
      applyResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  function reset(): void {
    setWorkflow(null)
    setWaitingReason(null)
    setWorkflowConfidence(null)
    setError(null)
    setLoading(false)
  }

  /* ----- projections ----- */

  const currentStep = workflow ? workflowToOpenStep(workflow) : null
  const chatHistory = workflow ? workflowToChatHistory(workflow) : null
  const workflowData = workflow
    ? {
        id: workflow.id,
        domain: workflow.domain,
        name: workflow.name,
        description: workflow.description,
        phase: workflow.phase,
      }
    : null

  /* ----- exposed controller ----- */

  return {
    workflowData,
    currentStep,
    chatHistory,
    waitingReason,
    workflowConfidence,
    loading,
    error,
    start,
    answer,
    chat,
    skip,
    refresh,
    reset,
  }
}
