import { STORAGE_KEYS, MAX_SESSIONS } from './constants'

// ─────────────────────────────────────────────────
// Session list helpers
// ─────────────────────────────────────────────────

/**
 * Load all sessions from localStorage.
 * @returns {Array}
 */
export const loadSessions = () => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.SESSIONS) || '[]')
  } catch {
    return []
  }
}

/**
 * Persist sessions array to localStorage.
 * Enforces MAX_SESSIONS limit by removing oldest entries.
 * @param {Array} sessions
 */
export const saveSessions = (sessions) => {
  const trimmed = sessions.slice(-MAX_SESSIONS)
  localStorage.setItem(STORAGE_KEYS.SESSIONS, JSON.stringify(trimmed))
}

// ─────────────────────────────────────────────────
// Per-session message helpers
// ─────────────────────────────────────────────────

/**
 * Load messages for a specific session.
 * @param {string} sessionId
 * @returns {Array}
 */
export const loadMessages = (sessionId) => {
  try {
    const key = `${STORAGE_KEYS.MESSAGES_PREFIX}${sessionId}`
    return JSON.parse(localStorage.getItem(key) || '[]')
  } catch {
    return []
  }
}

/**
 * Persist messages for a specific session.
 * @param {string} sessionId
 * @param {Array} messages
 */
export const saveMessages = (sessionId, messages) => {
  const key = `${STORAGE_KEYS.MESSAGES_PREFIX}${sessionId}`
  localStorage.setItem(key, JSON.stringify(messages))
}

/**
 * Remove all stored data for a specific session.
 * @param {string} sessionId
 */
export const removeSession = (sessionId) => {
  const key = `${STORAGE_KEYS.MESSAGES_PREFIX}${sessionId}`
  localStorage.removeItem(key)
}
