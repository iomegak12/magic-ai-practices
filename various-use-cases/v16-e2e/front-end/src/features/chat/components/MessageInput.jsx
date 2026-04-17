/**
 * MessageInput — auto-resizing textarea with send controls.
 *
 * Behaviour:
 *   • Enter → send  |  Shift+Enter → newline
 *   • Auto-resizes from 2 to 8 rows as the user types
 *   • Disabled while isLoading (prevent duplicate sends)
 *   • Character counter appears when message length > 4 800
 *   • Max length enforced at 10 000 chars (API limit)
 *
 * Ref: UI_COMPONENT_GUIDE.md — Message Input
 */

import { useState, useRef, useCallback, useEffect } from 'react'

const MAX_CHARS  = 10_000
const WARN_CHARS = 4_800
const MIN_ROWS   = 2
const MAX_ROWS   = 8
const LINE_HEIGHT = 22 // px per row (approx — matches 0.875rem * 1.6 line-height)

function MessageInput({ onSend, isLoading, disabled }) {
  const [text, setText]     = useState('')
  const textareaRef         = useRef(null)

  // ── auto-resize ─────────────────────────────────────────────────────────
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    const scrollH = el.scrollHeight
    const minH    = MIN_ROWS * LINE_HEIGHT + 20
    const maxH    = MAX_ROWS * LINE_HEIGHT + 20
    el.style.height = `${Math.min(Math.max(scrollH, minH), maxH)}px`
  }, [text])

  // ── send ─────────────────────────────────────────────────────────────────
  const handleSend = useCallback(() => {
    const trimmed = text.trim()
    if (!trimmed || isLoading || disabled) return
    onSend(trimmed)
    setText('')
    // Reset height
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
  }, [text, isLoading, disabled, onSend])

  // ── keyboard: Enter = send, Shift+Enter = newline ────────────────────────
  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }, [handleSend])

  const charCount    = text.length
  const overWarn     = charCount > WARN_CHARS
  const overLimit    = charCount >= MAX_CHARS
  const canSend      = text.trim().length > 0 && !isLoading && !disabled && !overLimit

  return (
    <div
      className="border-top px-3 pt-3 pb-3"
      style={{ background: 'var(--tblr-bg-surface, var(--bs-body-bg, #fff))' }}
    >
      {/* Character warning */}
      {overWarn && (
        <div className={`text-end mb-1 small ${overLimit ? 'text-danger fw-semibold' : 'text-warning'}`}>
          {charCount.toLocaleString()} / {MAX_CHARS.toLocaleString()}
        </div>
      )}

      <div className="d-flex align-items-end gap-2">
        {/* Textarea */}
        <textarea
          ref={textareaRef}
          className="form-control resize-none"
          placeholder="Type your message… (Shift+Enter for new line)"
          value={text}
          onChange={e => setText(e.target.value.slice(0, MAX_CHARS))}
          onKeyDown={handleKeyDown}
          disabled={isLoading || disabled}
          maxLength={MAX_CHARS}
          rows={MIN_ROWS}
          style={{ resize: 'none', lineHeight: `${LINE_HEIGHT}px`, transition: 'height 0.1s ease' }}
          aria-label="Message input"
        />

        {/* Send button */}
        <button
          type="button"
          className="btn btn-primary flex-shrink-0 d-flex align-items-center justify-content-center"
          style={{ width: 44, height: 44, padding: 0 }}
          onClick={handleSend}
          disabled={!canSend}
          title="Send message (Enter)"
          aria-label="Send message"
        >
          {isLoading
            ? <span className="spinner-border spinner-border-sm" role="status" />
            : <i className="ti ti-send" style={{ fontSize: '1.1rem' }} />
          }
        </button>
      </div>

      {/* Hint */}
      <div className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>
        <kbd>Enter</kbd> to send &nbsp;·&nbsp; <kbd>Shift+Enter</kbd> for a new line
      </div>
    </div>
  )
}

export default MessageInput
