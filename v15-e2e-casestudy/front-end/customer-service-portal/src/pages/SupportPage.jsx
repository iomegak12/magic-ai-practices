import SessionList from '../components/sessions/SessionList'
import ChatWindow from '../components/chat/ChatWindow'
import ChatInput from '../components/chat/ChatInput'
import { useSession } from '../context/SessionContext'
import { formatDateTime } from '../utils/dateFormatter'

/**
 * Support page — main chat interface.
 * Left panel: session list + create button.
 * Right panel: chat window + input (or empty state when no session is active).
 */
const SupportPage = () => {
  const { sessions, activeSessionId } = useSession()
  const activeSession = sessions.find((s) => s.id === activeSessionId) ?? null

  return (
    <div className="container-xl h-100">
      {/* Page header */}
      <div className="page-header mb-3">
        <div className="row align-items-center">
          <div className="col-auto">
            <h2 className="page-title">
              <i className="ti ti-message-chatbot me-2 text-primary" />
              Support — Customer Service Agent
            </h2>
            <div className="text-muted mt-1">
              AI-powered assistant for orders and complaints
            </div>
          </div>
          {activeSession && (
            <div className="col-auto ms-auto">
              <span className="badge bg-green-lt px-3 py-2">
                <i className="ti ti-circle-filled me-1" style={{ fontSize: '0.5rem' }} />
                Active Session
              </span>
              <div className="text-muted small mt-1 text-end">
                Started {formatDateTime(activeSession.createdAt)}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main layout */}
      <div className="row g-3" style={{ height: 'calc(100vh - 220px)' }}>
        {/* Left panel: session list */}
        <div className="col-md-3 d-flex flex-column">
          <SessionList />
        </div>

        {/* Right panel: chat area */}
        <div className="col-md-9 d-flex flex-column">
          {activeSession ? (
            /* ── Active session: chat window + input ──────────────────── */
            <>
              <div className="flex-grow-1 overflow-hidden">
                <ChatWindow />
              </div>
              <div className="mt-2">
                <ChatInput />
              </div>
            </>
          ) : (
            /* ── No session selected: empty state ─────────────────────── */
            <div className="card flex-grow-1 d-flex align-items-center justify-content-center">
              <div className="card-body text-center py-5">
                <div
                  className="avatar avatar-xl mb-4 rounded"
                  style={{ background: 'linear-gradient(135deg, #206bc4, #4dabf7)' }}
                >
                  <i className="ti ti-message-chatbot text-white" style={{ fontSize: '2rem' }} />
                </div>
                <h3 className="mb-2">No Session Selected</h3>
                <p className="text-muted mb-4" style={{ maxWidth: 360, margin: '0 auto 1.5rem' }}>
                  Create a new session from the left panel to start chatting with
                  the AI-powered customer service agent.
                </p>
                <div className="row g-3 justify-content-center" style={{ maxWidth: 480, margin: '0 auto' }}>
                  <div className="col-auto">
                    <div className="d-flex align-items-center gap-2 text-muted small">
                      <i className="ti ti-messages text-primary" />
                      Multi-turn conversations
                    </div>
                  </div>
                  <div className="col-auto">
                    <div className="d-flex align-items-center gap-2 text-muted small">
                      <i className="ti ti-bolt text-warning" />
                      Streaming responses
                    </div>
                  </div>
                  <div className="col-auto">
                    <div className="d-flex align-items-center gap-2 text-muted small">
                      <i className="ti ti-device-floppy text-success" />
                      Session history saved
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SupportPage
