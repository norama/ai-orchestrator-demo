export function Textarea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className='w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-300'
      {...props}
    />
  )
}
