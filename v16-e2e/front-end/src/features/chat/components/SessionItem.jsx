/**
 * SessionItem — a single row in the session list panel.
 *
 * Displays:
 *   • Relative timestamp (e.g. "2 min ago", "Yesterday")
 *   • Message count badge
 *   • Delete button (with confirm on hover)
 *   • Active highlight when this session is currently loaded
 *
 * Ref: UI_COMPONENT_GUIDE.md — Session Selector → Session Item Components
 */

import { useState, useCallback } from 'react'

// ─── relative time helper ────────────────────────────────────────────────────

function relativeTime(isoString) {
  try {
    const diff  = Date.now() - new Date(isoString).getTime()
    const mins  = Math.floor(diff / 60_000)
    const hours = Math.floor(diff / 3_600_000)
    const days  = Math.floor(diff / 86_400_000)

    if (mins  <  1)  return 'just now'
    if (mins  < 60)  return `${mins}m ago`
    if (hours < 24)  return `${hours}h ago`
    if (days  <  7)  return `${days}d ago`
    return new Date(isoString).toLocaleDateString([], { month: 'short', day: 'numeric' })
  } catch {
    return ''
  }
}

// ─── component ──────────────────────────────────────────────────────────────

function SessionItem({ session, isActive, onSelect, onDelete }) {
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  const handleDeleteClick = useCallback((e) => {
    e.stopPropagation()
    if (confirmingDelete) {
      onDelete(session.session_id)
      setConfirmingDelete(false)
    } else {
      setConfirmingDelete(true)
      // Auto-cancel after 3 seconds
      setTimeout(() => setConfirmingDelete(false), 3000)
    }
  }, [confirmingDelete, onDelete, session.session_id])

  const handleSelect = useCallback(() => {
    onSelect(session.session_id)
    setConfirmingDelete(false)
  }, [onSelect, session.session_id])

  return (
    <button
      type="button"
      onClick={handleSelect}
      className={`
        w-100 text-start border-0 rounded-2 px-3 py-2 mb-1 d-flex align-items-start gap-2
        ${isActive
          ? 'bg-primary-lt text-primary'
          : 'bg-transparent text-body hover-bg-light'}
      `}
      style={{ transition: 'background 0.15s', cursor: 'pointer' }}
      title={`Session ${session.session_id}`}
    >
      {/* Avatar dot */}
      <div
        className={`rounded-circle flex-shrink-0 mt-1 ${isActive ? 'bg-primary' : 'bg-secondary-lt'}`}
        style={{ width: 8, height: 8 }}
      />

      {/* Text block */}
      <div className="flex-grow-1 min-width-0 overflow-hidden">
        {/* Session ID (short) */}
        <div
          className={`fw-semibold small text-truncate lh-1 mb-1 ${isActive ? 'text-primary' : ''}`}
          style={{ fontFamily: 'monospace', fontSize: '0.72rem' }}
        >
          {session.session_id.length > 18
            ? `…${session.session_id.slice(-16)}`
            : session.session_id}
        </div>

        {/* Meta row: time + msg count */}
        <div className="d-flex align-items-center gap-2">
          <span className="text-muted" style={{ fontSize: '0.7rem' }}>
            <i className="ti ti-clock me-1" />
            {relativeTime(session.last_activity)}
          </span>
          {session.message_count > 0 && (
            <span
              className={`badge ${isActive ? 'bg-primary' : 'bg-secondary-lt text-secondary'}`}
              style={{ fontSize: '0.65rem', padding: '2px 6px' }}
            >
              {session.message_count}
            </span>
          )}
        </div>
      </div>

      {/* Delete button */}
      <button
        type="button"
        onClick={handleDeleteClick}
        className={`
          btn btn-icon btn-sm flex-shrink-0 border-0 p-0
          ${confirmingDelete
            ? 'text-danger bg-danger-lt rounded-1'
            : 'text-muted bg-transparent opacity-0 session-delete-btn'}
        `}
        title={confirmingDelete ? 'Click again to confirm delete' : 'Delete session'}
        style={{ width: 22, height: 22, fontSize: '0.8rem' }}
      >
        <i className={`ti ${confirmingDelete ? 'ti-trash-x' : 'ti-trash'}`} />
      </button>
    </button>
  )
}

export default SessionItem
