const API_BASE = 'http://localhost:8000'

export async function fetchWorkflows() {
  const res = await fetch(`${API_BASE}/workflows`)
  return res.json()
}

export async function fetchWorkflow(id: string) {
  const res = await fetch(`${API_BASE}/workflows/${id}`)
  return res.json()
}
