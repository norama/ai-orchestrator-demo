import { Badge } from '@/components/ui/Badge'
import { DomainTypeEnum } from '@/types/enums'

const DOMAIN_LABEL: Record<DomainTypeEnum, string> = {
  [DomainTypeEnum.PARROT]: 'Parrot',
  [DomainTypeEnum.PRINTER]: 'Printer',
  [DomainTypeEnum.LLM_SUPPORT]: 'Tech Issues',
  [DomainTypeEnum.LLM_REPORT]: 'Reporting',
}

interface Props {
  domainType: DomainTypeEnum
}

export function DomainBadge({ domainType }: Props) {
  return <Badge variant='info'>{DOMAIN_LABEL[domainType]}</Badge>
}
