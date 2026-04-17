import { useState, useCallback, useEffect } from 'react'
import { TenantContext } from './TenantContext.jsx'
import { DEFAULT_TENANT, STORAGE_KEYS } from '../../../core/config/constants.js'
import storage from '../../../core/utils/storage.js'
import { setTenantRef } from '../../../core/api/interceptors.js'
import logger from '../../../core/utils/logger.js'

/**
 * TenantProvider — manages multi-tenancy state.
 *
 * Responsibilities:
 *   - Load tenant list + current tenant from localStorage on mount
 *   - Persist changes to localStorage
 *   - Keep the Axios interceptor's tenant ref in sync via `setTenantRef()`
 *   - Provide `switchTenant()`, `addTenant()`, `removeTenant()`
 *
 * Ref: TENANT_MULTI_TENANCY.md — Tenant Context Management & Storage Patterns
 * Ref: INTEGRATION_GUIDE.md — Add Tenant Context interceptor
 */
function TenantProvider({ children }) {
  const [tenants, setTenants] = useState(() => {
    const saved = storage.get(STORAGE_KEYS.TENANT_LIST)
    if (Array.isArray(saved) && saved.length > 0) return saved
    return [DEFAULT_TENANT]
  })

  const [currentTenant, setCurrentTenant] = useState(() => {
    const savedId = storage.get(STORAGE_KEYS.CURRENT_TENANT)
    if (!savedId) return DEFAULT_TENANT

    const savedList = storage.get(STORAGE_KEYS.TENANT_LIST)
    if (Array.isArray(savedList)) {
      const found = savedList.find((t) => t.id === savedId)
      if (found) return found
    }
    return DEFAULT_TENANT
  })

  const [isLoading, setIsLoading] = useState(false)
  const [error,     setError]     = useState(null)

  // Keep Axios interceptor in sync whenever the current tenant changes
  useEffect(() => {
    setTenantRef(currentTenant.id)
    logger.debug(`TenantProvider: active tenant → "${currentTenant.id}"`)
  }, [currentTenant])

  // Persist tenant list whenever it changes
  useEffect(() => {
    storage.set(STORAGE_KEYS.TENANT_LIST, tenants)
  }, [tenants])

  /**
   * Switch to a different tenant by ID.
   * Clears that tenant's cached data so fresh data is fetched.
   * Ref: TENANT_MULTI_TENANCY.md — Tenant Switching
   */
  const switchTenant = useCallback((tenantId) => {
    const found = tenants.find((t) => t.id === tenantId)
    if (!found) {
      logger.warn(`switchTenant: tenant "${tenantId}" not found in list`)
      return
    }
    setCurrentTenant(found)
    storage.set(STORAGE_KEYS.CURRENT_TENANT, tenantId)
    logger.info(`Switched to tenant "${tenantId}"`)
  }, [tenants])

  /**
   * Add a new tenant.
   * Tenant ID must be unique (slug: lowercase + hyphens).
   * Ref: TENANT_MULTI_TENANCY.md — Add Tenant UI
   */
  const addTenant = useCallback((tenant) => {
    if (!tenant?.id) {
      logger.warn('addTenant: tenant.id is required')
      return false
    }
    if (tenants.find((t) => t.id === tenant.id)) {
      logger.warn(`addTenant: tenant "${tenant.id}" already exists`)
      return false
    }
    const newTenant = {
      id:          tenant.id.toLowerCase().replace(/\s+/g, '-'),
      displayName: tenant.displayName ?? tenant.id,
      description: tenant.description ?? '',
    }
    setTenants((prev) => [...prev, newTenant])
    logger.info(`Tenant "${newTenant.id}" added`)
    return true
  }, [tenants])

  /**
   * Remove a tenant from the list.
   * Cannot remove the currently active tenant.
   */
  const removeTenant = useCallback((tenantId) => {
    if (tenantId === currentTenant.id) {
      logger.warn('removeTenant: cannot remove the currently active tenant')
      return false
    }
    if (tenantId === DEFAULT_TENANT.id) {
      logger.warn('removeTenant: cannot remove the default tenant')
      return false
    }
    setTenants((prev) => prev.filter((t) => t.id !== tenantId))
    storage.clearTenant(tenantId)
    logger.info(`Tenant "${tenantId}" removed`)
    return true
  }, [currentTenant.id])

  return (
    <TenantContext.Provider
      value={{
        currentTenant,
        tenants,
        switchTenant,
        addTenant,
        removeTenant,
        isLoading,
        error,
      }}
    >
      {children}
    </TenantContext.Provider>
  )
}

export default TenantProvider
