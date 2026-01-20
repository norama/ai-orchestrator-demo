import { resetWorkspace } from '@/api/reset'
import { Button } from '@/components/ui/Button'

interface Props {
  disabled?: boolean
}

export function ResetDemoButton({ disabled = false }: Props) {
  return (
    <div className='flex-1 flex justify-end'>
      <Button
        variant='ghost'
        className='text-xs text-gray-500'
        onClick={async () => {
          const ok = window.confirm('Reset demo and start with a fresh workspace?')
          if (ok) {
            await resetWorkspace()
            window.location.reload()
          }
        }}
        disabled={disabled}>
        Reset demo
      </Button>
    </div>
  )
}
