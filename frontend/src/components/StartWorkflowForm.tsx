import { CatalogItemSelect } from '@/components/start/CatalogItemSelect'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Textarea } from '@/components/ui/Textarea'
import type { UICatalogItem, UICreateFromCatalog } from '@/types/fe'
import { useState } from 'react'

interface Props {
  loading: boolean
  error: string | null
  catalogItems: UICatalogItem[]
  onStart: (req: UICreateFromCatalog) => void
}

export function StartWorkflowForm({ loading, error, catalogItems, onStart }: Props) {
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [maxSteps, setMaxSteps] = useState(8)

  return (
    <div className='min-h-screen bg-gray-50'>
      <div className='mx-auto max-w-3xl px-4 py-10 space-y-8'>
        {/* Header */}
        <div className='text-center space-y-2'>
          <h1 className='text-2xl font-semibold text-gray-900'>AI Orchestrator Demo</h1>
          <p className='text-sm text-gray-600'>Start a workflow from the catalog</p>
        </div>

        {/* Catalog */}
        <CatalogItemSelect
          catalogItems={catalogItems}
          selectedItemId={selectedItemId}
          onSelect={setSelectedItemId}
          disabled={loading}
        />

        {/* Optional configuration */}
        <div className='space-y-4 rounded-lg border border-gray-400 bg-white p-4'>
          <div className='text-sm font-medium text-gray-700'>Optional configuration</div>

          <div className='grid gap-4 sm:grid-cols-2'>
            <Input
              placeholder='Workflow name (optional)'
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <Input
              type='number'
              min={1}
              max={20}
              value={maxSteps}
              onChange={(e) => setMaxSteps(Number(e.target.value))}
              placeholder='Max steps'
            />
          </div>

          <Textarea
            rows={2}
            placeholder='Optional description'
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        {/* Actions */}
        <div className='flex justify-end'>
          <Button
            disabled={loading || selectedItemId === null}
            onClick={
              selectedItemId
                ? () =>
                    onStart({
                      itemId: selectedItemId,
                      name,
                      description,
                      maxSteps,
                    })
                : undefined
            }>
            Start workflow
          </Button>
        </div>

        {error && <div className='text-sm text-red-600 text-center'>{error}</div>}
      </div>
    </div>
  )
}
