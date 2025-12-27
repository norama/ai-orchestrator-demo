interface Props {
  confidence: number | null
}

export function Confidence({ confidence }: Props) {
  if (confidence === null) {
    return null
  }
  return <p className='text-sm text-gray-600'>Confidence: {(confidence * 100).toFixed(2)}%</p>
}
