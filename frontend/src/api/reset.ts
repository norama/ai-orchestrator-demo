import { apiPost } from '@/api/api'
import { API_BASE_URL } from '@/api/constants'

export async function resetWorkspace() {
  return apiPost(`${API_BASE_URL}/workspace/reset`)
}
