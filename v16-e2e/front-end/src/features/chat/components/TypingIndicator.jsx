/**
 * TypingIndicator — animated three-dot pulse shown whilst the assistant is thinking.
 * Uses `.typing-dot` keyframes defined in src/index.css.
 *
 * Ref: UI_COMPONENT_GUIDE.md — Typing Indicator
 */
function TypingIndicator() {
  return (
    <div className="d-flex align-items-start gap-2 mb-3 px-1" aria-label="Assistant is typing">
      {/* Bot avatar */}
      <div
        className="avatar avatar-sm rounded-circle bg-primary-lt flex-shrink-0 d-flex align-items-center justify-content-center"
        style={{ width: 32, height: 32 }}
      >
        <i className="ti ti-robot text-primary" style={{ fontSize: 16 }} />
      </div>

      {/* Dot bubble */}
      <div
        className="d-inline-flex align-items-center gap-1 px-3 py-2 rounded-3"
        style={{ background: 'var(--chat-assistant-bg)', minHeight: 36 }}
      >
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </div>
  )
}

export default TypingIndicator
