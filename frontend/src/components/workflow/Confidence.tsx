interface Props {
  label: string
  confidence: number | null
}

export function Confidence({ label, confidence }: Props) {
  if (confidence === null) {
    return null
  }
  return (
    <p className='text-sm text-gray-600'>
      {label}: {(confidence * 100).toFixed(2)}%
    </p>
  )
}
