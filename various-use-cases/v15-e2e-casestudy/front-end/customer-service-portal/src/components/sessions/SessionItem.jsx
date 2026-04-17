import { useState } from 'react'
import { useSessionManager } from '../../hooks/useSessionManager'
import { useChat } from '../../context/ChatContext'
import { formatRelativeTime } from '../../utils/dateFormatter'

/**
 * Single session list item with click-to-switch and delete.
 * @param {object} props
 * @param {object} props.session - Session object
 */
const SessionItem = ({ session }) => {
  const { activeSessionId, switchSession, deleteSession, getSessionMessages } = useSessionManager()
  const { loadMessages } = useChat()
  const [hovered, setHovered] = useState(false)

  const isActive = session.id === activeSessionId

  const handleSwitch = () => {
    if (isActive) return
    switchSession(session.id)
    const saved = getSessionMessages(session.id)
    loadMessages(saved)
  }

  const handleDelete = (e) => {
    e.stopPropagation()
    deleteSession(session.id)
  }

  const shortId = `Session ...${session.id.slice(-8)}`

  return (
    <div
      className={`list-group-item list-group-item-action d-flex justify-content-between align-items-start cursor-pointer ${
        isActive ? 'active' : ''
      }`}
      onClick={handleSwitch}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{ cursor: 'pointer' }}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && handleSwitch()}
      aria-pressed={isActive}
      aria-label={`Switch to ${shortId}`}
    >
      <div className="me-2 overflow-hidden">
        <div className="fw-semibold text-truncate small">{shortId}</div>
        <div className={`small ${isActive ? 'text-white-50' : 'text-muted'}`}>
          {session.turnCount > 0
            ? `${session.turnCount} turn${session.turnCount > 1 ? 's' : ''}`
            : 'No messages yet'}
          {session.lastMessageAt && (
            <span className="ms-2">{formatRelativeTime(session.lastMessageAt)}</span>
          )}
        </div>
      </div>

      {hovered && (
        <button
          type="button"
          className={`btn btn-sm btn-icon ${isActive ? 'btn-ghost-light' : 'btn-ghost-danger'}`}
          onClick={handleDelete}
          aria-label="Delete session"
          title="Delete session"
        >
          <i className="ti ti-trash" />
        </button>
      )}
    </div>
  )
}

export default SessionItem
