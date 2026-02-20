import { createContext, useContext, useState, useCallback, useEffect } from 'react'

const UIContext = createContext(null)

export const useUI = () => {
  const ctx = useContext(UIContext)
  if (!ctx) throw new Error('useUI must be used within UIProvider')
  return ctx
}

const SIDEBAR_KEY = 'msav15_sidebar'
const THEME_KEY   = 'msav15_theme'

export const UIProvider = ({ children }) => {
  // Sidebar: default collapsed
  const [sidebarCollapsed, setSidebarCollapsed] = useState(
    () => localStorage.getItem(SIDEBAR_KEY) !== 'expanded'
  )

  // Theme: default light
  const [theme, setTheme] = useState(
    () => localStorage.getItem(THEME_KEY) || 'light'
  )

  // Apply theme to <html> so Tabler's data-bs-theme picks it up
  useEffect(() => {
    document.documentElement.setAttribute('data-bs-theme', theme)
    localStorage.setItem(THEME_KEY, theme)
  }, [theme])

  const toggleSidebar = useCallback(() => {
    setSidebarCollapsed((prev) => {
      const next = !prev
      localStorage.setItem(SIDEBAR_KEY, next ? 'collapsed' : 'expanded')
      return next
    })
  }, [])

  const toggleTheme = useCallback(() => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }, [])

  return (
    <UIContext.Provider value={{ sidebarCollapsed, toggleSidebar, theme, toggleTheme }}>
      {children}
    </UIContext.Provider>
  )
}

export default UIContext
