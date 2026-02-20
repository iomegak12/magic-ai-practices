/**
 * API error types and transformation.
 * Converts raw Axios errors into structured APIError objects.
 *
 * Ref: INTEGRATION_GUIDE.md — Error Handling
 * Ref: API_SPECIFICATION.md — Error Handling / HTTP Status Codes
 */

// ── Error type enum ────────────────────────────────────────────────────────────
export const ErrorType = Object.freeze({
  // Network
  NETWORK_ERROR:        'NETWORK_ERROR',
  TIMEOUT_ERROR:        'TIMEOUT_ERROR',

  // 4xx
  VALIDATION_ERROR:     'VALIDATION_ERROR',   // 400
  NOT_FOUND:            'NOT_FOUND',           // 404
  SESSION_EXPIRED:      'SESSION_EXPIRED',     // 410
  RATE_LIMIT_EXCEEDED:  'RATE_LIMIT_EXCEEDED', // 429

  // 5xx
  SERVER_ERROR:         'SERVER_ERROR',        // 500–504
  SERVICE_UNAVAILABLE:  'SERVICE_UNAVAILABLE', // 503

  // Other
  UNKNOWN_ERROR:        'UNKNOWN_ERROR',
})

/**
 * Transform a raw Axios error into a normalised APIError object.
 *
 * @param {unknown} error  Raw error from Axios
 * @returns {{
 *   type: string,
 *   message: string,
 *   statusCode: number|undefined,
 *   retryable: boolean,
 *   retryAfter: number|undefined,
 *   requestId: string|undefined,
 *   context: unknown
 * }}
 */
export function transformError(error) {
  // ── No response (network down / DNS fail) ──────────────────────────────────
  if (error?.code === 'ERR_NETWORK' || !error?.response) {
    return {
      type: ErrorType.NETWORK_ERROR,
      message: 'Network connection failed. Please check your internet connection.',
      statusCode: undefined,
      retryable: true,
      retryAfter: undefined,
      requestId: undefined,
      context: null,
    }
  }

  // ── Timeout ────────────────────────────────────────────────────────────────
  if (error?.code === 'ECONNABORTED' || error?.code === 'ERR_CANCELED') {
    return {
      type: ErrorType.TIMEOUT_ERROR,
      message: 'Request timed out. Please try again.',
      statusCode: undefined,
      retryable: true,
      retryAfter: undefined,
      requestId: undefined,
      context: null,
    }
  }

  const { response } = error
  const requestId  = response?.headers?.['x-request-id']
  const detail     = response?.data?.detail ?? response?.data?.error
  const status     = response?.status

  // ── 429 Rate limit ─────────────────────────────────────────────────────────
  if (status === 429) {
    const retryAfter = parseInt(response.headers?.['retry-after'] ?? '60', 10)
    return {
      type: ErrorType.RATE_LIMIT_EXCEEDED,
      message: `Rate limit exceeded. Please retry after ${retryAfter} seconds.`,
      statusCode: 429,
      retryable: true,
      retryAfter,
      requestId,
      context: response.data,
    }
  }

  // ── 410 Session expired ────────────────────────────────────────────────────
  if (status === 410) {
    return {
      type: ErrorType.SESSION_EXPIRED,
      message: detail ?? 'Session has expired. Please start a new conversation.',
      statusCode: 410,
      retryable: false,
      retryAfter: undefined,
      requestId,
      context: response.data,
    }
  }

  // ── 404 Not found ──────────────────────────────────────────────────────────
  if (status === 404) {
    return {
      type: ErrorType.NOT_FOUND,
      message: detail ?? 'The requested resource was not found.',
      statusCode: 404,
      retryable: false,
      retryAfter: undefined,
      requestId,
      context: response.data,
    }
  }

  // ── 400 Validation ─────────────────────────────────────────────────────────
  if (status === 400) {
    return {
      type: ErrorType.VALIDATION_ERROR,
      message: detail ?? 'Invalid request. Please check your input.',
      statusCode: 400,
      retryable: false,
      retryAfter: undefined,
      requestId,
      context: response.data,
    }
  }

  // ── 503 Service unavailable ────────────────────────────────────────────────
  if (status === 503) {
    return {
      type: ErrorType.SERVICE_UNAVAILABLE,
      message: 'Service is temporarily unavailable. Please try again later.',
      statusCode: 503,
      retryable: true,
      retryAfter: undefined,
      requestId,
      context: response.data,
    }
  }

  // ── 5xx Server errors ──────────────────────────────────────────────────────
  if (status >= 500) {
    return {
      type: ErrorType.SERVER_ERROR,
      message: detail ?? 'A server error occurred. Please try again later.',
      statusCode: status,
      retryable: true,
      retryAfter: undefined,
      requestId,
      context: response.data,
    }
  }

  // ── Catch-all ──────────────────────────────────────────────────────────────
  return {
    type: ErrorType.UNKNOWN_ERROR,
    message: detail ?? error?.message ?? 'An unexpected error occurred.',
    statusCode: status,
    retryable: false,
    retryAfter: undefined,
    requestId,
    context: response?.data ?? null,
  }
}
