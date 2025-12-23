/* eslint-disable @typescript-eslint/no-explicit-any */
// src/pages/WorkflowDetail.tsx
import { fetchWorkflow } from '@/api/workflows'
import { useEffect, useState } from 'react'

export function WorkflowDetail({ id }: { id: string }) {
  const [workflow, setWorkflow] = useState<any | null>(null)

  useEffect(() => {
    fetchWorkflow(id).then((res) => setWorkflow(res.state))
  }, [id])

  if (!workflow) return <div>Loading...</div>

  return (
    <div>
      <h2 className='text-lg font-bold'>{workflow.ticket.title}</h2>
      <p className='text-sm text-amber-700'>Phase: {workflow.phase}</p>

      <h3 className='mt-4 font-semibold'>Clarifications</h3>
      <ul>
        {workflow.clarifications.map((c: any) => (
          <li key={c.id}>
            <strong>Q:</strong> {c.question}
            <br />
            <strong>A:</strong> {c.answer ?? '—'}
          </li>
        ))}
      </ul>
    </div>
  )
}
