/**
 * chatService — API wrappers for the agent chat endpoints.
 * All calls go through the singleton Axios instance (interceptors + retry attached).
 *
 * Ref: API_SPECIFICATION.md — Agent Operations
 *   POST /api/v1/agent/sessions         → createSession
 *   POST /api/v1/agent/messages         → sendMessage
 *   POST /api/v1/agent/messages/stream  → sendMessageStream (SSE)
 */

import apiClient from '@/core/api/client.js'
import { ENDPOINTS } from '@/core/config/endpoints.js'
import env from '@/core/config/env.js'
import logger from '@/core/utils/logger.js'

/**
 * Create a new conversation session.
 * @param {string}  tenantId   - Tenant identifier (default: 'default')
 * @param {object}  metadata   - Optional extra metadata forwarded to the backend
 * @returns {Promise<{ session_id: string, status: string, created_at: string }>}
 */
export async function createSession(tenantId = 'default', metadata = {}) {
  logger.debug('[chatService] createSession', { tenantId })

  const res = await apiClient.post(ENDPOINTS.AGENT_CREATE_SESSION, {
    tenant_id: tenantId,
    metadata: { channel: 'web', ...metadata },
  })

  logger.info('[chatService] session created', { sessionId: res.data?.session_id })
  return res.data
}

/**
 * Send a user message in an existing session.
 * @param {string} sessionId  - Target session ID
 * @param {string} message    - User message text (max 10 000 chars)
 * @param {string} tenantId   - Tenant identifier
 * @returns {Promise<{ session_id: string, response: string, status: string, metadata: object }>}
 */
export async function sendMessage(sessionId, message, tenantId = 'default') {
  logger.debug('[chatService] sendMessage', { sessionId, tenantId, length: message.length })

  const res = await apiClient.post(ENDPOINTS.AGENT_SEND_MESSAGE, {
    session_id: sessionId,
    message,
    tenant_id: tenantId,
    stream: false,
  })

  logger.info('[chatService] message response received', {
    sessionId,
    toolCalls: res.data?.metadata?.tool_calls,
    ms: res.data?.metadata?.processing_time_ms,
  })

  return res.data
}

/**
 * Send a user message and consume the response as an SSE stream.
 * Uses native `fetch` + `ReadableStream` because EventSource only supports GET.
 *
 * @param {string} sessionId  - Target session ID
 * @param {string} message    - User message text
 * @param {string} tenantId   - Tenant identifier
 * @param {object} callbacks  - Event handlers
 * @param {function} [callbacks.onStart]      - ({ session_id }) → void
 * @param {function} [callbacks.onChunk]      - (chunkText: string) → void
 * @param {function} [callbacks.onToolCall]   - ({ tool, status }) → void
 * @param {function} [callbacks.onToolResult] - ({ tool, status }) → void
 * @param {function} [callbacks.onEnd]        - ({ session_id, total_chunks }) → void
 * @param {function} [callbacks.onError]      - (Error) → void
 * @returns {AbortController}  — call .abort() to cancel mid-stream
 */
export function sendMessageStream(sessionId, message, tenantId = 'default', callbacks = {}) {
  const { onStart, onChunk, onToolCall, onToolResult, onEnd, onError } = callbacks
  const controller = new AbortController()
  const url = env.apiBaseURL + ENDPOINTS.AGENT_SEND_MESSAGE_STREAM

  logger.debug('[chatService] sendMessageStream start', { sessionId, tenantId, length: message.length })

  // Run the fetch + SSE parse loop asynchronously so we can return the controller immediately.
  ;(async () => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
          'X-Tenant-ID': tenantId,
          'X-Request-ID': crypto.randomUUID(),
          'Cache-Control': 'no-cache',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message,
          tenant_id: tenantId,
        }),
        signal: controller.signal,
      })

      if (!response.ok) {
        const errText = await response.text().catch(() => response.statusText)
        throw new Error(`Stream request failed: ${response.status} – ${errText}`)
      }

      const reader  = response.body.getReader()
      const decoder = new TextDecoder()
      let   buffer  = ''

      // eslint-disable-next-line no-constant-condition
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })

        // Split on newlines; hold back the last (possibly incomplete) chunk
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const raw = line.slice(6).trim()
          if (!raw || raw === '[DONE]') continue

          let evt
          try { evt = JSON.parse(raw) } catch { continue }

          switch (evt.type) {
            case 'start':
              logger.debug('[chatService] stream start', evt)
              onStart?.(evt)
              break
            case 'chunk':
              onChunk?.(evt.content ?? '')
              break
            case 'tool_call':
              logger.debug('[chatService] stream tool_call', evt)
              onToolCall?.(evt)
              break
            case 'tool_result':
              logger.debug('[chatService] stream tool_result', evt)
              onToolResult?.(evt)
              break
            case 'end':
              logger.info('[chatService] stream end', evt)
              onEnd?.(evt)
              break
            case 'error':
              onError?.(new Error(evt.error ?? evt.detail ?? 'Streaming error'))
              break
            default:
              break
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        logger.error('[chatService] sendMessageStream error', err)
        onError?.(err)
      } else {
        logger.debug('[chatService] stream aborted by caller')
      }
    }
  })()

  return controller
}
