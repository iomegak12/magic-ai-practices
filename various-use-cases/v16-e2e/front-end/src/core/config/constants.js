/**
 * Application-wide constants.
 * Values that never change regardless of environment.
 */

// ── Storage Keys ──────────────────────────────────────────────
export const STORAGE_KEYS = {
  CURRENT_TENANT: 'current_tenant_id',
  TENANT_LIST: 'tenant_list',
  THEME: 'app_theme',
  /** Per-tenant keys — call as template literals: `${STORAGE_KEYS.TENANT_PREFIX}${tenantId}_sessions` */
  TENANT_PREFIX: 'tenant_',
}

// ── Theme ──────────────────────────────────────────────────────
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
}

// ── Default Tenant ─────────────────────────────────────────────
export const DEFAULT_TENANT = {
  id: 'default',
  displayName: 'Personal Workspace',
  description: 'Default workspace',
}

// ── API ────────────────────────────────────────────────────────
export const API_VERSION = 'v1'

/** HTTP status codes used in error handling */
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  NOT_FOUND: 404,
  GONE: 410,
  TOO_MANY_REQUESTS: 429,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
}

// ── UI ─────────────────────────────────────────────────────────
/** Navigation links rendered in TopNavbar */
export const NAV_LINKS = [
  { label: 'Home', path: '/', icon: 'ti-home' },
  { label: 'Support', path: '/support', icon: 'ti-headset' },
  { label: 'About', path: '/about', icon: 'ti-info-circle' },
  { label: 'Contact', path: '/contact', icon: 'ti-mail' },
  { label: 'Settings', path: '/settings', icon: 'ti-settings' },
]

/** Color palette from design system */
export const COLORS = {
  primary: '#6366f1',
  primaryLight: '#818cf8',
  primaryDark: '#4f46e5',
  success: '#2fb344',
  warning: '#f76707',
  danger: '#d63939',
  info: '#4299e1',
  secondary: '#6c757d',
}

// ── Polling / Timers ───────────────────────────────────────────
/** Health check polling interval in ms */
export const HEALTH_POLL_INTERVAL = 30_000

/** Session list refresh interval in ms */
export const SESSION_REFRESH_INTERVAL = 60_000
