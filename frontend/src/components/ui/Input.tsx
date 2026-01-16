import React from 'react'

export const Input = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(function Input(props, ref) {
  return (
    <input
      ref={ref}
      {...props}
      className={[
        'w-full px-3 py-2 text-sm rounded',
        'border border-gray-300',
        'focus:outline-none focus:ring focus:ring-blue-300',
        'disabled:bg-gray-50 disabled:text-gray-500',
      ].join(' ')}
    />
  )
})
