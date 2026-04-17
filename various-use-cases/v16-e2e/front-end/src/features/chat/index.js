/**
 * Chat feature public API.
 * Import from here rather than from internal paths.
 *
 * Usage:
 *   import { ChatProvider, ChatView, SessionPanel, useChat } from '@/features/chat'
 */

export { default as ChatView }      from './components/ChatView.jsx'
export { default as SessionPanel }  from './components/SessionPanel.jsx'
export { default as ChatProvider }  from './context/ChatProvider.jsx'
export { useChat }                   from './hooks/useChat.js'
