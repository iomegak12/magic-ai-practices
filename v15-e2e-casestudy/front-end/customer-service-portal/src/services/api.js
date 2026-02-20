import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'

/**
 * Configured Axios instance for all MSAv15 API calls.
 * Base URL resolves to the backend service on port 9080.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30_000, // 30 seconds
})

// ── Request interceptor ──────────────────────────
api.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.debug(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ── Response interceptor ─────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(`[API] Error ${error.response.status}:`, error.response.data)
    } else if (error.request) {
      console.error('[API] Network error: No response received from server')
    } else {
      console.error('[API] Request setup error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api
