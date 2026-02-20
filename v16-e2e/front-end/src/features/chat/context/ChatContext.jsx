/**
 * ChatContext — shape of the context consumed by useChat().
 *
 * Ref: FRONTEND_ARCHITECTURE.md — Chat feature context
 *
 * Context value (Phase 3):
 *   sessionId          {string|null}        - Active backend session ID
 *   messages           {Message[]}          - Ordered conversation history (oldest first)
 *   isLoading          {boolean}            - True while waiting for assistant response
 *   error              {string|null}        - Last error; cleared on next send
 *   sendMessage        {(text: string) => Promise<void>}
 *   resetSession       {() => Promise<void>} - Clears history + starts fresh session
 *   clearError         {() => void}
 *
 * Context value additions (Phase 4 — Session Management):
 *   sessionList        {SessionSummary[]}   - List of all backend sessions for tenant
 *   isLoadingSessions  {boolean}            - True while fetching session list
 *   isLoadingHistory   {boolean}            - True while loading a selected session's history
 *   refreshSessions    {() => Promise<void>} - Re-fetch session list from backend
 *   switchToSession    {(id: string) => Promise<void>} - Load history of an existing session
 *   deleteSession      {(id: string) => Promise<void>} - Delete a session + refresh list
 *
 * Message shape:
 *   { id, role: 'user'|'assistant'|'error', content, timestamp, toolCalls }
 *
 * SessionSummary shape (from backend):
 *   { session_id, tenant_id, message_count, created_at, last_activity }
 */

import { createContext, useContext } from 'react'

export const ChatContext = createContext(null)

/**
 * Convenience hook — must be called inside a ChatProvider.
 */
export function useChat() {
  const ctx = useContext(ChatContext)
  if (!ctx) throw new Error('useChat must be used within <ChatProvider>')
  return ctx
}
