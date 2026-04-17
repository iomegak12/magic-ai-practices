import { createContext, useContext } from 'react'
import { DEFAULT_TENANT } from '../../../core/config/constants.js'

/**
 * TenantContext — holds the current tenant and tenant management functions.
 *
 * Consumed exclusively via `useTenant()` hook.
 * Ref: TENANT_MULTI_TENANCY.md — Tenant Context Management
 * Ref: FRONTEND_ARCHITECTURE.md — State Management
 */

export const TenantContext = createContext({
  /** Active tenant object */
  currentTenant: DEFAULT_TENANT,
  /** Full list of saved tenants */
  tenants:        [DEFAULT_TENANT],
  /** Switch to a tenant by ID */
  switchTenant:  (_tenantId) => {},
  /** Add a new tenant to the list */
  addTenant:     (_tenant) => {},
  /** Remove a tenant from the list (cannot remove the currently active one) */
  removeTenant:  (_tenantId) => {},
  isLoading:     false,
  error:         null,
})

/** Hook — must be used inside TenantProvider */
export function useTenant() {
  const ctx = useContext(TenantContext)
  if (!ctx) throw new Error('useTenant must be used within a TenantProvider')
  return ctx
}
