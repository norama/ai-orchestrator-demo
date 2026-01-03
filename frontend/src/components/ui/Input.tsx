export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={[
        'w-full px-3 py-2 text-sm rounded',
        'border border-gray-300',
        'focus:outline-none focus:ring focus:ring-blue-300',
        'disabled:bg-gray-50 disabled:text-gray-500',
      ].join(' ')}
    />
  )
}
