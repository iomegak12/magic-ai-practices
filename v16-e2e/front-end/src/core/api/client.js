/**
 * Axios-based API client — singleton instance used across the whole app.
 *
 * Wires together:
 *   - Base URL + timeout from env
 *   - All request / response interceptors
 *   - Error transform + retry logic
 *
 * Usage:
 *   import apiClient from '@/core/api/client.js'
 *   const { data } = await apiClient.get('/health')
 *
 * Ref: INTEGRATION_GUIDE.md — API Client Setup
 */

import axios from 'axios'
import env from '../config/env.js'
import { transformError } from './errors.js'
import { buildRetryInterceptor } from './retry.js'
import { attachInterceptors } from './interceptors.js'
import logger from '../utils/logger.js'

// ── Create instance ────────────────────────────────────────────────────────────
const instance = axios.create({
  baseURL:         env.apiBaseURL,
  timeout:         env.apiTimeout,
  headers: {
    'Content-Type': 'application/json',
    'Accept':       'application/json',
  },
})

// ── Build error + retry interceptor ───────────────────────────────────────────
// Combines: error transform → retry logic → final rejection
const errorResponseInterceptor = buildRetryInterceptor(instance, (error) => {
  const apiError = transformError(error)
  logger.error('[API Error]', apiError.type, apiError.message, {
    status:    apiError.statusCode,
    requestId: apiError.requestId,
  })
  return apiError
})

// ── Attach all interceptors ────────────────────────────────────────────────────
attachInterceptors(instance, errorResponseInterceptor)

logger.info(`API client initialised — baseURL: ${env.apiBaseURL}`)

export default instance
