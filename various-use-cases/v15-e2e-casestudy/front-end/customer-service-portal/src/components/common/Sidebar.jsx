import { NavLink } from 'react-router-dom'
import { useUI } from '../../context/UIContext'

const NAV_ITEMS = [
  { path: '/',        label: 'Home',       icon: 'ti-home',         end: true },
  { path: '/about',   label: 'About Us',   icon: 'ti-info-circle'           },
  { path: '/contact', label: 'Contact Us', icon: 'ti-phone'                 },
  { path: '/support', label: 'Support',    icon: 'ti-message-chatbot'       },
]

/**
 * Collapsible vertical sidebar.
 * Default state: collapsed (icon-only rail, 4.5rem wide).
 * Expanded state: full-width with icons + labels (15rem).
 * State persists to localStorage via UIContext.
 */
const Sidebar = () => {
  const { sidebarCollapsed, toggleSidebar } = useUI()

  return (
    <aside
      className="navbar navbar-vertical navbar-expand-lg"
      data-bs-theme="dark"
      style={{
        width: sidebarCollapsed ? '4.5rem' : '15rem',
        minWidth: sidebarCollapsed ? '4.5rem' : '15rem',
        transition: 'width 0.22s ease, min-width 0.22s ease',
      }}
    >
      <div className="container-fluid flex-column align-items-stretch h-100 p-0">

        {/* ── Brand ─────────────────────────────────── */}
        <a
          className={`navbar-brand d-flex align-items-center py-3 sidebar-brand ${
            sidebarCollapsed ? 'justify-content-center px-0' : 'gap-2 px-3'
          }`}
          href="/"
          style={{ textDecoration: 'none' }}
        >
          <i className={`ti ti-headset text-azure flex-shrink-0 ${
            sidebarCollapsed ? 'fs-3' : 'fs-4'
          }`} />
          {!sidebarCollapsed && <span className="fw-bold">MSAv15</span>}
        </a>

        <div className="border-bottom border-white-10 mx-2 mb-1" />

        {/* ── Nav items ─────────────────────────────── */}
        <nav className="flex-grow-1 py-2" style={{ padding: '0 0.5rem' }}>
          {NAV_ITEMS.map(({ path, label, icon, end }) => (
            <NavLink
              key={path}
              to={path}
              end={end}
              title={sidebarCollapsed ? label : undefined}
              className={({ isActive }) =>
                sidebarCollapsed
                  ? `nav-link d-flex align-items-center justify-content-center mb-1${
                      isActive ? ' active' : ''
                    }`
                  : `nav-link d-flex align-items-center gap-2 mb-1${
                      isActive ? ' active' : ''
                    }`
              }
              style={sidebarCollapsed ? { padding: '0.6rem 0' } : undefined}
            >
              <i className={`ti ${icon} ${
                sidebarCollapsed ? 'fs-3' : 'fs-4'
              }`} />
              {!sidebarCollapsed && (
                <span className="nav-link-title">{label}</span>
              )}
            </NavLink>
          ))}
        </nav>

        {/* ── Collapse toggle ───────────────────────── */}
        <div className="border-top border-white-10 mx-2 mt-auto" />
        <button
          type="button"
          className={`sidebar-toggle-btn text-white-50 py-3 ${
            sidebarCollapsed ? 'justify-content-center px-0' : 'px-3'
          }`}
          onClick={toggleSidebar}
          title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <i
            className={`ti fs-4 ${
              sidebarCollapsed
                ? 'ti-layout-sidebar-right-expand'
                : 'ti-layout-sidebar-right-collapse'
            }`}
          />
          {!sidebarCollapsed && (
            <span className="small ms-1">Collapse</span>
          )}
        </button>

      </div>
    </aside>
  )
}

export default Sidebar
