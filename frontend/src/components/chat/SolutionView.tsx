import { Confidence } from '@/components/chat/Confidence'
import type { UISolution } from '@/types/fe'

interface Props {
  solution: UISolution
}

export function SolutionView({ solution }: Props) {
  return (
    <div className='p-4 bg-green-50 border border-green-200 rounded-lg'>
      <h3 className='text-lg font-medium mb-2'>Proposed Solution</h3>
      <p className='whitespace-pre-wrap mb-2'>{solution.content}</p>
      <Confidence label='Solution confidence' confidence={solution.confidence} />
      {solution.rationale && (
        <div className='mt-2 p-2 bg-green-100 border border-green-200 rounded'>
          <h4 className='font-medium mb-1'>Rationale:</h4>
          <p className='whitespace-pre-wrap text-sm'>{solution.rationale}</p>
        </div>
      )}
    </div>
  )
}
