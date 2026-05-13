type LoaderProps = {
  size?: 'small' | 'medium' | 'large'
  label?: string
}

const SIZE_CLASS: Record<NonNullable<LoaderProps['size']>, string> = {
  small: 'gap-2 text-xs',
  medium: 'gap-3 text-sm',
  large: 'gap-3.5 text-base',
}

const SPINNER_SIZE_CLASS: Record<NonNullable<LoaderProps['size']>, string> = {
  small: 'h-4 w-4 border-2',
  medium: 'h-8 w-8 border-3',
  large: 'h-12 w-12 border-4',
}

export function Loader({ size = 'medium', label = 'Loading' }: LoaderProps) {
  return (
    <div className={['inline-flex items-center text-blue-700', SIZE_CLASS[size]].join(' ')}>
      <span
        className={[
          'animate-spin rounded-full border-blue-200 border-t-blue-700',
          SPINNER_SIZE_CLASS[size],
        ].join(' ')}
        aria-hidden='true'
      />
      <span>{label}</span>
    </div>
  )
}
