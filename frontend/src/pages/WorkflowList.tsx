import { fetchWorkflows } from '@/api/workflows'
import { useEffect, useState } from 'react'

export function WorkflowList({ onSelect }: { onSelect: (id: string) => void }) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [workflows, setWorkflows] = useState<any[]>([])

  useEffect(() => {
    fetchWorkflows().then((res) => setWorkflows(res.workflows))
  }, [])

  return (
    <div>
      <h1 className='text-xl font-bold'>Workflows</h1>
      <ul>
        {workflows.map((wf) => (
          <li key={wf.id} className='cursor-pointer underline' onClick={() => onSelect(wf.id)}>
            {wf.ticket.title} ({wf.phase})
          </li>
        ))}
      </ul>
    </div>
  )
}
