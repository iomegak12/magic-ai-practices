import { useState, useCallback, useEffect } from 'react'
import { ThemeContext } from './ThemeContext.jsx'
import { THEMES, STORAGE_KEYS } from '../../../core/config/constants.js'
import storage from '../../../core/utils/storage.js'
import logger from '../../../core/utils/logger.js'

/**
 * ThemeProvider — manages light/dark theme state.
 *
 * - Reads persisted preference from localStorage on mount
 * - Applies `data-bs-theme` attribute to `<html>` element (Tabler convention)
 * - Persists changes to localStorage
 *
 * Ref: UI_COMPONENT_GUIDE.md — Design System → Theme Support (Dark/Light Mode)
 */
function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() => {
    const saved = storage.get(STORAGE_KEYS.THEME)
    // Respect OS preference if nothing saved
    if (!saved) {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      return prefersDark ? THEMES.DARK : THEMES.LIGHT
    }
    return saved === THEMES.DARK ? THEMES.DARK : THEMES.LIGHT
  })

  // Apply to <html> element so Tabler's Bootstrap 5 `data-bs-theme` works
  useEffect(() => {
    document.documentElement.setAttribute('data-bs-theme', theme)
    storage.set(STORAGE_KEYS.THEME, theme)
    logger.debug(`Theme set to "${theme}"`)
  }, [theme])

  const setTheme = useCallback((newTheme) => {
    if (newTheme === THEMES.LIGHT || newTheme === THEMES.DARK) {
      setThemeState(newTheme)
    }
  }, [])

  const toggleTheme = useCallback(() => {
    setThemeState((prev) =>
      prev === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT
    )
  }, [])

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme,
        setTheme,
        isDark: theme === THEMES.DARK,
      }}
    >
      {children}
    </ThemeContext.Provider>
  )
}

export default ThemeProvider
