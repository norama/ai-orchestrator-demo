import { WorkflowDetail } from '@/pages/WorkflowDetail'
import { WorkflowList } from '@/pages/WorkflowList'
import { useState } from 'react'

export default function App() {
  const [selectedId, setSelectedId] = useState<string | null>(null)

  return (
    <div className='p-4'>
      {!selectedId ? <WorkflowList onSelect={setSelectedId} /> : <WorkflowDetail id={selectedId} />}
    </div>
  )
}
