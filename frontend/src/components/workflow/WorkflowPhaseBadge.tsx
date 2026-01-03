import { Badge } from '@/components/ui/Badge'
import { WorkflowPhaseEnum } from '@/types/enums'

interface WorkflowPhaseBadgeProps {
  phase: WorkflowPhaseEnum
}

export function WorkflowPhaseBadge({ phase }: WorkflowPhaseBadgeProps) {
  const variant =
    phase === WorkflowPhaseEnum.DONE
      ? 'error'
      : phase === WorkflowPhaseEnum.SOLVING || phase === WorkflowPhaseEnum.DISCUSSION
        ? 'success'
        : 'info'

  return <Badge variant={variant}>{phase}</Badge>
}
