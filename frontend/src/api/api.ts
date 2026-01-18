export async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  const data = await res.json()
  return data as T
}

export async function apiGetRaw(path: string): Promise<Response> {
  return await fetch(path, {
    method: 'GET',
    credentials: 'include',
  })
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await apiGetRaw(path)

  return handleResponse<T>(response)
}

export async function apiPostRaw(path: string, body?: unknown): Promise<Response> {
  return await fetch(path, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  })
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const response = await apiPostRaw(path, body)

  return handleResponse<T>(response)
}
