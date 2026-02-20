import api from './api'
import { HEALTH_STATUS } from '../utils/constants'

/**
 * Check the health status of the MSAv15 backend service.
 *
 * @returns {Promise<import('../types').HealthResponse>}
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch {
    // Return a synthetic "unavailable" response so callers don't need to
    // handle both promise rejection and status checks separately.
    return {
      status: HEALTH_STATUS.UNAVAILABLE,
      service: 'MSAv15Service',
      version: 'unknown',
      timestamp: new Date().toISOString(),
      dependencies: {},
    }
  }
}
