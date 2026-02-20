import { Outlet } from 'react-router-dom'
import TopNavbar from './TopNavbar.jsx'
import Footer from './Footer.jsx'

/**
 * Main layout wrapper.
 * Renders the top navbar, the active page content (<Outlet />), and the footer.
 * Ref: FRONTEND_ARCHITECTURE.md — Layout Components
 */
function MainLayout() {
  return (
    <div className="wrapper">
      <TopNavbar />

      {/* Page content rendered by the matched child route */}
      <div className="page-wrapper">
        <Outlet />
      </div>

      <Footer />
    </div>
  )
}

export default MainLayout
