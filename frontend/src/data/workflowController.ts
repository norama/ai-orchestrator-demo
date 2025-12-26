import { useState } from 'react'

import { answerStep, createWorkflow, getWorkflow, skipToSolution } from '@/api/workflows'
import type { DomainType, WaitingReason, WorkflowResponse, WorkflowState } from '@/types/workflow'

/* ---------- controller API ---------- */

export interface WorkflowController {
  workflow: WorkflowState | null
  waitingReason: WaitingReason | null
  confidence: number | null
  loading: boolean
  error: string | null

  start(domain: DomainType): Promise<void>
  answer(stepId: string, answer: string): Promise<void>
  skip(): Promise<void>
  refresh(): Promise<void>
  reset(): void
}

/* ---------- implementation ---------- */

export function useWorkflowController(): WorkflowController {
  const [workflow, setWorkflow] = useState<WorkflowState | null>(null)
  const [waitingReason, setWaitingReason] = useState<WaitingReason | null>(null)
  const [confidence, setConfidence] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /* ----- helpers ----- */

  function applyResponse(res: WorkflowResponse) {
    setWorkflow(res.state)
    setWaitingReason(res.waiting_reason ?? null)
    setConfidence(res.confidence ?? null)
  }

  /* ----- actions ----- */

  async function start(domain: DomainType): Promise<void> {
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
    setConfidence(null)
    setError(null)
    setLoading(false)
  }

  /* ----- exposed controller ----- */

  return {
    workflow,
    waitingReason,
    confidence,
    loading,
    error,
    start,
    answer,
    skip,
    refresh,
    reset,
  }
}
