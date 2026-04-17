// ─────────────────────────────────────────────────
// Constants used across the MSAv15 Portal
// ─────────────────────────────────────────────────

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9080'

export const MAX_SESSIONS = 10

export const HEALTH_POLL_INTERVAL = 30_000 // 30 seconds

export const STORAGE_KEYS = {
  SESSIONS: 'msav15_sessions',
  MESSAGES_PREFIX: 'msav15_messages_',
}

export const MESSAGE_TYPES = {
  USER: 'user',
  AGENT: 'agent',
  SYSTEM: 'system',
}

export const HEALTH_STATUS = {
  HEALTHY: 'healthy',
  DEGRADED: 'degraded',
  UNAVAILABLE: 'unavailable',
}
