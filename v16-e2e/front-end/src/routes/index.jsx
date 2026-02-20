import { Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from '../shared/components/layout/MainLayout.jsx'
import HomePage from '../pages/HomePage.jsx'
import SupportPage from '../pages/SupportPage.jsx'
import AboutPage from '../pages/AboutPage.jsx'
import ContactPage from '../pages/ContactPage.jsx'
import SettingsPage from '../pages/SettingsPage.jsx'
import NotFoundPage from '../pages/NotFoundPage.jsx'

/**
 * Application route configuration.
 * All routes are wrapped in MainLayout (TopNavbar + Footer).
 * Ref: FRONTEND_ARCHITECTURE.md — Component Hierarchy
 */
function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/404" element={<NotFoundPage />} />
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
