import { Badge } from '@/components/ui/Badge'
import { MarkdownView } from '@/components/ui/MarkdownView'
import { Confidence } from '@/components/workflow/Confidence'
import { DomainTypeEnum } from '@/types/enums'
import type { UISolution } from '@/types/fe'

interface Props {
  solution: UISolution
  updated: boolean | null
  domainType: DomainTypeEnum
}

export function SolutionView({ solution, updated, domainType }: Props) {
  return (
    <div className='relative p-4 max-h-[30vh] overflow-y-auto bg-green-50 border border-green-200 rounded-lg whitespace-pre-wrap'>
      {updated && (
        <div className='sticky top-0 z-10 flex justify-end px-2 py-2'>
          {updated && <Badge variant='warning'>Updated</Badge>}
        </div>
      )}

      {domainType !== DomainTypeEnum.LLM_REPORT && (
        <h3 className='text-lg font-medium mb-2'>Proposed Solution</h3>
      )}

      <MarkdownView content={solution.content} />

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
