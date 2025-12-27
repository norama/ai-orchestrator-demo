export function Select(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className='w-full border rounded px-3 py-2 bg-white focus:outline-none focus:ring focus:ring-blue-300'
      {...props}
    />
  )
}
