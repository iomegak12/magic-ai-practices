/**
 * Centralised API endpoint definitions.
 * All backend routes live here — no magic strings in components.
 *
 * NOTE — API Drift (confirmed by api-drift-test.js, 2026-02-20):
 *   The backend does NOT mount agent/info routes under /api/v1/.
 *   Correct prefixes per backend OpenAPI:
 *     Agent ops  → /agent/*
 *     Info       → /info/*
 *     Sessions   → /api/v1/sessions/*   (unchanged)
 *     Health     → /health/*             (unchanged)
 */

import { API_VERSION } from './constants.js'

// Session management still uses /api/v1
const SESSION_BASE = `/api/${API_VERSION}/sessions`

export const ENDPOINTS = {
  // ── Root / Info ────────────────────────────────────────────
  ROOT: '/',
  API_INFO: '/info',
  API_TOOLS: '/info/tools',

  // ── Health ─────────────────────────────────────────────────
  HEALTH: '/health',
  HEALTH_DETAILED: '/health/detailed',
  HEALTH_LIVE: '/health/live',
  HEALTH_READY: '/health/ready',

  // ── Agent Operations (no /api/v1 prefix on backend) ────────
  AGENT_CREATE_SESSION: '/agent/sessions',
  AGENT_LIST_SESSIONS: '/agent/sessions',
  AGENT_SEND_MESSAGE: '/agent/messages',
  AGENT_SEND_MESSAGE_STREAM: '/agent/messages/stream',
  /** @param {string} id */
  AGENT_DELETE_SESSION: (id) => `/agent/sessions/${id}`,

  // ── Session Management (/api/v1/sessions) ──────────────────
  SESSIONS_LIST: `${SESSION_BASE}/`,
  SESSIONS_STATS: `${SESSION_BASE}/stats`,
  /** @param {string} id */
  SESSION_HISTORY: (id) => `${SESSION_BASE}/${id}/history`,
  /** @param {string} id */
  SESSION_DELETE: (id) => `${SESSION_BASE}/${id}`,
  /** @param {string} id */
  SESSION_CLEANUP: (id) => `${SESSION_BASE}/${id}/cleanup`,
}

export default ENDPOINTS
