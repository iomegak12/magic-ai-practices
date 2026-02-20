import { useEffect, useState } from 'react'
import { checkHealth } from '../../services/healthService'
import { HEALTH_POLL_INTERVAL, HEALTH_STATUS } from '../../utils/constants'
import { useUI } from '../../context/UIContext'

/**
 * Top navbar with health status, dark/light theme toggle, and sidebar toggle.
 */
const Header = () => {
  const [health, setHealth] = useState(null)
  const { theme, toggleTheme, toggleSidebar } = useUI()

  const fetchHealth = async () => {
    const data = await checkHealth()
    setHealth(data)
  }

  useEffect(() => {
    fetchHealth()
    const interval = setInterval(fetchHealth, HEALTH_POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [])

  const getStatusColor = () => {
    if (!health) return 'secondary'
    if (health.status === HEALTH_STATUS.HEALTHY) return 'success'
    if (health.status === HEALTH_STATUS.DEGRADED) return 'warning'
    return 'danger'
  }

  const getStatusLabel = () => {
    if (!health) return 'Checking...'
    if (health.status === HEALTH_STATUS.HEALTHY) return 'Operational'
    if (health.status === HEALTH_STATUS.DEGRADED) return 'Degraded'
    return 'Unavailable'
  }

  const isUnavailable = health && health.status === HEALTH_STATUS.UNAVAILABLE

  return (
    <>
      <header className="navbar navbar-expand-md d-print-none">
        <div className="container-xl">

          {/* Sidebar toggle (hamburger) */}
          <button
            type="button"
            className="btn btn-icon me-2"
            onClick={toggleSidebar}
            title="Toggle sidebar"
            aria-label="Toggle sidebar"
          >
            <i className="ti ti-menu-2" />
          </button>

          {/* Page title / brand */}
          <a href="/" className="navbar-brand pe-0 pe-md-3 text-decoration-none">
            <span className="fw-bold text-primary">MSAv15 Portal</span>
          </a>

          <div className="navbar-nav flex-row order-md-last ms-auto gap-2 align-items-center">

            {/* Health status badge */}
            <div className="d-flex align-items-center">
              <span
                className={`badge bg-${getStatusColor()}-lt`}
                title={`Service: ${health?.service || 'MSAv15Service'} | Version: ${health?.version || '...'}`}
              >
                <span className={`status-dot status-dot-animated bg-${getStatusColor()} me-1`} />
                {getStatusLabel()}
              </span>
            </div>

            {/* API version */}
            {health?.version && health.version !== 'unknown' && (
              <span className="text-muted small d-none d-md-inline">
                v{health.version}
              </span>
            )}

            {/* Dark / Light theme toggle */}
            <button
              type="button"
              className="btn btn-icon"
              onClick={toggleTheme}
              title={theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme'}
              aria-label="Toggle theme"
            >
              <i className={`ti ${theme === 'light' ? 'ti-moon' : 'ti-sun'}`} />
            </button>

          </div>
        </div>
      </header>

      {/* Offline / unavailable banner */}
      {isUnavailable && (
        <div
          className="alert alert-danger alert-dismissible mb-0 py-2 rounded-0 text-center small"
          role="alert"
          style={{ borderRadius: 0 }}
        >
          <i className="ti ti-wifi-off me-2" />
          <strong>Backend unavailable</strong> — The service cannot be reached.
          Chat features are disabled until the connection is restored.
          <button
            type="button"
            className="btn-close btn-sm"
            aria-label="Retry"
            onClick={fetchHealth}
          />
        </div>
      )}
    </>
  )
}

export default Header
