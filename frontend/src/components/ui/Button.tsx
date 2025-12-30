export function Button({
  children,
  className = '',
  ...props
}: React.PropsWithChildren<React.ButtonHTMLAttributes<HTMLButtonElement>>) {
  return (
    <button
      {...props}
      className={`
        px-4 py-2 rounded
        bg-blue-600 text-white
        enabled:hover:bg-blue-700
        enabled:cursor-pointer
        disabled:opacity-50
        disabled:cursor-not-allowed
        ${className}
      `}>
      {children}
    </button>
  )
}
