import { Outlet } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'
import Footer from './Footer'
import { useUI } from '../../context/UIContext'

/**
 * Root layout wrapper.
 * Correct Tabler structure: <Sidebar /> is a sibling of <div.page-wrapper>,
 * NOT nested inside it — this allows Tabler CSS to manage margin-left correctly.
 */
const Layout = () => {
  const { sidebarCollapsed } = useUI()

  return (
    <div className={`page ${sidebarCollapsed ? 'sidebar-collapsed' : 'sidebar-expanded'}`}>
      <Sidebar />
      <div className="page-wrapper">
        <Header />
        <div className="page-body">
          <Outlet />
        </div>
        <Footer />
      </div>
    </div>
  )
}

export default Layout
