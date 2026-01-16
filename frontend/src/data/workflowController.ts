import { useState } from 'react'

import { createWorkflowFromCatalog } from '@/api/catalog'
import { branchFromSnapshot, getSnapshot } from '@/api/history'
import { postSSE } from '@/api/sse'
import { answerStep, getWorkflow, sendChatMessage, skipToSolution } from '@/api/workflows'
import {
  stateToWorkflowState,
  workflowToTicket,
  workflowToWorkflowData,
} from '@/data/workflowProjector'
import type { Workflow, WorkflowDetailResponse, WorkflowState } from '@/types/be'
import { ChatRoleEnum } from '@/types/enums'
import type { UICreateFromCatalog, UITicket, UIWorkflowData, UIWorkflowState } from '@/types/fe'

/* ---------- controller API ---------- */

interface Preview {
  snapshotId: string
  state: WorkflowState
}

export interface WorkflowController {
  ticket: UITicket | null
  workflowData: UIWorkflowData | null
  workflowState: UIWorkflowState | null
  loading: boolean
  error: string | null

  previewingSnapshotId: string | null

  isStreaming: boolean
  streamedText: string

  start(req: UICreateFromCatalog): Promise<string | null>
  answer(stepId: string, answer: string): Promise<void>
  answerStream(stepId: string, answer: string): Promise<void>
  chat(content: string): Promise<void>
  skip(): Promise<void>
  skipStream(): Promise<void>
  refresh(): Promise<void>
  load(workflowId: string, snapshotId: string | null): Promise<void>
  previewSnapshot(snapshotId: string): Promise<void>
  branch(): Promise<string | null>
  reset(): void
}

/* ---------- implementation ---------- */

export function useWorkflowController(): WorkflowController {
  const [workflow, setWorkflow] = useState<Workflow | null>(null)
  const [preview, setPreview] = useState<Preview | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [isStreaming, setIsStreaming] = useState(false)
  const [streamedText, setStreamedText] = useState('')

  /* ----- helpers ----- */

  function applyWorkflowResponse(res: WorkflowDetailResponse) {
    setWorkflow(res.workflow)
  }

  /* ----- actions ----- */

  async function start(req: UICreateFromCatalog): Promise<string | null> {
    setLoading(true)
    setError(null)

    try {
      const res = await createWorkflowFromCatalog({
        item_id: req.itemId,
        name: req.name,
        description: req.description,
        max_steps: req.maxSteps,
      })

      applyWorkflowResponse(res)
      return res.workflow.id
    } catch (e) {
      setError((e as Error).message)
      return null
    } finally {
      setLoading(false)
    }
  }

  async function answer(stepId: string, answer: string): Promise<void> {
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await answerStep(workflow.id, {
        step_id: stepId,
        answer,
      })

      applyWorkflowResponse(res)
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
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    await stream(`${workflow.id}/answer/stream`, {
      step_id: stepId,
      answer,
    })
  }

  async function chat(content: string): Promise<void> {
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await sendChatMessage(workflow.id, {
        role: ChatRoleEnum.USER,
        content,
      })

      applyWorkflowResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function skip(): Promise<void> {
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await skipToSolution(workflow.id)

      applyWorkflowResponse(res)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function skipStream(): Promise<void> {
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    await stream(`${workflow.id}/skip/stream`, {})
  }

  async function load(workflowId: string, snapshotId: string | null = null): Promise<void> {
    setPreview(null)
    setLoading(true)
    setError(null)

    try {
      const res = await getWorkflow(workflowId)
      applyWorkflowResponse(res)

      if (snapshotId) {
        const res = await getSnapshot(workflowId, snapshotId)
        setPreview({ snapshotId, state: res.snapshot })
      }
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function previewSnapshot(snapshotId: string): Promise<void> {
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await getSnapshot(workflow.id, snapshotId)
      setPreview({ snapshotId, state: res.snapshot })
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  async function branch(): Promise<string | null> {
    if (!workflow || !preview) {
      setError('No snapshot selected for branching')
      return null
    }

    setLoading(true)
    setError(null)

    try {
      const res = await branchFromSnapshot(workflow.id, preview.snapshotId)

      // Switch to new workflow
      setPreview(null)
      applyWorkflowResponse(res)
      return res.workflow.id
    } catch (e) {
      setError((e as Error).message)
      return null
    } finally {
      setLoading(false)
    }
  }

  async function refresh(): Promise<void> {
    if (!workflow) {
      setError('No workflow loaded')
      return
    }

    await load(workflow.id)
  }

  function reset(): void {
    setWorkflow(null)
    setPreview(null)
    setError(null)
    setLoading(false)
  }

  /* ----- projections ----- */

  const ticket = workflow ? workflowToTicket(workflow) : null
  const workflowData = workflow ? workflowToWorkflowData(workflow) : null
  const state = preview ? preview.state : workflow ? workflow.state : null
  const workflowState = state ? stateToWorkflowState(state) : null

  const previewingSnapshotId = preview !== null ? preview.snapshotId : null

  /* ----- exposed controller ----- */

  return {
    ticket,
    workflowData,
    workflowState,
    loading,
    error,
    previewingSnapshotId,
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
    previewSnapshot,
    branch,
    reset,
  } as WorkflowController
}
