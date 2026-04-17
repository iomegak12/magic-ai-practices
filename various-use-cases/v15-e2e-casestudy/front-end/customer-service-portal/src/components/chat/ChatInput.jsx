import { useState, useRef } from 'react'
import { useChat } from '../../context/ChatContext'
import { useSession } from '../../context/SessionContext'
import StreamingToggle from './StreamingToggle'

/**
 * Chat message input area with textarea, streaming toggle, and send button.
 * Calls ChatContext.sendMessage() which routes to non-streaming or SSE path.
 */
const ChatInput = () => {
  const [inputValue, setInputValue] = useState('')
  const { isLoading, sendMessage } = useChat()
  const { activeSessionId } = useSession()
  const textareaRef = useRef(null)

  const hasSession = !!activeSessionId
  const canSend = inputValue.trim().length > 0 && !isLoading && hasSession

  const handleSend = async () => {
    if (!canSend) return
    const text = inputValue.trim()
    setInputValue('')
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
    await sendMessage(text)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleInput = (e) => {
    setInputValue(e.target.value)
    // Auto-expand textarea up to 150px
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = `${Math.min(el.scrollHeight, 150)}px`
    }
  }

  return (
    <div className="card">
      <div className="card-body pb-2 pt-2">
        {/* Streaming toggle row */}
        <div className="d-flex justify-content-end mb-2">
          <StreamingToggle />
        </div>

        {/* No-session hint */}
        {!hasSession && (
          <div className="text-muted small text-center mb-2">
            <i className="ti ti-info-circle me-1" />
            Create or select a session to start chatting.
          </div>
        )}

        {/* Input row */}
        <div className="d-flex gap-2 align-items-end">
          <textarea
            ref={textareaRef}
            className="form-control"
            placeholder={
              hasSession
                ? 'Type your message here… (Enter to send, Shift+Enter for new line)'
                : 'No session selected'
            }
            value={inputValue}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            disabled={isLoading || !hasSession}
            rows={1}
            style={{ resize: 'none', overflow: 'hidden', maxHeight: '150px' }}
            aria-label="Chat message input"
          />
          <button
            type="button"
            className="btn btn-primary"
            onClick={handleSend}
            disabled={!canSend}
            aria-label="Send message"
          >
            {isLoading ? (
              <span className="spinner-border spinner-border-sm" role="status" />
            ) : (
              <i className="ti ti-send" />
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatInput
