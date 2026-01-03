type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger'

const VARIANT_CLASS: Record<ButtonVariant, string> = {
  primary: `
    bg-blue-600 text-white
    enabled:hover:bg-blue-700
  `,
  secondary: `
    bg-gray-100 text-gray-800
    enabled:hover:bg-gray-200
  `,
  ghost: `
    bg-transparent text-gray-600
    enabled:hover:bg-gray-100
  `,
  danger: `
    bg-red-600 text-white
    enabled:hover:bg-red-700
  `,
}

export function Button({
  children,
  className = '',
  variant = 'primary',
  ...props
}: React.PropsWithChildren<
  React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: ButtonVariant }
>) {
  return (
    <button
      {...props}
      className={[
        'px-4 py-2 rounded text-sm font-medium',
        'enabled:cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed',
        VARIANT_CLASS[variant],
        className,
      ].join(' ')}>
      {children}
    </button>
  )
}
