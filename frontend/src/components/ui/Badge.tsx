type BadgeVariant = 'neutral' | 'info' | 'success' | 'warning' | 'error'

const VARIANT_CLASS: Record<BadgeVariant, string> = {
  neutral: 'bg-gray-200 text-gray-700',
  info: 'bg-blue-100 text-blue-700',
  success: 'bg-green-100 text-green-700',
  warning: 'bg-yellow-100 text-yellow-800',
  error: 'bg-red-100 text-red-700',
}

export function Badge({
  children,
  className = '',
  variant = 'neutral',
  ...props
}: React.PropsWithChildren<React.HTMLAttributes<HTMLSpanElement> & { variant?: BadgeVariant }>) {
  return (
    <span
      {...props}
      className={[
        'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium',
        VARIANT_CLASS[variant],
        className,
      ].join(' ')}>
      {children}
    </span>
  )
}
