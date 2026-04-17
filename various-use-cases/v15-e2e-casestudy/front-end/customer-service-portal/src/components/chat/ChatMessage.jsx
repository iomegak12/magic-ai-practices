import { MESSAGE_TYPES } from '../../utils/constants'
import { formatTime } from '../../utils/dateFormatter'

/**
 * Renders a single chat message bubble.
 * @param {object} props
 * @param {object} props.message - Message object from ChatContext
 */
const ChatMessage = ({ message }) => {
  const { type, content, timestamp, isError } = message

  if (type === MESSAGE_TYPES.SYSTEM) {
    return (
      <div className="text-center my-2">
        <span className="badge bg-secondary-lt text-secondary">{content}</span>
      </div>
    )
  }

  const isUser = type === MESSAGE_TYPES.USER

  return (
    <div className={`d-flex mb-3 ${isUser ? 'justify-content-end' : 'justify-content-start'}`}>
      <div style={{ maxWidth: '75%' }}>
        <div className={`small text-muted mb-1 ${isUser ? 'text-end' : ''}`}>
          {isUser ? 'You' : 'AI Agent'}
          {timestamp && <span className="ms-2">{formatTime(timestamp)}</span>}
        </div>
        <div
          className={`p-3 rounded ${
            isUser
              ? 'bg-primary text-white'
              : isError
              ? 'bg-danger-lt border border-danger text-danger'
              : 'bg-light border'
          }`}
          style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
        >
          {content}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
