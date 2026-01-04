import { MarkdownView } from '@/components/ui/MarkdownView'
import { Confidence } from '@/components/workflow/Confidence'
import { Rationale } from '@/components/workflow/Rationale'
import { SolutionStatus } from '@/components/workflow/SolutionStatus'
import { DomainTypeEnum } from '@/types/enums'
import type { UISolution } from '@/types/fe'
import { useEffect, useRef } from 'react'

interface Props {
  solution: UISolution | null
  updated: boolean | null
  domainType: DomainTypeEnum
  isStreaming: boolean
  streamedText: string
}

export function SolutionView({ solution, updated, domainType, isStreaming, streamedText }: Props) {
  const content = streamedText ? streamedText : solution ? solution.content : null
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isStreaming) return
    const el = containerRef.current
    if (!el) return

    el.scrollTop = el.scrollHeight
  }, [streamedText, isStreaming])

  return (
    <div
      ref={containerRef}
      className='relative p-4 max-h-[30vh] overflow-y-auto bg-green-50 border border-green-200 rounded-lg'>
      {updated && <SolutionStatus status='Updated' variant='warning' />}
      {isStreaming && <SolutionStatus status='Generating' variant='info' />}

      {domainType !== DomainTypeEnum.LLM_REPORT && (
        <h3 className='text-lg font-medium mb-2'>Proposed Solution</h3>
      )}

      {content && <MarkdownView content={content} />}

      {solution && <Confidence label='Solution confidence' confidence={solution.confidence} />}
      {solution && <Rationale label='Rationale' rationale={solution.rationale} />}
    </div>
  )
}
