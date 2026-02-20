import { useSession } from '../context/SessionContext'

/**
 * Convenience hook that exposes session management operations
 * with a flat, component-friendly API.
 */
export const useSessionManager = () => {
  const {
    sessions,
    activeSessionId,
    createSession,
    switchSession,
    deleteSession,
    getActiveSession,
    updateSessionMetadata,
    getSessionMessages,
    persistMessages,
  } = useSession()

  const activeSession = getActiveSession()

  return {
    sessions,
    activeSessionId,
    activeSession,
    createSession,
    switchSession,
    deleteSession,
    updateSessionMetadata,
    getSessionMessages,
    persistMessages,
  }
}
