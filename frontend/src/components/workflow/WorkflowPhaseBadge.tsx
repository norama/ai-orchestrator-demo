import { Badge } from '@/components/ui/Badge'
import { WorkflowPhaseEnum } from '@/types/enums'

interface Props {
  phase: WorkflowPhaseEnum
}

export function WorkflowPhaseBadge({ phase }: Props) {
  const variant =
    phase === WorkflowPhaseEnum.DONE
      ? 'error'
      : phase === WorkflowPhaseEnum.SOLVING || phase === WorkflowPhaseEnum.DISCUSSION
        ? 'success'
        : 'info'

  return <Badge variant={variant}>{phase}</Badge>
}
