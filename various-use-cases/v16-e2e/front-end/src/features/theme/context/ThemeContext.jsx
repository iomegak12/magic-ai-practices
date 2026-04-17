import { createContext, useContext } from 'react'
import { THEMES } from '../../../core/config/constants.js'

/**
 * ThemeContext — holds the active theme and the toggle function.
 *
 * Consumed via `useTheme()` hook (never import ThemeContext directly).
 * Ref: FRONTEND_ARCHITECTURE.md — State Management → ThemeContext
 */

export const ThemeContext = createContext({
  theme:       THEMES.LIGHT,
  toggleTheme: () => {},
  setTheme:    (_theme) => {},
  isDark:      false,
})

/** Hook — must be used inside ThemeProvider */
export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within a ThemeProvider')
  return ctx
}
