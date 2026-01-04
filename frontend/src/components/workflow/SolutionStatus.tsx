import { Badge, type BadgeVariant } from '@/components/ui/Badge'

interface Props {
  status: string
  variant: BadgeVariant
}

export function SolutionStatus({ status, variant }: Props) {
  return (
    <div className='sticky top-0 z-10 flex justify-end px-2 py-2'>
      <Badge variant={variant}>{status}</Badge>
    </div>
  )
}
