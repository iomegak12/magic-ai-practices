/**
 * sessionService — API wrappers for session management endpoints.
 *
 * Ref: API_SPECIFICATION.md — Session Management
 *   GET  /api/v1/sessions/                     → listSessions
 *   GET  /api/v1/sessions/{id}/history          → getSessionHistory
 *   DELETE /api/v1/sessions/{id}?tenant_id=...  → deleteSession
 */

import apiClient from '@/core/api/client.js'
import { ENDPOINTS } from '@/core/config/endpoints.js'
import logger from '@/core/utils/logger.js'

/**
 * List all sessions for a tenant (most-recent first).
 * @param {string} tenantId
 * @param {{ limit?: number, offset?: number }} opts
 * @returns {Promise<{ sessions: SessionSummary[], total: number }>}
 */
export async function listSessions(tenantId = 'default', { limit = 50, offset = 0 } = {}) {
  logger.debug('[sessionService] listSessions', { tenantId, limit, offset })

  const res = await apiClient.get(ENDPOINTS.SESSIONS_LIST, {
    params: { tenant_id: tenantId, limit, offset },
  })

  logger.info('[sessionService] sessions loaded', { count: res.data?.sessions?.length ?? 0 })
  return res.data
}

/**
 * Fetch the full conversation history for one session.
 * @param {string} sessionId
 * @param {string} tenantId
 * @returns {Promise<SessionHistoryResponse>}
 */
export async function getSessionHistory(sessionId, tenantId = 'default') {
  logger.debug('[sessionService] getSessionHistory', { sessionId, tenantId })

  const res = await apiClient.get(ENDPOINTS.SESSION_HISTORY(sessionId), {
    params: { tenant_id: tenantId },
  })

  logger.info('[sessionService] history loaded', {
    sessionId,
    messageCount: res.data?.message_count,
  })
  return res.data
}

/**
 * Delete a session and all its messages.
 * @param {string} sessionId
 * @param {string} tenantId
 * @returns {Promise<{ session_id: string, message: string }>}
 */
export async function deleteSession(sessionId, tenantId = 'default') {
  logger.debug('[sessionService] deleteSession', { sessionId, tenantId })

  const res = await apiClient.delete(ENDPOINTS.SESSION_DELETE(sessionId), {
    params: { tenant_id: tenantId },
  })

  logger.info('[sessionService] session deleted', { sessionId })
  return res.data
}
