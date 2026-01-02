import { Badge } from '@/components/ui/Badge'
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
  const baseClassName = 'border rounded p-3 border-gray-200'
  const selectedBaseClassName = 'relative border rounded p-3 border-blue-500 bg-blue-50'
  const className = disabled ? baseClassName : `${baseClassName} cursor-pointer hover:bg-gray-100`
  const selectedClassName = disabled
    ? selectedBaseClassName
    : `${selectedBaseClassName} cursor-pointer`
  return (
    <>
      <label className='text-sm font-medium'>Select a ticket</label>

      <div className='space-y-2 max-h-60 overflow-y-auto'>
        {catalogItems.length === 0 && (
          <div key='-' className='text-sm text-red-500 text-center'>
            No catalog items available
          </div>
        )}
        {catalogItems.map((item) => (
          <div
            key={item.id}
            className={selectedItemId === item.id ? selectedClassName : className}
            onClick={!disabled ? () => onSelect(item.id) : undefined}
            role='button'
            tabIndex={0}
            aria-pressed={selectedItemId === item.id}>
            <div className='font-medium'>{item.name}</div>
            <div className='text-sm text-gray-600'>{item.description}</div>
            <div className='mt-2 flex flex-wrap gap-2'>
              {item.category && <Badge>{item.category}</Badge>}

              <Badge variant='info'>{item.domainType}</Badge>
            </div>
            {selectedItemId === item.id && (
              <span className='absolute bottom-2 right-2 text-blue-600'>✓</span>
            )}
          </div>
        ))}
      </div>
    </>
  )
}
