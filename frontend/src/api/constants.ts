export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

console.log('VITE_API_BASE_URL =', API_BASE_URL)

export const API_WORKFLOWS_URL = `${API_BASE_URL}/workflows`

export const API_CATALOG_URL = `${API_BASE_URL}/catalog`
