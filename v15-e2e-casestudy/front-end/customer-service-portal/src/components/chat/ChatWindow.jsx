import { useEffect, useRef } from 'react'
import { useChat } from '../../context/ChatContext'
import ChatMessage from './ChatMessage'
import TypingIndicator from './TypingIndicator'

/**
 * Scrollable chat message list.
 * Auto-scrolls to the bottom on every new message or streaming chunk.
 */
const ChatWindow = () => {
  const { messages, isLoading, error, setError, retryLastMessage } = useChat()
  const bottomRef = useRef(null)

  // Auto-scroll to bottom whenever messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div
      className="card h-100"
      style={{ display: 'flex', flexDirection: 'column' }}
    >
      <div className="card-header">
        <h3 className="card-title">
          <i className="ti ti-message-chatbot me-2 text-primary" />
          Conversation
        </h3>
      </div>

      <div
        className="card-body overflow-auto"
        style={{ flex: '1 1 auto', minHeight: 0 }}
      >
        {messages.length === 0 && !isLoading && (
          <div className="text-center text-muted py-5">
            <i className="ti ti-message-plus fs-1 mb-3 d-block" />
            <p>No messages yet. Start a conversation!</p>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {isLoading && <TypingIndicator />}

        {error && (
          <div className="alert alert-danger d-flex align-items-center gap-2">
            <i className="ti ti-alert-circle flex-shrink-0" />
            <div className="flex-grow-1 small">{error}</div>
            <button
              type="button"
              className="btn btn-sm btn-danger"
              onClick={() => { setError(null); retryLastMessage() }}
              title="Resend the last message"
            >
              <i className="ti ti-refresh me-1" />
              Retry
            </button>
            <button
              type="button"
              className="btn-close"
              aria-label="Dismiss error"
              onClick={() => setError(null)}
            />
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  )
}

export default ChatWindow
