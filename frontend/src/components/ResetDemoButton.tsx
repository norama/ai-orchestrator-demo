import { resetWorkspace } from '@/api/api'
import { Button } from '@/components/ui/Button'

export function ResetDemoButton() {
  return (
    <div className='flex-1 flex justify-end'>
      <Button
        variant='ghost'
        className='text-xs text-gray-500'
        onClick={() => {
          const ok = window.confirm('Reset demo and start with a fresh workspace?')
          if (ok) {
            resetWorkspace()
            window.location.reload()
          }
        }}>
        Reset demo
      </Button>
    </div>
  )
}
