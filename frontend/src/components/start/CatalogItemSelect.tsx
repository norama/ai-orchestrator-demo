import { Badge } from '@/components/ui/Badge'
import { DomainBadge } from '@/components/workflow/DomainBadge'
import type { UICatalogItem } from '@/types/fe'

interface Props {
  catalogItems: UICatalogItem[]
  selectedItemId: string | null
  onSelect: (itemId: string) => void
  disabled?: boolean
}

export function CatalogItemSelect({
  catalogItems,
  selectedItemId,
  onSelect,
  disabled = false,
}: Props) {
  return (
    <div className='space-y-3'>
      <div className='text-sm font-bold text-gray-700'>Select a workflow type</div>

      <div className='grid gap-3 sm:grid-cols-2'>
        {catalogItems.length === 0 && (
          <div className='text-sm text-red-500 col-span-full text-center'>
            No catalog items available
          </div>
        )}

        {catalogItems.map((item) => {
          const selected = selectedItemId === item.id

          return (
            <div
              key={item.id}
              onClick={!disabled ? () => onSelect(item.id) : undefined}
              className={[
                'relative rounded-lg border p-3 transition',
                selected
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 bg-white hover:bg-gray-50 hover:border-gray-300',
                disabled ? 'opacity-80' : 'cursor-pointer',
              ].join(' ')}>
              <div className='font-medium text-gray-900'>{item.name}</div>

              <div className='mt-1 text-sm text-gray-600 line-clamp-2'>{item.description}</div>

              <div className='mt-2 flex gap-2'>
                {item.category && <Badge>{item.category}</Badge>}
                <DomainBadge domainType={item.domainType} />
              </div>

              {selected && <span className='absolute bottom-2 right-3 text-blue-600'>✓</span>}
            </div>
          )
        })}
      </div>
    </div>
  )
}
