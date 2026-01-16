import { apiPostRaw } from '@/api/api'
import { API_WORKFLOWS_URL } from '@/api/constants'

interface SSEHandlers {
  onChunk: (text: string) => void
  onDone: () => void
  onError?: (error: string) => void
}

export async function postSSE(path: string, body: unknown, handlers: SSEHandlers) {
  const res = await apiPostRaw(`${API_WORKFLOWS_URL}/${path}`, body)

  if (!res.ok || !res.body) {
    handlers.onError?.(`HTTP ${res.status}`)
    return
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()

  let buffer = ''
  let event = ''
  let dataLines: string[] = []

  const flush = async () => {
    const data = dataLines.join('\n')
    if (event === 'chunk') handlers.onChunk(data)
    if (event === 'done') handlers.onDone()
    if (event === 'error') handlers.onError?.(data)
    event = ''
    dataLines = []
  }

  while (true) {
    const { value, done } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })

    let idx
    while ((idx = buffer.indexOf('\n\n')) !== -1) {
      const raw = buffer.slice(0, idx)
      buffer = buffer.slice(idx + 2)

      for (const line of raw.split('\n')) {
        if (line.startsWith('event:')) {
          event = line.slice(6).trim()
        } else if (line.startsWith('data:')) {
          try {
            const data = line.slice(5)
            const json = JSON.parse(data) as { text: string }
            dataLines.push(json.text)
          } catch {
            handlers.onError?.(`Invalid SSE payload: ${line}`)
          }
        }
      }
      await flush()
    }
  }
}
