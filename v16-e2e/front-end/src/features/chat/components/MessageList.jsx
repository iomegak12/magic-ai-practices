/**
 * MessageList — scrollable container for all chat bubbles.
 *
 * Behaviour:
 *   • Automatically scrolls to the bottom when a new message arrives.
 *   • Shows a "↓ New messages" FAB when the user has scrolled up.
 *
 * Ref: UI_COMPONENT_GUIDE.md — Message List
 */

import { useEffect, useRef, useState, useCallback } from 'react'
import MessageItem from './MessageItem.jsx'
import TypingIndicator from './TypingIndicator.jsx'

function MessageList({ messages, isLoading, isStreaming = false }) {
  const bottomRef    = useRef(null)
  const containerRef = useRef(null)
  const [showScrollBtn, setShowScrollBtn] = useState(false)

  // ── auto-scroll to bottom on new message ───────────────────────────────
  const scrollToBottom = useCallback((behaviour = 'smooth') => {
    bottomRef.current?.scrollIntoView({ behavior: behaviour })
    setShowScrollBtn(false)
  }, [])

  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    const isNearBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight < 200
    if (isNearBottom) {
      scrollToBottom('smooth')
    } else {
      setShowScrollBtn(true)
    }
  }, [messages.length, isLoading, scrollToBottom])

  // ── track scroll position to show/hide jump button ─────────────────────
  const handleScroll = useCallback(() => {
    const container = containerRef.current
    if (!container) return
    const distFromBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight
    setShowScrollBtn(distFromBottom > 200)
  }, [])

  // ── empty state ────────────────────────────────────────────────────────
  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4 text-muted">
        <i className="ti ti-message-chatbot mb-3" style={{ fontSize: '3rem', opacity: 0.35 }} />
        <p className="mb-1 fw-semibold">No messages yet</p>
        <p className="small">Type a message below to start chatting with the agent.</p>
      </div>
    )
  }

  return (
    <div className="position-relative flex-grow-1 overflow-hidden">
      {/* Scrollable message area */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="h-100 overflow-y-auto overflow-x-hidden p-3"
        style={{ scrollBehavior: 'smooth' }}
      >
        {messages.map(msg => (
          <MessageItem key={msg.id} message={msg} />
        ))}

        {/* Typing indicator whilst loading — hidden during streaming (placeholder bubble shows dots instead) */}
        {isLoading && !isStreaming && <TypingIndicator />}

        {/* Invisible anchor for auto-scroll */}
        <div ref={bottomRef} style={{ height: 1 }} />
      </div>

      {/* Jump-to-bottom FAB */}
      {showScrollBtn && (
        <button
          type="button"
          onClick={() => scrollToBottom('smooth')}
          className="btn btn-primary btn-sm rounded-circle shadow position-absolute"
          title="Scroll to latest message"
          style={{
            bottom: 12,
            right: 16,
            width: 36,
            height: 36,
            padding: 0,
            zIndex: 10,
            lineHeight: 1,
          }}
        >
          <i className="ti ti-arrow-down" />
        </button>
      )}
    </div>
  )
}

export default MessageList
