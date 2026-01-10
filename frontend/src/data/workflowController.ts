import { useState } from 'react'

import { createWorkflowFromCatalog } from '@/api/catalog'
import { answerStep, getWorkflow, sendChatMessage, skipToSolution } from '@/api/workflows'
import { postSSE } from '@/data/sse'
import {
  stateToWorkflowState,
  workflowToTicket,
  workflowToWorkflowData,
} from '@/data/workflowProjector'
import type { Workflow, WorkflowDetailResponse } from '@/types/be'
import { ChatRoleEnum, type WaitingReasonEnum } from '@/types/enums'
import type { UICreateFromCatalog, UITicket, UIWorkflowData, UIWorkflowState } from '@/types/fe'

/* ---------- controller API ---------- */

export interface WorkflowController {
  ticket: UITicket | null
  workflowData: UIWorkflowData | null
  workflowState: UIWorkflowState | null
  waitingReason: WaitingReasonEnum | null
  workflowConfidence: number | null
  loading: boolean
  error: string | null

  isStreaming: boolean
  streamedText: string

  start(req: UICreateFromCatalog): Promise<void>
  answer(stepId: string, answer: string): Promise<void>
  answerStream(stepId: string, answer: string): Promise<void>
  chat(content: string): Promise<void>
  skip(): Promise<void>
  skipStream(): Promise<void>
  refresh(): Promise<void>
  load(workflowId: string): Promise<void>
  reset(): void
}

/* ---------- implementation ---------- */

export function useWorkflowController(): WorkflowController {
  const [workflow, setWorkflow] = useState<Workflow | null>(null)
  const [waitingReason, setWaitingReason] = useState<WaitingReasonEnum | null>(null)
  const [workflowConfidence, setWorkflowConfidence] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [isStreaming, setIsStreaming] = useState(false)
  const [streamedText, setStreamedText] = useState('')

  /* ----- helpers ----- */

  function applyResponse(res: WorkflowDetailResponse) {
    setWorkflow(res.workflow)
    setWaitingReason(res.waiting_reason ?? null)
    setWorkflowConfidence(res.workflow_confidence ?? null)
  }

  /* ----- actions ----- */

  async function start(req: UICreateFromCatalog): Promise<void> {
    setLoading(true)
    setError(null)

    try {
      const res = await createWorkflowFromCatalog({
        item_id: req.itemId,
        name: req.name,
        description: req.description,
        max_steps: req.maxSteps,
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

  async function stream(path: string, body: unknown): Promise<void> {
    setIsStreaming(true)
    setStreamedText('')
    setError(null)

    try {
      await postSSE(path, body, {
        onChunk: (text) => {
          setStreamedText((prev) => prev + text)
        },
        onDone: async () => {
          setIsStreaming(false)

          // authoritative refresh
          await refresh()

          // reset streamed text back only after refresh to avoid flicker
          setStreamedText('')
        },
        onError: (err) => {
          setIsStreaming(false)
          setError(err)
        },
      })
    } catch (e) {
      setIsStreaming(false)
      setError((e as Error).message)
    }
  }

  async function answerStream(stepId: string, answer: string): Promise<void> {
    if (!workflow) return

    await stream(`${workflow.id}/answer/stream`, {
      step_id: stepId,
      answer,
    })
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

  async function skipStream(): Promise<void> {
    if (!workflow) return

    await stream(`${workflow.id}/skip/stream`, {})
  }

  async function load(workflowId: string): Promise<void> {
    setLoading(true)
    setError(null)

    try {
      const res = await getWorkflow(workflowId)
      applyResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function refresh(): Promise<void> {
    if (!workflow) return

    await load(workflow.id)
  }

  function reset(): void {
    setWorkflow(null)
    setWaitingReason(null)
    setWorkflowConfidence(null)
    setError(null)
    setLoading(false)
  }

  /* ----- projections ----- */

  const ticket = workflow ? workflowToTicket(workflow) : null
  const workflowData = workflow ? workflowToWorkflowData(workflow) : null
  const workflowState = workflow ? stateToWorkflowState(workflow.state) : null

  /* ----- exposed controller ----- */

  return {
    ticket,
    workflowData,
    workflowState,
    waitingReason,
    workflowConfidence,
    loading,
    error,
    isStreaming,
    streamedText,
    start,
    answer,
    answerStream,
    chat,
    skip,
    skipStream,
    refresh,
    load,
    reset,
  }
}
