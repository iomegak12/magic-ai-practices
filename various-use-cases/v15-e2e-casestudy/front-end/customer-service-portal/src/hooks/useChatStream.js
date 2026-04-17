import { useState, useRef, useCallback } from 'react'
import { sendStreamingMessage } from '../services/chatService'

/**
 * Custom hook that manages SSE streaming state and lifecycle.
 *
 * @param {object} callbacks
 * @param {function} callbacks.onChunk  - (chunk: string) => void
 * @param {function} callbacks.onDone   - (metadata: object) => void
 * @param {function} callbacks.onError  - (error: string) => void
 */
export const useChatStream = ({ onChunk, onDone, onError }) => {
  const [isStreaming, setIsStreaming] = useState(false)
  const controllerRef = useRef(null)

  /**
   * Start a streaming request.
   * @param {string} message
   * @param {string|null} sessionId
   */
  const startStream = useCallback(
    (message, sessionId) => {
      setIsStreaming(true)

      const controller = sendStreamingMessage(
        message,
        sessionId,
        (chunk) => {
          onChunk(chunk)
        },
        (metadata) => {
          setIsStreaming(false)
          onDone(metadata)
        },
        (error) => {
          setIsStreaming(false)
          onError(error)
        }
      )

      controllerRef.current = controller
    },
    [onChunk, onDone, onError]
  )

  /** Abort an in-progress stream. */
  const stopStream = useCallback(() => {
    if (controllerRef.current) {
      controllerRef.current.abort()
      controllerRef.current = null
    }
    setIsStreaming(false)
  }, [])

  return { startStream, stopStream, isStreaming }
}
