import { useTenant } from '../hooks/useTenant.js'

/**
 * TenantIndicator — small badge in the TopNavbar showing the active tenant.
 *
 * Phase 2: read-only badge.
 * Phase 6: will be replaced by the full TenantSelector dropdown.
 *
 * Ref: TENANT_MULTI_TENANCY.md — Tenant Indicator
 */
function TenantIndicator() {
  const { currentTenant } = useTenant()

  return (
    <span
      className="badge bg-primary-lt text-primary d-flex align-items-center gap-1"
      title={`Active tenant: ${currentTenant.id}`}
      aria-label={`Active tenant: ${currentTenant.displayName}`}
    >
      <i className="ti ti-building" aria-hidden="true" />
      <span className="d-none d-md-inline">{currentTenant.displayName}</span>
    </span>
  )
}

export default TenantIndicator
