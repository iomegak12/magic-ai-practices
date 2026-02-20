import api from './api'
import { API_BASE_URL } from '../utils/constants'

/**
 * Send a non-streaming chat message to the agent.
 *
 * @param {string} message   - The user's message text.
 * @param {string|null} sessionId - Existing session ID (null for new session).
 * @returns {Promise<import('../types').ChatResponse>}
 */
export const sendMessage = async (message, sessionId = null) => {
  const payload = {
    message,
    stream: false,
    ...(sessionId ? { session_id: sessionId } : {}),
  }
  const response = await api.post('/chat', payload)
  return response.data
}

/**
 * Send a streaming chat message via Server-Sent Events (SSE).
 * Uses fetch() + ReadableStream because EventSource only supports GET.
 *
 * NOTE: SSE contract is based on the PM specification. Pending formal
 * documentation from the backend team (see IMPLEMENTATION-PLAN.md - Drift #1).
 *
 * @param {string}   message    - The user's message text.
 * @param {string|null} sessionId - Existing session ID.
 * @param {function} onChunk   - Called with each text chunk: (chunk: string) => void
 * @param {function} onDone    - Called on completion: (metadata: object) => void
 * @param {function} onError   - Called on error: (error: string) => void
 * @returns {AbortController}  - Call `.abort()` to cancel the stream.
 */
export const sendStreamingMessage = (message, sessionId = null, onChunk, onDone, onError) => {
  const controller = new AbortController()
  const baseURL = import.meta.env.VITE_API_BASE_URL || API_BASE_URL

  const payload = {
    message,
    stream: true,
    ...(sessionId ? { session_id: sessionId } : {}),
  }

  ;(async () => {
    try {
      const response = await fetch(`${baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'text/event-stream',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        onError(errData?.detail || `HTTP error ${response.status}`)
        return
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() // hold incomplete line

        let currentEvent = null
        for (const line of lines) {
          if (line.startsWith('event:')) {
            currentEvent = line.replace('event:', '').trim()
          } else if (line.startsWith('data:')) {
            const raw = line.replace('data:', '').trim()
            try {
              const data = JSON.parse(raw)
              if (currentEvent === 'message') {
                onChunk(data.chunk || '')
              } else if (currentEvent === 'done') {
                // Pass the full data object so callers can access both
                // data.session_id (for session continuity) and data.metadata
                onDone(data)
                return
              } else if (currentEvent === 'error') {
                onError(data.error || 'Unknown streaming error')
                return
              }
            } catch {
              // ignore malformed SSE data lines
            }
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        onError(err.message || 'Streaming connection failed')
      }
    }
  })()

  return controller
}
