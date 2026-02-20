import { NavLink, useLocation } from 'react-router-dom'
import { NAV_LINKS } from '../../../core/config/constants.js'
import ThemeToggle from '../../../features/theme/components/ThemeToggle.jsx'
import TenantIndicator from '../../../features/tenant/components/TenantIndicator.jsx'

/**
 * Top navigation bar.
 * Uses Tabler's .navbar component built on Bootstrap 5.
 *
 * Slots reserved for Phase 2:
 *   - ThemeToggle  (src/features/theme/components/ThemeToggle.jsx)
 *   - TenantSelector (src/features/tenant/components/TenantSelector.jsx)
 *   - HealthIndicator (src/features/health/components/HealthIndicator.jsx)
 *
 * Ref: UI_COMPONENT_GUIDE.md — Navigation
 * Ref: FRONTEND_ARCHITECTURE.md — Component Hierarchy → TopNavbar
 */
function TopNavbar() {
  const location = useLocation()

  return (
    <header className="navbar navbar-expand-md navbar-light d-print-none">
      <div className="container-xl">

        {/* ── Brand / Logo ──────────────────────────────── */}
        <NavLink to="/" className="navbar-brand">
          <span className="navbar-brand-text fw-bold text-primary">
            <i className="ti ti-robot me-2" />
            CS Agent
          </span>
        </NavLink>

        {/* ── Mobile toggle ─────────────────────────────── */}
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbar-menu"
          aria-controls="navbar-menu"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        {/* ── Nav links ─────────────────────────────────── */}
        <div className="collapse navbar-collapse" id="navbar-menu">
          <ul className="navbar-nav me-auto">
            {NAV_LINKS.map(({ label, path, icon }) => (
              <li key={path} className="nav-item">
                <NavLink
                  to={path}
                  end={path === '/'}
                  className={({ isActive }) =>
                    `nav-link ${isActive ? 'active' : ''}`
                  }
                >
                  <span className="nav-link-icon">
                    <i className={`ti ${icon}`} />
                  </span>
                  <span className="nav-link-title">{label}</span>
                </NavLink>
              </li>
            ))}
          </ul>

          {/* ── Right-side controls ────────────────────────── */}
          <div className="navbar-nav ms-auto d-flex align-items-center gap-2">

            {/* Phase 7: <HealthIndicator /> */}
            {/* Phase 6: <TenantSelector /> (full dropdown — TenantIndicator is Phase 2 stub) */}

            <TenantIndicator />
            <ThemeToggle />

            {/* Placeholder user avatar */}
            <div className="nav-item dropdown">
              <a
                href="#"
                className="nav-link d-flex lh-1 text-reset p-0"
                data-bs-toggle="dropdown"
                aria-label="Open user menu"
              >
                <span className="avatar avatar-sm bg-primary-lt">
                  <i className="ti ti-user" />
                </span>
              </a>
              <div className="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
                <a href="#" className="dropdown-item">Profile</a>
                <div className="dropdown-divider" />
                <a href="#" className="dropdown-item text-danger">Sign out</a>
              </div>
            </div>
          </div>
        </div>

      </div>
    </header>
  )
}

export default TopNavbar
