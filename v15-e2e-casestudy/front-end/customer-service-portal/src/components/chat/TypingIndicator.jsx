/**
 * Animated "Agent is typing..." indicator shown while waiting for a response.
 */
const TypingIndicator = () => {
  return (
    <div className="d-flex justify-content-start mb-3">
      <div className="bg-light border p-3 rounded d-flex align-items-center gap-1">
        <span className="text-muted small me-2">AI Agent is typing</span>
        <span className="spinner-grow spinner-grow-sm text-secondary" style={{ animationDelay: '0ms' }} />
        <span className="spinner-grow spinner-grow-sm text-secondary" style={{ animationDelay: '150ms' }} />
        <span className="spinner-grow spinner-grow-sm text-secondary" style={{ animationDelay: '300ms' }} />
      </div>
    </div>
  )
}

export default TypingIndicator
