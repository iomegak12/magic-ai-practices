import { BrowserRouter } from 'react-router-dom'
import AppRoutes from './routes/index.jsx'
import ThemeProvider from './features/theme/context/ThemeProvider.jsx'
import TenantProvider from './features/tenant/context/TenantProvider.jsx'

/**
 * Root application component.
 * Provider nesting order (outermost → innermost):
 *   ThemeProvider  → reads/writes localStorage, applies data-bs-theme to <html>
 *   TenantProvider → reads/writes localStorage, syncs Axios interceptor tenant ref
 *   BrowserRouter  → routing
 *
 * Ref: FRONTEND_ARCHITECTURE.md — Context Providers
 */
function App() {
  return (
    <ThemeProvider>
      <TenantProvider>
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <AppRoutes />
        </BrowserRouter>
      </TenantProvider>
    </ThemeProvider>
  )
}

export default App
