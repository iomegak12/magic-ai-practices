import { useSessionManager } from '../../hooks/useSessionManager'
import { useChat } from '../../context/ChatContext'

/**
 * Button that creates a new chat session.
 */
const CreateSessionButton = () => {
  const { createSession } = useSessionManager()
  const { clearMessages, addMessage, MESSAGE_TYPES } = useChat()

  const handleCreate = () => {
    const session = createSession()
    clearMessages()
    addMessage({
      type: MESSAGE_TYPES.SYSTEM,
      content: `New session started · ID: ${session.id.slice(0, 8)}...`,
    })
  }

  return (
    <button
      type="button"
      className="btn btn-primary w-100 mb-3"
      onClick={handleCreate}
    >
      <i className="ti ti-plus me-2" />
      New Session
    </button>
  )
}

export default CreateSessionButton
