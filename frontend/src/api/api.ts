import { v4 as uuidv4 } from 'uuid'

const STORAGE_KEY = 'ai_orchestrator_workspace_id'

export function getWorkspaceId(): string {
  let ws = localStorage.getItem(STORAGE_KEY)
  if (!ws) {
    ws = `ws_${uuidv4()}`
    localStorage.setItem(STORAGE_KEY, ws)
  }
  return ws
}

export function resetWorkspace() {
  localStorage.removeItem(STORAGE_KEY)
}

export async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  const data = await res.json()
  return data as T
}

export async function apiGetRaw(path: string): Promise<Response> {
  const ws = getWorkspaceId()

  return await fetch(path, {
    method: 'GET',
    headers: {
      'X-Workspace-Id': ws,
    },
  })
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await apiGetRaw(path)

  return handleResponse<T>(response)
}

export async function apiPostRaw(path: string, body?: unknown): Promise<Response> {
  const ws = getWorkspaceId()

  return await fetch(path, {
    method: 'POST',
    headers: {
      'X-Workspace-Id': ws,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  })
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const response = await apiPostRaw(path, body)

  return handleResponse<T>(response)
}
