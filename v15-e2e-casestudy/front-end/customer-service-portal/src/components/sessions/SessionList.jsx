import { useSessionManager } from '../../hooks/useSessionManager'
import CreateSessionButton from './CreateSessionButton'
import SessionItem from './SessionItem'

/**
 * Left-panel session list with create button and scrollable session items.
 */
const SessionList = () => {
  const { sessions } = useSessionManager()

  return (
    <div className="card h-100 d-flex flex-column">
      <div className="card-header">
        <h3 className="card-title">
          <i className="ti ti-messages me-2 text-primary" />
          Sessions
        </h3>
      </div>
      <div className="card-body d-flex flex-column p-2">
        <CreateSessionButton />

        {sessions.length === 0 ? (
          <div className="text-center text-muted py-4 small">
            <i className="ti ti-inbox fs-2 d-block mb-2" />
            No sessions yet.
            <br />
            Click &ldquo;New Session&rdquo; to start.
          </div>
        ) : (
          <div className="list-group list-group-flush overflow-auto flex-grow-1">
            {[...sessions].reverse().map((session) => (
              <SessionItem key={session.id} session={session} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default SessionList
