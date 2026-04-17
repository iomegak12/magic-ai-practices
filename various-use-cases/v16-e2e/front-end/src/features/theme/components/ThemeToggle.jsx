import { useTheme } from '../hooks/useTheme.js'
import { THEMES } from '../../../core/config/constants.js'

/**
 * ThemeToggle — sun/moon icon button in the TopNavbar.
 *
 * Toggles between light and dark Tabler themes.
 * Ref: UI_COMPONENT_GUIDE.md — Navigation
 */
function ThemeToggle() {
  const { theme, toggleTheme, isDark } = useTheme()

  return (
    <button
      type="button"
      className="nav-link btn btn-icon"
      onClick={toggleTheme}
      aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDark
        ? <i className="ti ti-sun fs-4" aria-hidden="true" />
        : <i className="ti ti-moon fs-4" aria-hidden="true" />
      }
    </button>
  )
}

export default ThemeToggle
