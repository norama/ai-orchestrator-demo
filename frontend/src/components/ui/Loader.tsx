type LoaderProps = {
  className?: string
  label?: string
}

export function Loader({ className = '', label = 'Loading' }: LoaderProps) {
  return (
    <div className={['inline-flex items-center gap-3 text-gray-500', className].join(' ')}>
      <span
        className='h-5 w-5 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600'
        aria-hidden='true'
      />
      <span className='text-sm'>{label}</span>
    </div>
  )
}
