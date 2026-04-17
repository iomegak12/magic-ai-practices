/**
 * Retry logic with exponential back-off and jitter.
 *
 * Ref: INTEGRATION_GUIDE.md — Retry Strategies
 */

import { ErrorType } from './errors.js'
import logger from '../utils/logger.js'
import env from '../config/env.js'

// ── Configuration ──────────────────────────────────────────────────────────────
export const retryConfig = {
  maxAttempts:       env.retryAttempts,   // from VITE_API_RETRY_ATTEMPTS (default 3)
  initialDelay:      env.retryDelay,      // from VITE_API_RETRY_DELAY   (default 1000ms)
  maxDelay:          30_000,              // 30 s ceiling
  backoffMultiplier: 2,                   // doubles each attempt

  /** Only these HTTP methods are retried (POST excluded — not idempotent) */
  retryableMethods: ['GET', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'],

  /** HTTP status codes that warrant a retry */
  retryableStatuses: [408, 429, 500, 502, 503, 504],
}

// ── Helpers ────────────────────────────────────────────────────────────────────

/** Pause execution for `ms` milliseconds. */
export const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

/**
 * Calculate next delay using exponential back-off + ±10 % jitter.
 * @param {number} attempt  0-based attempt index
 * @returns {number} delay in milliseconds
 */
export function calculateBackoffDelay(attempt) {
  const base  = retryConfig.initialDelay * Math.pow(retryConfig.backoffMultiplier, attempt)
  const jitter = Math.random() * 0.1 * base
  return Math.min(base + jitter, retryConfig.maxDelay)
}

/**
 * Decide whether to retry a failed request.
 * @param {object} config        Axios request config (has `retryCount` injected by interceptor)
 * @param {object} apiError      Normalised APIError from `transformError()`
 * @returns {boolean}
 */
export function shouldRetry(config, apiError) {
  // Max attempts reached
  if ((config.retryCount ?? 0) >= retryConfig.maxAttempts) return false

  // Error itself says it's not retryable
  if (!apiError.retryable) return false

  // Method must be idempotent
  const method = config.method?.toUpperCase() ?? ''
  if (!retryConfig.retryableMethods.includes(method)) return false

  // 4xx errors (except 429) are permanent — don't retry
  const code = apiError.statusCode
  if (code && code >= 400 && code < 500 && code !== 429) return false

  return true
}

/**
 * Build the Axios response-error interceptor that implements retry logic.
 * Must be called with a reference to the axios instance so it can re-issue
 * the request after the delay.
 *
 * @param {import('axios').AxiosInstance} axiosInstance
 * @param {(error: unknown) => object} transformError  Error transform fn
 * @returns {(error: unknown) => Promise<never>}
 */
export function buildRetryInterceptor(axiosInstance, transformError) {
  return async (error) => {
    const config      = error.config
    const apiError    = transformError(error)

    // Initialise retry counter on first failure
    config.retryCount = config.retryCount ?? 0

    if (!shouldRetry(config, apiError)) {
      return Promise.reject(apiError)
    }

    config.retryCount += 1

    // Use server-provided Retry-After for rate limits; otherwise back-off
    const delay =
      apiError.type === ErrorType.RATE_LIMIT_EXCEEDED && apiError.retryAfter
        ? apiError.retryAfter * 1_000
        : calculateBackoffDelay(config.retryCount - 1)

    logger.warn(
      `[Retry ${config.retryCount}/${retryConfig.maxAttempts}]`,
      `${config.method?.toUpperCase()} ${config.url}`,
      `— waiting ${Math.round(delay)}ms`,
    )

    await sleep(delay)
    return axiosInstance.request(config)
  }
}
