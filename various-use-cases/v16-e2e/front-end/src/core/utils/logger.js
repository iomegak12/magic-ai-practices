/**
 * Lightweight logger utility.
 * Respects VITE_LOG_LEVEL env var. In production, only warn/error are printed.
 * Ref: INTEGRATION_GUIDE.md — Development Logging
 */

import env from '../config/env.js'

const LEVELS = { debug: 0, info: 1, warn: 2, error: 3 }
const configured = LEVELS[env.logLevel] ?? LEVELS.info

const shouldLog = (level) => LEVELS[level] >= configured

const prefix = (level) => `[${level.toUpperCase()}]`

const logger = {
  debug: (...args) => {
    if (shouldLog('debug')) console.debug(prefix('debug'), ...args)
  },
  info: (...args) => {
    if (shouldLog('info')) console.info(prefix('info'), ...args)
  },
  warn: (...args) => {
    if (shouldLog('warn')) console.warn(prefix('warn'), ...args)
  },
  error: (...args) => {
    if (shouldLog('error')) console.error(prefix('error'), ...args)
  },

  /** Group logs — only in dev/debug */
  group: (label, fn) => {
    if (env.isDev && shouldLog('debug')) {
      console.group(label)
      fn()
      console.groupEnd()
    }
  },

  /** Log API request details */
  apiRequest: (method, url, params, data) => {
    if (!env.isDev || !shouldLog('debug')) return
    console.group(`[API →] ${method?.toUpperCase()} ${url}`)
    if (params && Object.keys(params).length) console.log('Params:', params)
    if (data) console.log('Body:', data)
    console.groupEnd()
  },

  /** Log API response details */
  apiResponse: (url, status, durationMs) => {
    if (!env.isDev || !shouldLog('debug')) return
    console.log(`[API ←] ${url}  ${status}  ${durationMs}ms`)
  },
}

export default logger
