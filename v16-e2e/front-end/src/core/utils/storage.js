/**
 * LocalStorage wrapper with JSON serialisation, error handling, and
 * per-tenant key namespacing.
 * Ref: TENANT_MULTI_TENANCY.md — Storage Patterns
 */

import { STORAGE_KEYS } from '../config/constants.js'
import logger from './logger.js'

const storage = {
  /** Read and JSON-parse a value. Returns `fallback` if missing or parse fails. */
  get(key, fallback = null) {
    try {
      const raw = localStorage.getItem(key)
      if (raw === null) return fallback
      return JSON.parse(raw)
    } catch (err) {
      logger.warn(`storage.get failed for key "${key}":`, err)
      return fallback
    }
  },

  /** JSON-stringify and write a value. */
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value))
      return true
    } catch (err) {
      logger.warn(`storage.set failed for key "${key}":`, err)
      return false
    }
  },

  /** Remove a single key. */
  remove(key) {
    try {
      localStorage.removeItem(key)
      return true
    } catch (err) {
      logger.warn(`storage.remove failed for key "${key}":`, err)
      return false
    }
  },

  /** Remove all localStorage keys that start with `prefix`. */
  removeByPrefix(prefix) {
    try {
      const keys = []
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i)
        if (k?.startsWith(prefix)) keys.push(k)
      }
      keys.forEach((k) => localStorage.removeItem(k))
      logger.debug(`storage.removeByPrefix: cleared ${keys.length} key(s) with prefix "${prefix}"`)
      return keys.length
    } catch (err) {
      logger.warn(`storage.removeByPrefix failed for prefix "${prefix}":`, err)
      return 0
    }
  },

  // ── Tenant-scoped helpers ──────────────────────────────────────

  /** Build the scoped key: `tenant_${tenantId}_${suffix}` */
  tenantKey(tenantId, suffix) {
    return `${STORAGE_KEYS.TENANT_PREFIX}${tenantId}_${suffix}`
  },

  /** Read a tenant-scoped value. */
  getTenant(tenantId, suffix, fallback = null) {
    return this.get(this.tenantKey(tenantId, suffix), fallback)
  },

  /** Write a tenant-scoped value. */
  setTenant(tenantId, suffix, value) {
    return this.set(this.tenantKey(tenantId, suffix), value)
  },

  /**
   * Clear all data for a specific tenant.
   * Removes every key matching `tenant_${tenantId}_*`.
   * Ref: TENANT_MULTI_TENANCY.md — Clear Tenant Data
   */
  clearTenant(tenantId) {
    const prefix = `${STORAGE_KEYS.TENANT_PREFIX}${tenantId}_`
    return this.removeByPrefix(prefix)
  },
}

export default storage
