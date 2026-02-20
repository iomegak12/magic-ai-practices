/**
 * ChatView — the top-level chat UI.
 * Smart container that consumes ChatContext and composes:
 *   • Chat header (session info + new-chat button)
 *   • MessageList (scrollable)
 *   • MessageInput (sticky bottom)
 *
 * Designed to fill the available vertical space on the Support page.
 *
 * Ref: UI_COMPONENT_GUIDE.md — Chat Interface → Layout Structure
 *      FRONTEND_ARCHITECTURE.md — ChatContainer pattern
 */

import { useCallback } from 'react'
import { useChat } from '../hooks/useChat.js'
import MessageList from './MessageList.jsx'
import MessageInput from './MessageInput.jsx'

function ChatView() {
  const {
    sessionId,
    messages,
    isLoading,
    isStreaming,
    error,
    sendMessage,
    resetSession,
    clearError,
    cancelStreaming,
  } = useChat()

  const handleNewChat = useCallback(async () => {
    if (messages.length === 0) return
    if (isStreaming) { cancelStreaming(); return }
    if (window.confirm('Start a new chat? The current conversation will be cleared.')) {
      await resetSession()
    }
  }, [messages.length, isStreaming, cancelStreaming, resetSession])

  return (
    <div
      className="card shadow-sm d-flex flex-column overflow-hidden"
      style={{ height: 'calc(100vh - 178px)', minHeight: 480 }}
    >
      {/* ── HEADER ─────────────────────────────────────────────────────────── */}
      <div
        className="card-header d-flex align-items-center gap-2 py-2 px-3 flex-shrink-0"
        style={{ borderBottom: '1px solid var(--tblr-border-color)' }}
      >
        {/* Bot icon */}
        <div className="avatar avatar-sm rounded-circle bg-primary d-flex align-items-center justify-content-center flex-shrink-0"
          style={{ width: 32, height: 32 }}>
          <i className="ti ti-robot text-white" style={{ fontSize: 16 }} />
        </div>

        {/* Title + session badge */}
        <div className="flex-grow-1 min-width-0">
          <div className="fw-semibold lh-1">Customer Service Agent</div>
          <div className="d-flex align-items-center gap-2 mt-1">
            {sessionId ? (
              <>
                <span className="badge bg-success-lt text-success d-inline-flex align-items-center gap-1"
                  style={{ fontSize: '0.68rem' }}>
                  <span
                    className="rounded-circle bg-success"
                    style={{ width: 6, height: 6, display: 'inline-block' }}
                  />
                  Session active
                </span>
                <span className="text-muted" style={{ fontSize: '0.68rem', fontFamily: 'monospace' }}>
                  {sessionId.slice(-10)}
                </span>
              </>
            ) : (
              <span
                className="badge bg-secondary-lt text-secondary d-inline-flex align-items-center gap-1"
                style={{ fontSize: '0.68rem' }}
              >
                <span
                  className="rounded-circle bg-secondary"
                  style={{ width: 6, height: 6, display: 'inline-block' }}
                />
                No active session
              </span>
            )}
          </div>
        </div>

        {/* Loading / Streaming indicator */}
        {isStreaming ? (
          <div className="d-flex align-items-center gap-2 flex-shrink-0">
            <span className="badge bg-success-lt text-success d-inline-flex align-items-center gap-1"
              style={{ fontSize: '0.68rem' }}>
              <span className="spinner-grow spinner-grow-sm text-success me-1"
                style={{ width: 6, height: 6 }} role="status" aria-hidden="true" />
              Streaming…
            </span>
            <button
              type="button"
              className="btn btn-sm btn-ghost-danger py-0 px-1"
              onClick={cancelStreaming}
              title="Cancel streaming response"
              style={{ fontSize: '0.72rem' }}
            >
              <i className="ti ti-square-rounded-x me-1" />
              Stop
            </button>
          </div>
        ) : isLoading ? (
          <div
            className="spinner-border spinner-border-sm text-primary flex-shrink-0"
            role="status"
            aria-label="Agent is responding"
          />
        ) : null}

        {/* New chat button */}
        <button
          type="button"
          className="btn btn-sm btn-outline-secondary flex-shrink-0"
          onClick={handleNewChat}
          disabled={messages.length === 0}
          title="Start a new conversation"
        >
          <i className="ti ti-plus me-1" />
          <span className="d-none d-sm-inline">New Chat</span>
        </button>
      </div>

      {/* ── ERROR ALERT ────────────────────────────────────────────────────── */}
      {error && (
        <div
          className="alert alert-danger alert-dismissible d-flex align-items-center gap-2 mb-0 rounded-0 py-2 px-3"
          role="alert"
          style={{ fontSize: '0.82rem', flexShrink: 0 }}
        >
          <i className="ti ti-alert-circle flex-shrink-0" />
          <span className="flex-grow-1">{error}</span>
          <button
            type="button"
            className="btn-close btn-sm"
            onClick={clearError}
            aria-label="Dismiss error"
          />
        </div>
      )}

      {/* ── MESSAGE LIST (flex-grow) ────────────────────────────────────────── */}
      <MessageList messages={messages} isLoading={isLoading} isStreaming={isStreaming} />

      {/* ── INPUT ──────────────────────────────────────────────────────────── */}
      <div className="flex-shrink-0">
        <MessageInput
          onSend={sendMessage}
          isLoading={isLoading || isStreaming}
          disabled={false}
        />
      </div>
    </div>
  )
}

export default ChatView
