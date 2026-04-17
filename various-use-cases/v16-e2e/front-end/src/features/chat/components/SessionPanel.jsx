/**
 * SessionPanel — left-side sessions sidebar on the Support page.
 *
 * Features:
 *   • "New Chat" button (resets active session)
 *   • Search/filter by session ID
 *   • Sessions grouped: Today / Yesterday / Last 7 Days / Older
 *   • Loading skeleton while fetching
 *   • Empty state with help text
 *   • Delete session with two-click confirmation (handled inside SessionItem)
 *   • Highlights the currently active session
 *
 * Ref: UI_COMPONENT_GUIDE.md — Session Selector
 */

import { useState, useMemo, useCallback } from 'react'
import { useChat } from '../hooks/useChat.js'
import SessionItem from './SessionItem.jsx'

// ─── date-grouping helpers ────────────────────────────────────────────────────

function startOfDay(date) {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  return d.getTime()
}

function groupSessions(sessions) {
  const now      = Date.now()
  const todayStart     = startOfDay(now)
  const yesterdayStart = todayStart - 86_400_000
  const week7Start     = todayStart - 6 * 86_400_000

  const groups = { Today: [], Yesterday: [], 'Last 7 Days': [], Older: [] }

  for (const s of sessions) {
    const t = new Date(s.last_activity).getTime()
    if      (t >= todayStart)     groups['Today'].push(s)
    else if (t >= yesterdayStart) groups['Yesterday'].push(s)
    else if (t >= week7Start)     groups['Last 7 Days'].push(s)
    else                           groups['Older'].push(s)
  }

  return groups
}

// ─── skeleton ─────────────────────────────────────────────────────────────────

function SkeletonRow() {
  return (
    <div className="px-2 py-2 d-flex gap-2 align-items-start">
      <div className="rounded-circle bg-secondary-lt flex-shrink-0 mt-1" style={{ width: 8, height: 8 }} />
      <div className="flex-grow-1">
        <div className="rounded bg-secondary-lt mb-1" style={{ height: 10, width: '70%' }} />
        <div className="rounded bg-secondary-lt"       style={{ height: 8,  width: '40%' }} />
      </div>
    </div>
  )
}

// ─── main component ────────────────────────────────────────────────────────────

function SessionPanel() {
  const {
    sessionId,
    sessionList,
    isLoadingSessions,
    isLoadingHistory,
    refreshSessions,
    switchToSession,
    deleteSession,
    resetSession,
  } = useChat()

  const [query, setQuery] = useState('')

  // ── filter by search query ────────────────────────────────────────────────
  const filtered = useMemo(() => {
    if (!query.trim()) return sessionList
    const q = query.toLowerCase()
    return sessionList.filter(s => s.session_id.toLowerCase().includes(q))
  }, [sessionList, query])

  // ── group by date ─────────────────────────────────────────────────────────
  const groups = useMemo(() => groupSessions(filtered), [filtered])

  const handleNewChat = useCallback(async () => {
    await resetSession()
  }, [resetSession])

  const handleRefresh = useCallback(() => {
    refreshSessions()
  }, [refreshSessions])

  return (
    <div
      className="card shadow-sm d-flex flex-column h-100"
      style={{ minHeight: 360 }}
    >
      {/* ── HEADER ────────────────────────────────────────────────────── */}
      <div className="card-header py-2 px-3 d-flex align-items-center gap-2 flex-shrink-0">
        <i className="ti ti-layout-list text-primary" />
        <span className="fw-semibold flex-grow-1">Sessions</span>

        {/* Refresh */}
        <button
          type="button"
          className="btn btn-icon btn-sm btn-ghost-secondary"
          onClick={handleRefresh}
          disabled={isLoadingSessions}
          title="Refresh session list"
        >
          <i className={`ti ti-refresh ${isLoadingSessions ? 'ti-spin' : ''}`} />
        </button>
      </div>

      {/* ── NEW CHAT ──────────────────────────────────────────────────── */}
      <div className="px-3 pt-3 pb-2 flex-shrink-0">
        <button
          type="button"
          className="btn btn-primary w-100 d-flex align-items-center justify-content-center gap-2"
          onClick={handleNewChat}
        >
          <i className="ti ti-plus" />
          New Chat
        </button>
      </div>

      {/* ── SEARCH ────────────────────────────────────────────────────── */}
      <div className="px-3 pb-2 flex-shrink-0">
        <div className="input-group input-group-sm">
          <span className="input-group-text bg-transparent border-end-0">
            <i className="ti ti-search text-muted" />
          </span>
          <input
            type="search"
            className="form-control border-start-0 ps-0"
            placeholder="Search sessions…"
            value={query}
            onChange={e => setQuery(e.target.value)}
            aria-label="Search sessions"
          />
        </div>
      </div>

      {/* ── HISTORY-LOADING INDICATOR ─────────────────────────────────── */}
      {isLoadingHistory && (
        <div className="px-3 pb-2 flex-shrink-0">
          <div className="alert alert-info alert-sm py-1 px-2 mb-0 d-flex align-items-center gap-2"
            style={{ fontSize: '0.78rem' }}>
            <span className="spinner-border spinner-border-sm" />
            Loading conversation…
          </div>
        </div>
      )}

      {/* ── SESSION LIST ──────────────────────────────────────────────── */}
      <div className="flex-grow-1 overflow-y-auto px-2 pb-3">
        {/* Loading skeleton */}
        {isLoadingSessions && sessionList.length === 0 && (
          <>
            {[...Array(5)].map((_, i) => <SkeletonRow key={i} />)}
          </>
        )}

        {/* Empty state */}
        {!isLoadingSessions && filtered.length === 0 && (
          <div className="text-center text-muted py-5 px-2">
            <i className="ti ti-messages-off mb-2 d-block" style={{ fontSize: '2rem', opacity: 0.4 }} />
            <p className="small mb-1">
              {query ? 'No sessions match your search.' : 'No sessions yet.'}
            </p>
            {!query && (
              <p className="small" style={{ fontSize: '0.72rem' }}>
                Start a new chat to create one.
              </p>
            )}
          </div>
        )}

        {/* Grouped session items */}
        {Object.entries(groups).map(([label, items]) => {
          if (items.length === 0) return null
          return (
            <div key={label} className="mb-2">
              <div
                className="text-muted px-2 mb-1 fw-semibold"
                style={{ fontSize: '0.68rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}
              >
                {label}
              </div>
              {items.map(s => (
                <SessionItem
                  key={s.session_id}
                  session={s}
                  isActive={s.session_id === sessionId}
                  onSelect={switchToSession}
                  onDelete={deleteSession}
                />
              ))}
            </div>
          )
        })}
      </div>

      {/* ── FOOTER: total count ────────────────────────────────────────── */}
      {sessionList.length > 0 && (
        <div
          className="border-top px-3 py-2 text-muted text-center flex-shrink-0"
          style={{ fontSize: '0.7rem' }}
        >
          {sessionList.length} session{sessionList.length !== 1 ? 's' : ''} total
        </div>
      )}
    </div>
  )
}

export default SessionPanel
