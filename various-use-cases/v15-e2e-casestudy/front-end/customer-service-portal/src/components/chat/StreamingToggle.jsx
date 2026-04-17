import { useChat } from '../../context/ChatContext'

/**
 * Toggle switch to enable/disable streaming mode.
 * Phase 6 wires this to the actual streaming call logic.
 */
const StreamingToggle = () => {
  const { streamingEnabled, toggleStreaming } = useChat()

  return (
    <div
      className="d-flex align-items-center gap-2"
      title="Enable for real-time word-by-word responses"
    >
      <span className="text-muted small">Streaming</span>
      <label className="form-check form-switch mb-0">
        <input
          type="checkbox"
          className="form-check-input"
          role="switch"
          checked={streamingEnabled}
          onChange={toggleStreaming}
          id="streamingToggle"
          aria-label="Toggle streaming mode"
        />
      </label>
      <span className={`badge ${streamingEnabled ? 'bg-success-lt' : 'bg-secondary-lt'} small`}>
        {streamingEnabled ? 'ON' : 'OFF'}
      </span>
    </div>
  )
}

export default StreamingToggle
