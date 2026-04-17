/**
 * ChatProvider — manages all chat + session state.
 *
 * Phase 3 responsibilities (preserved):
 *   • Lazy session creation on first send
 *   • Optimistic user-message insertion
 *   • 410 SESSION_EXPIRED recovery
 *
 * Phase 4 additions:
 *   • sessionList   — array fetched from GET /api/v1/sessions/
 *   • refreshSessions — re-fetches the session list (auto-called on tenant change)
 *   • switchToSession — loads history of an existing session from the backend
 *   • deleteSession   — deletes a session; resets state if it was the active one
 *
 * Phase 5 additions:
 *   • isStreaming      — true while SSE tokens are arriving
 *   • cancelStreaming  — abort an in-progress stream
 *   • sendMessage now auto-picks streaming when env.enableStreaming is true
 *
 * Ref: API_SPECIFICATION.md — Agent Operations + Session Management + Streaming Support
 *      FRONTEND_ARCHITECTURE.md — ChatContainer pattern
 */

import { useState, useCallback, useRef, useEffect } from 'react'
import { ChatContext } from './ChatContext.jsx'
import { createSession, sendMessage as apiSendMessage, sendMessageStream } from '../services/chatService.js'
import env from '@/core/config/env.js'
import {
  listSessions,
  getSessionHistory,
  deleteSession as apiDeleteSession,
} from '../services/sessionService.js'
import { useTenant } from '@/features/tenant/hooks/useTenant.js'
import logger from '@/core/utils/logger.js'

// ─── helpers ─────────────────────────────────────────────────────────────────

function newId() {
  return typeof crypto !== 'undefined'
    ? crypto.randomUUID()
    : String(Date.now() + Math.random())
}

function makeMessage(role, content, extra = {}) {
  return {
    id: newId(),
    role,       // 'user' | 'assistant' | 'error'
    content,
    timestamp: extra.timestamp ?? new Date().toISOString(),
    toolCalls: extra.toolCalls ?? null,
  }
}

/** Map backend SessionMessage → internal Message */
function mapHistoryMessage(msg) {
  return {
    id: newId(),
    role: msg.role === 'user' ? 'user' : 'assistant',
    content: msg.content,
    timestamp: msg.timestamp,
    toolCalls: msg.tool_calls ?? null,
  }
}

// ─── provider ────────────────────────────────────────────────────────────────

function ChatProvider({ children }) {
  const { currentTenant } = useTenant()
  const tenantId = currentTenant?.id ?? 'default'

  // ── chat state ──────────────────────────────────────────────────────────
  const [sessionId,         setSessionId]         = useState(null)
  const [messages,          setMessages]           = useState([])
  const [isLoading,         setIsLoading]          = useState(false)
  const [error,             setError]              = useState(null)

  // ── session list state ─────────────────────────────────────────────────
  const [sessionList,       setSessionList]        = useState([])
  const [isLoadingSessions, setIsLoadingSessions]  = useState(false)
  const [isLoadingHistory,  setIsLoadingHistory]   = useState(false)

  // ── streaming state (Phase 5) ───────────────────────────────────────────
  const [isStreaming, setIsStreaming] = useState(false)

  // Ref guard: avoids stale closures in send callbacks
  const sessionRef     = useRef(sessionId)
  sessionRef.current   = sessionId

  // Ref to the AbortController returned by sendMessageStream
  const abortStreamRef = useRef(null)

  // ── refreshSessions ─────────────────────────────────────────────────────
  const refreshSessions = useCallback(async () => {
    setIsLoadingSessions(true)
    try {
      const data = await listSessions(tenantId)
      // Sort newest first
      const sorted = [...(data.sessions ?? [])].sort(
        (a, b) => new Date(b.last_activity) - new Date(a.last_activity)
      )
      setSessionList(sorted)
    } catch (err) {
      logger.warn('[ChatProvider] could not load session list', err)
      // Non-blocking — don't surface to user
    } finally {
      setIsLoadingSessions(false)
    }
  }, [tenantId])

  // Auto-refresh session list when tenant changes
  useEffect(() => {
    refreshSessions()
  }, [refreshSessions])

  // ── ensureSession ───────────────────────────────────────────────────────
  const ensureSession = useCallback(async () => {
    if (sessionRef.current) return sessionRef.current

    logger.debug('[ChatProvider] creating new session', { tenantId })
    const data = await createSession(tenantId, { source: 'web-ui' })
    const id = data.session_id
    setSessionId(id)
    sessionRef.current = id
    return id
  }, [tenantId])

  // ── _sendMessageNormal (non-streaming fallback) ─────────────────────────
  const _sendMessageNormal = useCallback(async (trimmed, sid) => {
    try {
      const data = await apiSendMessage(sid, trimmed, tenantId)
      const assistantMsg = makeMessage('assistant', data.response, {
        toolCalls: data.metadata?.tool_calls ?? null,
      })
      setMessages(prev => [...prev, assistantMsg])
      refreshSessions()
    } catch (err) {
      logger.error('[ChatProvider] sendMessage (normal) error', err)
      if (err?.statusCode === 410 || err?.type === 'SESSION_EXPIRED') {
        setSessionId(null)
        sessionRef.current = null
        setMessages(prev => [
          ...prev,
          makeMessage('error', 'Session expired. A new session has been started — please resend your message.'),
        ])
      } else {
        setMessages(prev => [
          ...prev,
          makeMessage('error', err?.message ?? 'Something went wrong. Please try again.'),
        ])
        setError(err?.message ?? 'Failed to send message')
      }
    } finally {
      setIsLoading(false)
    }
  }, [tenantId, refreshSessions])

  // ── _sendMessageStreaming (SSE path) ─────────────────────────────────────
  const _sendMessageStreaming = useCallback(async (trimmed, sid) => {
    // Create a placeholder assistant message that will be updated in-place
    const placeholderId = newId()
    const placeholder = {
      ...makeMessage('assistant', ''),
      id:          placeholderId,
      isStreaming: true,
    }
    setMessages(prev => [...prev, placeholder])
    setIsStreaming(true)

    // Accumulated tool-call events
    const toolCallsAccum = []

    abortStreamRef.current = sendMessageStream(sid, trimmed, tenantId, {
      onStart: () => {
        logger.debug('[ChatProvider] stream started')
      },

      onChunk: (chunk) => {
        setMessages(prev =>
          prev.map(m =>
            m.id === placeholderId
              ? { ...m, content: m.content + chunk }
              : m
          )
        )
      },

      onToolCall: (evt) => {
        toolCallsAccum.push({ tool: evt.tool, status: evt.status })
        // Show a temporary tool-call indicator inside the bubble
        setMessages(prev =>
          prev.map(m =>
            m.id === placeholderId
              ? { ...m, toolCalls: [...toolCallsAccum] }
              : m
          )
        )
      },

      onToolResult: (evt) => {
        // Update the matching tool entry with the result status
        const idx = toolCallsAccum.findLastIndex?.(t => t.tool === evt.tool)
        if (idx !== undefined && idx >= 0) {
          toolCallsAccum[idx] = { ...toolCallsAccum[idx], status: evt.status }
        }
        setMessages(prev =>
          prev.map(m =>
            m.id === placeholderId
              ? { ...m, toolCalls: [...toolCallsAccum] }
              : m
          )
        )
      },

      onEnd: () => {
        // Finalise the bubble — strip isStreaming flag
        setMessages(prev =>
          prev.map(m =>
            m.id === placeholderId
              ? { ...m, isStreaming: false, toolCalls: toolCallsAccum.length ? toolCallsAccum : null }
              : m
          )
        )
        setIsStreaming(false)
        setIsLoading(false)
        abortStreamRef.current = null
        refreshSessions()
      },

      onError: (err) => {
        const is404 = err?.message?.includes('404') || err?.message?.includes('Not Found')

        if (is404) {
          // Streaming endpoint not yet implemented on backend — fall back silently
          logger.warn('[ChatProvider] stream endpoint unavailable (404) — falling back to normal send')
          // Remove the streaming placeholder bubble
          setMessages(prev => prev.filter(m => m.id !== placeholderId))
          setIsStreaming(false)
          abortStreamRef.current = null
          // Re-invoke the normal path (isLoading is still true)
          _sendMessageNormal(trimmed, sid)
          return
        }

        logger.error('[ChatProvider] stream error', err)
        setMessages(prev =>
          prev.map(m =>
            m.id === placeholderId
              ? { ...makeMessage('error', err?.message ?? 'Streaming failed. Please try again.'), id: placeholderId }
              : m
          )
        )
        setError(err?.message ?? 'Streaming failed')
        setIsStreaming(false)
        setIsLoading(false)
        abortStreamRef.current = null
      },
    })
  }, [tenantId, refreshSessions, _sendMessageNormal])

  // ── sendMessage (public — auto-picks streaming or normal) ────────────────
  const sendMessage = useCallback(async (text) => {
    const trimmed = text.trim()
    if (!trimmed || isLoading || isStreaming) return

    setError(null)
    setIsLoading(true)

    const userMsg = makeMessage('user', trimmed)
    setMessages(prev => [...prev, userMsg])

    let sid
    try {
      sid = await ensureSession()
    } catch (err) {
      logger.error('[ChatProvider] ensureSession error', err)
      setMessages(prev => [
        ...prev,
        makeMessage('error', err?.message ?? 'Could not create session. Please try again.'),
      ])
      setError(err?.message ?? 'Session creation failed')
      setIsLoading(false)
      return
    }

    if (env.enableStreaming) {
      // Streaming path — _sendMessageStreaming manages setIsLoading(false) itself
      await _sendMessageStreaming(trimmed, sid)
    } else {
      // Non-streaming fallback — _sendMessageNormal manages setIsLoading(false)
      await _sendMessageNormal(trimmed, sid)
    }
  }, [isLoading, isStreaming, ensureSession, _sendMessageStreaming, _sendMessageNormal])

  // ── cancelStreaming ──────────────────────────────────────────────────────
  const cancelStreaming = useCallback(() => {
    if (abortStreamRef.current) {
      abortStreamRef.current.abort()
      abortStreamRef.current = null
      setIsStreaming(false)
      setIsLoading(false)
      // Finalise whatever partial content exists in the streaming bubble
      setMessages(prev => prev.map(m => m.isStreaming ? { ...m, isStreaming: false } : m))
      logger.debug('[ChatProvider] stream cancelled by user')
    }
  }, [])

  // ── switchToSession — load history of an existing session ───────────────
  const switchToSession = useCallback(async (id) => {
    if (id === sessionRef.current) return   // already active

    setIsLoadingHistory(true)
    setError(null)
    setMessages([])

    try {
      const data = await getSessionHistory(id, tenantId)
      const mapped = (data.messages ?? []).map(mapHistoryMessage)
      setMessages(mapped)
      setSessionId(id)
      sessionRef.current = id
      logger.info('[ChatProvider] switched to session', { id, messageCount: mapped.length })
    } catch (err) {
      logger.error('[ChatProvider] switchToSession error', err)
      setError(`Could not load session history: ${err?.message ?? 'Unknown error'}`)
      // Leave sessionId unchanged so user can still send in their old session
    } finally {
      setIsLoadingHistory(false)
    }
  }, [tenantId])

  // ── deleteSession ────────────────────────────────────────────────────────
  const deleteSession = useCallback(async (id) => {
    try {
      await apiDeleteSession(id, tenantId)
      logger.info('[ChatProvider] deleted session', { id })

      // If the deleted session was active, reset the chat
      if (id === sessionRef.current) {
        setSessionId(null)
        sessionRef.current = null
        setMessages([])
        setError(null)
      }

      // Refresh the list
      await refreshSessions()
    } catch (err) {
      logger.error('[ChatProvider] deleteSession error', err)
      setError(`Could not delete session: ${err?.message ?? 'Unknown error'}`)
    }
  }, [tenantId, refreshSessions])

  // ── resetSession ────────────────────────────────────────────────────────
  const resetSession = useCallback(async () => {
    setSessionId(null)
    sessionRef.current = null
    setMessages([])
    setError(null)
    setIsLoading(false)
    logger.debug('[ChatProvider] session reset')
  }, [])

  // ── clearError ──────────────────────────────────────────────────────────
  const clearError = useCallback(() => setError(null), [])

  const value = {
    // Phase 3
    sessionId,
    messages,
    isLoading,
    error,
    sendMessage,
    resetSession,
    clearError,
    // Phase 4
    sessionList,
    isLoadingSessions,
    isLoadingHistory,
    refreshSessions,
    switchToSession,
    deleteSession,
    // Phase 5
    isStreaming,
    cancelStreaming,
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}

export default ChatProvider
