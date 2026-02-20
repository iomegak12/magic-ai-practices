/**
 * MessageItem — renders a single chat bubble.
 *
 * Roles:
 *   'user'      → right-aligned indigo bubble  (--chat-user-bg)
 *   'assistant' → left-aligned grey bubble     (--chat-assistant-bg)
 *   'error'     → left-aligned red/warning     (bg-danger-lt)
 *
 * Ref: UI_COMPONENT_GUIDE.md — Message Bubble Design
 */

import { useState, useCallback } from 'react'

// ─── helpers ─────────────────────────────────────────────────────────────────

function formatTime(iso) {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

// ─── component ───────────────────────────────────────────────────────────────

function MessageItem({ message }) {
  const { role, content, timestamp, toolCalls, isStreaming } = message
  const [copied, setCopied] = useState(false)

  const isUser      = role === 'user'
  const isAssistant = role === 'assistant'
  const isError     = role === 'error'

  const handleCopy = useCallback(() => {
    navigator.clipboard?.writeText(content).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    })
  }, [content])

  // ── user bubble ────────────────────────────────────────────────────────
  if (isUser) {
    return (
      <div className="d-flex flex-column align-items-end mb-3 px-1">
        <div className="d-flex align-items-start gap-2 flex-row-reverse" style={{ maxWidth: '78%' }}>
          {/* Avatar */}
          <div
            className="avatar avatar-sm rounded-circle bg-primary flex-shrink-0 d-flex align-items-center justify-content-center"
            style={{ width: 32, height: 32 }}
          >
            <i className="ti ti-user text-white" style={{ fontSize: 16 }} />
          </div>

          {/* Bubble */}
          <div
            className="px-3 py-2 rounded-3 shadow-sm"
            style={{
              background: 'var(--chat-user-bg)',
              color: 'var(--chat-user-text)',
              wordBreak: 'break-word',
              whiteSpace: 'pre-wrap',
              lineHeight: 1.55,
            }}
          >
            {content}
          </div>
        </div>
        {/* Timestamp */}
        <small className="text-muted mt-1 me-5" style={{ fontSize: '0.7rem' }}>
          {formatTime(timestamp)}
        </small>
      </div>
    )
  }

  // ── assistant bubble ────────────────────────────────────────────────────
  if (isAssistant) {
    return (
      <div className="d-flex flex-column align-items-start mb-3 px-1">
        <div className="d-flex align-items-start gap-2" style={{ maxWidth: '82%' }}>
          {/* Avatar */}
          <div
            className="avatar avatar-sm rounded-circle bg-primary-lt flex-shrink-0 d-flex align-items-center justify-content-center"
            style={{ width: 32, height: 32 }}
          >
            <i className="ti ti-robot text-primary" style={{ fontSize: 16 }} />
          </div>

          {/* Bubble */}
          <div
            className="px-3 py-2 rounded-3 shadow-sm"
            style={{
              background: 'var(--chat-assistant-bg)',
              color: 'var(--chat-assistant-text)',
              wordBreak: 'break-word',
              whiteSpace: 'pre-wrap',
              lineHeight: 1.6,
            }}
          >
            {/* If streaming with no content yet — show pulsing dots */}
            {isStreaming && !content ? (
              <span className="streaming-placeholder d-inline-flex gap-1 align-items-center" aria-label="Agent is responding">
                <span className="typing-dot" />
                <span className="typing-dot" style={{ animationDelay: '0.18s' }} />
                <span className="typing-dot" style={{ animationDelay: '0.36s' }} />
              </span>
            ) : (
              <>
                {content}
                {/* Blinking cursor while tokens are arriving */}
                {isStreaming && (
                  <span className="streaming-cursor" aria-hidden="true">▋</span>
                )}
              </>
            )}

            {/* Tool calls pill row */}
            {toolCalls && toolCalls.length > 0 && (
              <div className="d-flex flex-wrap gap-1 mt-2">
                {toolCalls.map((tc, i) => {
                  // Support both string (legacy) and object { tool, status } (Phase 5)
                  const toolName   = typeof tc === 'string' ? tc : tc.tool
                  const toolStatus = typeof tc === 'string' ? null : tc.status
                  const iconClass  = toolStatus === 'completed'
                    ? 'ti-check text-success'
                    : toolStatus === 'failed'
                      ? 'ti-x text-danger'
                      : 'ti-loader-2 text-muted'
                  return (
                    <span
                      key={`${toolName}-${i}`}
                      className="badge bg-purple-lt text-purple d-inline-flex align-items-center gap-1"
                      style={{ fontSize: '0.68rem' }}
                    >
                      <i className={`ti ${toolStatus !== null ? iconClass : 'ti-tool'}`} style={{ fontSize: '0.7rem' }} />
                      {toolName}
                    </span>
                  )
                })}
              </div>
            )}
          </div>
        </div>

        {/* Timestamp + copy action */}
        <div className="d-flex align-items-center gap-2 mt-1 ms-5">
          <small className="text-muted" style={{ fontSize: '0.7rem' }}>
            {formatTime(timestamp)}
          </small>
          <button
            type="button"
            className="btn btn-ghost-secondary btn-icon btn-sm p-0"
            onClick={handleCopy}
            title="Copy response"
            style={{ width: 20, height: 20, fontSize: '0.72rem' }}
          >
            <i className={`ti ${copied ? 'ti-check text-success' : 'ti-copy'}`} />
          </button>
        </div>
      </div>
    )
  }

  // ── error / system bubble ───────────────────────────────────────────────
  if (isError) {
    return (
      <div className="d-flex justify-content-center mb-3 px-1">
        <div
          className="d-inline-flex align-items-start gap-2 px-3 py-2 rounded-3 text-danger bg-danger-lt"
          style={{ maxWidth: '80%', fontSize: '0.85rem', wordBreak: 'break-word' }}
        >
          <i className="ti ti-alert-circle flex-shrink-0 mt-1" />
          <span>{content}</span>
        </div>
      </div>
    )
  }

  return null
}

export default MessageItem
