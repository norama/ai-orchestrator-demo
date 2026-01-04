interface Props {
  label: string
  rationale?: string | null
}

export function Rationale({ label, rationale }: Props) {
  if (!rationale) {
    return null
  }
  return (
    <div className='mt-2 p-2 bg-green-100 border border-green-200 rounded'>
      <h4 className='font-medium mb-1'>{label}:</h4>
      <p className='whitespace-pre-wrap text-sm'>{rationale}</p>
    </div>
  )
}
