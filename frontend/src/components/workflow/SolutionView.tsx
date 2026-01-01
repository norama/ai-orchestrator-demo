import { Badge } from '@/components/ui/Badge'
import { Confidence } from '@/components/workflow/Confidence'
import type { UISolution } from '@/types/fe'

interface Props {
  solution: UISolution
  updated: boolean | null
}

export function SolutionView({ solution, updated }: Props) {
  return (
    <div className='relative p-4 max-h-[30vh] overflow-y-auto bg-green-50 border border-green-200 rounded-lg whitespace-pre-wrap'>
      {updated && (
        <div className='sticky top-0 z-10 flex justify-end px-2 py-2'>
          {updated && <Badge variant='warning'>Updated</Badge>}
        </div>
      )}

      <h3 className='text-lg font-medium mb-2'>Proposed Solution</h3>

      <p className='text-sm leading-relaxed whitespace-pre-wrap mb-2'>{solution.content}</p>
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
