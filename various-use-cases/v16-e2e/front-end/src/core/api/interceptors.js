/**
 * Axios interceptor factories.
 *
 * Request interceptors (applied in order):
 *   1. Inject X-Request-ID + start timestamp
 *   2. Inject tenant_id query param on /sessions endpoints + X-Tenant-ID header
 *   3. Dev-mode request logging
 *
 * Response interceptors (applied in order):
 *   1. Log response time (dev only)
 *   2. Capture X-Request-ID from response headers
 *   3. Error transform + retry (built in client.js via retry.js)
 *
 * Ref: INTEGRATION_GUIDE.md — Request/Response Patterns
 * Ref: TENANT_MULTI_TENANCY.md — Automatic Tenant Injection
 */

import logger from '../utils/logger.js'

// A mutable ref so interceptors can read the current tenant without a circular
// import.  Set by TenantProvider after mount via `setTenantRef()`.
let _tenantId = 'default'

/** Called by TenantProvider to keep the tenant ref in sync. */
export function setTenantRef(id) {
  _tenantId = id ?? 'default'
}

/** Currently active tenant ID (read by request interceptor). */
export function getTenantRef() {
  return _tenantId
}

// ── Request interceptors ───────────────────────────────────────────────────────

/**
 * Injects X-Request-ID header and records startTime for latency logging.
 */
export function requestIdInterceptor(config) {
  const requestId = crypto.randomUUID()
  config.headers['X-Request-ID'] = requestId
  config.metadata = { ...(config.metadata ?? {}), requestId, startTime: Date.now() }
  return config
}

/**
 * Injects tenant_id as a query param on /sessions endpoints
 * and X-Tenant-ID header on every request.
 * Agent endpoints (/agent/) are NOT tenant-scoped per the spec.
 *
 * Ref: API_SPECIFICATION.md — Headers
 * Ref: TENANT_MULTI_TENANCY.md — Tenant-Scoped Endpoints
 */
export function tenantInterceptor(config) {
  const tenantId = getTenantRef()
  if (!tenantId) return config

  // Always add as header for server-side logging/tracing
  config.headers['X-Tenant-ID'] = tenantId

  // Add query param only for session-management endpoints
  const url = config.url ?? ''
  if (url.includes('/sessions')) {
    config.params = { ...(config.params ?? {}), tenant_id: tenantId }
  }

  return config
}

/**
 * Dev-only: logs request method, URL, params, and body.
 */
export function devLoggingRequestInterceptor(config) {
  logger.apiRequest(config.method, config.url, config.params, config.data)
  return config
}

// ── Response interceptors ──────────────────────────────────────────────────────

/**
 * Logs response time and captures X-Request-ID from response headers.
 */
export function responseMetaInterceptor(response) {
  const { startTime, requestId } = response.config?.metadata ?? {}
  if (startTime) {
    const duration = Date.now() - startTime
    logger.apiResponse(response.config.url, response.status, duration)
    response.config.metadata = {
      ...(response.config.metadata ?? {}),
      duration,
      serverRequestId: response.headers?.['x-request-id'] ?? requestId,
      responseTime:    response.headers?.['x-response-time'],
    }
  }
  return response
}

/**
 * Attaches all interceptors to an Axios instance.
 *
 * @param {import('axios').AxiosInstance} instance
 * @param {function} errorResponseInterceptor  The combined error-transform+retry handler
 */
export function attachInterceptors(instance, errorResponseInterceptor) {
  // ── Request ──────────────────────────────────────────────────
  instance.interceptors.request.use(requestIdInterceptor,  (e) => Promise.reject(e))
  instance.interceptors.request.use(tenantInterceptor,     (e) => Promise.reject(e))
  instance.interceptors.request.use(devLoggingRequestInterceptor, (e) => Promise.reject(e))

  // ── Response ─────────────────────────────────────────────────
  instance.interceptors.response.use(responseMetaInterceptor, errorResponseInterceptor)
}
