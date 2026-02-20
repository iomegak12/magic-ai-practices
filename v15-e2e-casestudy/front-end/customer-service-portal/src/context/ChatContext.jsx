import { createContext, useContext, useState, useCallback, useRef } from 'react'
import { MESSAGE_TYPES } from '../utils/constants'
import { sendMessage as apiSendMessage, sendStreamingMessage as apiSendStreaming } from '../services/chatService'
import { saveMessages } from '../utils/sessionStorage'
import { useSession } from './SessionContext'

/**
 * Parse API errors into a human-readable string.
 * Handles FastAPI 422 HTTPValidationError (detail is an array) and plain strings.
 * Addresses Drift #4 — only 422 is formally defined; handle all non-2xx gracefully.
 */
const parseApiError = (err) => {
  const detail = err?.response?.data?.detail
  if (Array.isArray(detail)) {
    // 422 HTTPValidationError: [{loc, msg, type}, ...]
    const parts = detail.map((d) => {
      const field = Array.isArray(d?.loc) ? d.loc.slice(1).join('.') : ''
      return field ? `${field}: ${d.msg}` : (d.msg ?? String(d))
    })
    return parts.join('; ') || 'Validation error'
  }
  if (typeof detail === 'string' && detail) return detail
  if (err?.response?.status === 500) return 'Internal server error. Please try again later.'
  if (err?.response?.status === 503) return 'Service unavailable. The backend is not responding.'
  return err?.message ?? 'Request failed. Please try again.'
}

const ChatContext = createContext(null)

/**
 * Custom hook to consume ChatContext.
 */
export const useChat = () => {
  const ctx = useContext(ChatContext)
  if (!ctx) throw new Error('useChat must be used within ChatProvider')
  return ctx
}

/** Generates a simple unique message ID. */
const generateId = () => `msg_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [streamingEnabled, setStreamingEnabled] = useState(false)

  // messagesRef mirrors state so async callbacks always have the latest array
  const messagesRef = useRef([])

  // Track the last user message text so errors can offer a one-click retry
  const lastUserMessageRef = useRef('')

  // SessionContext — ChatProvider is mounted inside SessionProvider so this is safe
  const { sessions, activeSessionId, updateSessionMetadata } = useSession()
  const activeSession = sessions.find((s) => s.id === activeSessionId) ?? null

  /**
   * State + ref updater so async callbacks can read the latest messages
   * without stale closure issues.
   */
  const syncMessages = useCallback((updater) => {
    setMessages((prev) => {
      const next = typeof updater === 'function' ? updater(prev) : updater
      messagesRef.current = next
      return next
    })
  }, [])

  /** Add a single message object to the chat. Returns the new message. */
  const addMessage = useCallback(
    (message) => {
      const newMessage = {
        id: generateId(),
        timestamp: new Date().toISOString(),
        ...message,
      }
      syncMessages((prev) => [...prev, newMessage])
      return newMessage
    },
    [syncMessages]
  )

  /**
   * Append a text chunk to an in-progress agent message during SSE streaming.
   */
  const appendChunk = useCallback(
    (chunk, streamMessageId) => {
      syncMessages((prev) => {
        const idx = prev.findIndex((m) => m.id === streamMessageId)
        if (idx === -1) return prev
        const updated = [...prev]
        updated[idx] = { ...updated[idx], content: updated[idx].content + chunk }
        return updated
      })
    },
    [syncMessages]
  )

  /** Clear all messages (e.g. when creating a new session). */
  const clearMessages = useCallback(() => {
    messagesRef.current = []
    setMessages([])
    setError(null)
  }, [])

  /** Load messages from localStorage when switching sessions. */
  const loadMessages = useCallback(
    (messagesArray) => {
      const arr = messagesArray || []
      messagesRef.current = arr
      syncMessages(arr)
      setError(null)
    },
    [syncMessages]
  )

  /** Toggle streaming on/off. */
  const toggleStreaming = useCallback(() => setStreamingEnabled((prev) => !prev), [])

  /**
   * Master send orchestrator — called by ChatInput.
   *
   * Non-streaming: POST /chat  → response.data.response
   * Streaming:     POST /chat  → SSE chunks via fetch + ReadableStream
   *
   * After every exchange the messages are persisted to localStorage and
   * the session metadata (turnCount, lastMessageAt) is updated.
   */
  const sendMessage = useCallback(
    async (text) => {
      const trimmed = text?.trim()
      if (!trimmed || isLoading) return

      // Use the backend-assigned session_id if we have one (Drift #2: opaque string).
      // On first turn this is null → backend creates a new session → we store its ID.
      const sessionId = activeSession?.backendSessionId ?? activeSession?.id ?? null

      // Store for retry
      lastUserMessageRef.current = trimmed

      // ── User message ──────────────────────────────────────────────────────
      addMessage({ type: MESSAGE_TYPES.USER, content: trimmed })
      setIsLoading(true)
      setError(null)

      if (!streamingEnabled) {
        // ── Non-streaming path ─────────────────────────────────────────────
        try {
          const data = await apiSendMessage(trimmed, sessionId)
          const agentContent = data?.response ?? data?.message ?? '(no response)'

          addMessage({
            type: MESSAGE_TYPES.AGENT,
            content: agentContent,
          })

          // Persist + update session metadata (including backend session_id for continuity)
          if (activeSession?.id) {
            saveMessages(activeSession.id, messagesRef.current)
            updateSessionMetadata(activeSession.id, {
              lastMessageAt: new Date().toISOString(),
              turnCount:
                data?.metadata?.turn_count ?? (activeSession.turnCount ?? 0) + 1,
              // Store backend-assigned session_id so subsequent turns use it (Drift #2)
              ...(data?.session_id ? { backendSessionId: data.session_id } : {}),
            })
          }
        } catch (err) {
          const msg = parseApiError(err)
          setError(msg)
          addMessage({ type: MESSAGE_TYPES.SYSTEM, content: `⚠ ${msg}` })
        } finally {
          setIsLoading(false)
        }
      } else {
        // ── Streaming path ─────────────────────────────────────────────────
        const placeholder = addMessage({ type: MESSAGE_TYPES.AGENT, content: '' })

        apiSendStreaming(
          trimmed,
          sessionId,
          // onChunk
          (chunk) => appendChunk(chunk, placeholder.id),
          // onDone — finalData is the full SSE done payload: { session_id, metadata }
          (finalData) => {
            setIsLoading(false)
            if (activeSession?.id) {
              saveMessages(activeSession.id, messagesRef.current)
              updateSessionMetadata(activeSession.id, {
                lastMessageAt: new Date().toISOString(),
                turnCount:
                  finalData?.metadata?.turn_count ??
                  (activeSession.turnCount ?? 0) + 1,
                // Store backend session_id for continuity on next turn (Drift #2)
                ...(finalData?.session_id ? { backendSessionId: finalData.session_id } : {}),
              })
            }
          },
          // onError
          (errMsg) => {
            setIsLoading(false)
            const msg = errMsg ?? 'Stream interrupted. Please try again.'
            setError(msg)
            // Replace the empty placeholder with an error indicator
            syncMessages((prev) => {
              const idx = prev.findIndex((m) => m.id === placeholder.id)
              if (idx === -1) return prev
              const updated = [...prev]
              updated[idx] = {
                ...updated[idx],
                content: `⚠ ${msg}`,
                isError: true,
              }
              return updated
            })
          }
        )
      }
    },
    [
      isLoading,
      streamingEnabled,
      activeSession,
      addMessage,
      appendChunk,
      syncMessages,
      updateSessionMetadata,
    ]
  )

  /** Resend the last user message — used by the Retry button in ChatWindow. */
  const retryLastMessage = useCallback(() => {
    const last = lastUserMessageRef.current
    if (last) sendMessage(last)
  }, [sendMessage])

  return (
    <ChatContext.Provider
      value={{
        messages,
        isLoading,
        error,
        streamingEnabled,
        addMessage,
        appendChunk,
        clearMessages,
        loadMessages,
        toggleStreaming,
        sendMessage,
        retryLastMessage,
        setError,
        setIsLoading,
        MESSAGE_TYPES,
      }}
    >
      {children}
    </ChatContext.Provider>
  )
}

export default ChatContext
