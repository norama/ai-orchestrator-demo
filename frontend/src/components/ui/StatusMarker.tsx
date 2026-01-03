type StatusVariant = 'idle' | 'pending' | 'success' | 'error'

const STATUS_CLASS: Record<StatusVariant, string> = {
  idle: 'bg-gray-100 text-gray-600',
  pending: 'bg-blue-50 text-blue-700',
  success: 'bg-green-50 text-green-700',
  error: 'bg-red-50 text-red-700',
}

export function StatusMarker({
  children,
  variant = 'idle',
  className = '',
}: React.PropsWithChildren<{ variant?: StatusVariant; className?: string }>) {
  return (
    <span
      className={[
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
        STATUS_CLASS[variant],
        className,
      ].join(' ')}>
      {children}
    </span>
  )
}
