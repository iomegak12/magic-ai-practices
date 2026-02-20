import { createContext, useContext, useState, useCallback } from 'react'
import { loadSessions, saveSessions, loadMessages, saveMessages, removeSession } from '../utils/sessionStorage'

const SessionContext = createContext(null)

/**
 * Custom hook to consume SessionContext.
 */
export const useSession = () => {
  const ctx = useContext(SessionContext)
  if (!ctx) throw new Error('useSession must be used within SessionProvider')
  return ctx
}

/**
 * Generates a simple UUID v4.
 */
const generateUUID = () =>
  'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16)
  })

export const SessionProvider = ({ children }) => {
  const [sessions, setSessions] = useState(() => loadSessions())
  const [activeSessionId, setActiveSessionId] = useState(
    () => loadSessions()[loadSessions().length - 1]?.id || null
  )

  /** Create a new session and make it active. */
  const createSession = useCallback(() => {
    const newSession = {
      id: generateUUID(),
      createdAt: new Date().toISOString(),
      lastMessageAt: new Date().toISOString(),
      turnCount: 0,
    }
    setSessions((prev) => {
      const updated = [...prev, newSession]
      saveSessions(updated)
      return updated
    })
    setActiveSessionId(newSession.id)
    return newSession
  }, [])

  /** Switch to an existing session. */
  const switchSession = useCallback((sessionId) => {
    setActiveSessionId(sessionId)
  }, [])

  /** Delete a session and its messages from storage. */
  const deleteSession = useCallback(
    (sessionId) => {
      removeSession(sessionId)
      setSessions((prev) => {
        const updated = prev.filter((s) => s.id !== sessionId)
        saveSessions(updated)
        return updated
      })
      if (activeSessionId === sessionId) {
        setSessions((prev) => {
          const remaining = prev.filter((s) => s.id !== sessionId)
          setActiveSessionId(remaining[remaining.length - 1]?.id || null)
          return remaining
        })
      }
    },
    [activeSessionId]
  )

  /** Update session metadata (turn count, last message time). */
  const updateSessionMetadata = useCallback((sessionId, metadata) => {
    setSessions((prev) => {
      const updated = prev.map((s) =>
        s.id === sessionId ? { ...s, ...metadata } : s
      )
      saveSessions(updated)
      return updated
    })
  }, [])

  /** Get the current active session object. */
  const getActiveSession = useCallback(() => {
    return sessions.find((s) => s.id === activeSessionId) || null
  }, [sessions, activeSessionId])

  /** Load messages for a session from localStorage. */
  const getSessionMessages = useCallback((sessionId) => {
    return loadMessages(sessionId)
  }, [])

  /** Persist messages for a session to localStorage. */
  const persistMessages = useCallback((sessionId, messages) => {
    saveMessages(sessionId, messages)
  }, [])

  return (
    <SessionContext.Provider
      value={{
        sessions,
        activeSessionId,
        createSession,
        switchSession,
        deleteSession,
        getActiveSession,
        updateSessionMetadata,
        getSessionMessages,
        persistMessages,
      }}
    >
      {children}
    </SessionContext.Provider>
  )
}

export default SessionContext
