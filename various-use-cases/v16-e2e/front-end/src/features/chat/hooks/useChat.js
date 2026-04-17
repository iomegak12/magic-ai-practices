/**
 * useChat — re-export of the chat context hook.
 * Provides access to ChatContext.sendMessage, messages, isLoading, etc.
 *
 * Usage:
 *   import { useChat } from '@/features/chat/hooks/useChat.js'
 *   const { messages, sendMessage, isLoading } = useChat()
 */
export { useChat } from '../context/ChatContext.jsx'
