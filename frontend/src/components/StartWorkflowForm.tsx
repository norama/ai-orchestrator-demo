import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Textarea } from '@/components/ui/Textarea'
import { DomainTypeEnum } from '@/types/enums'
import type { UIWorkflowCreateForm } from '@/types/fe'
import { useState } from 'react'

interface Props {
  loading: boolean
  error: string | null
  onStart: (req: UIWorkflowCreateForm) => void
}

export function StartWorkflowForm({ loading, error, onStart }: Props) {
  const [domain, setDomain] = useState<DomainTypeEnum>(DomainTypeEnum.PRINTER)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [maxSteps, setMaxSteps] = useState(8)

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-50'>
      <div className='space-y-4 p-6 bg-white rounded shadow max-w-md w-full'>
        <h1 className='text-xl font-semibold text-center'>AI Orchestrator Demo</h1>

        <p className='text-sm text-gray-600 text-center'>Configure and start a workflow</p>

        {/* Domain */}
        <div className='space-y-1'>
          <label className='text-sm font-medium'>Domain</label>
          <Select value={domain} onChange={(e) => setDomain(e.target.value as DomainTypeEnum)}>
            <option value={DomainTypeEnum.PRINTER}>Printer</option>
            <option value={DomainTypeEnum.PARROT}>Parrot</option>
            <option value={DomainTypeEnum.LLM_SUPPORT}>LLM Support</option>
          </Select>
        </div>

        {/* Name */}
        <div className='space-y-1'>
          <label className='text-sm font-medium'>Name</label>
          <Input
            placeholder='Short workflow name'
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        {/* Description */}
        <div className='space-y-1'>
          <label className='text-sm font-medium'>Description</label>
          <Textarea
            rows={3}
            placeholder='Optional description'
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        {/* Max steps */}
        <div className='space-y-1'>
          <label className='text-sm font-medium'>Max clarification steps</label>
          <Input
            type='number'
            min={1}
            max={20}
            value={maxSteps}
            onChange={(e) => setMaxSteps(Number(e.target.value))}
          />
        </div>

        <div className='flex justify-end'>
          <Button
            disabled={loading}
            onClick={() => onStart({ domain, name, description, maxSteps })}>
            Start workflow
          </Button>
        </div>
        {error && <div className='text-sm text-red-600 text-center'>{error}</div>}
      </div>
    </div>
  )
}
