/**
 * Environment variable loader.
 * All VITE_* variables are injected at build time by Vite.
 * Access via import.meta.env
 */

const env = {
  /** FastAPI backend base URL */
  apiBaseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:9080',

  /** Axios request timeout in milliseconds */
  apiTimeout: Number(import.meta.env.VITE_API_TIMEOUT) || 30_000,

  /** Feature flags */
  // Opt-in: streaming requires VITE_ENABLE_STREAMING=true — backend endpoint is not yet live
  enableStreaming: import.meta.env.VITE_ENABLE_STREAMING === 'true',
  enableAnalytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
  enableDebug: import.meta.env.VITE_ENABLE_DEBUG === 'true',

  /** Logging level: debug | info | warn | error */
  logLevel: import.meta.env.VITE_LOG_LEVEL || 'info',

  /** Default tenant ID */
  defaultTenant: import.meta.env.VITE_DEFAULT_TENANT || 'default',

  /** Retry configuration */
  retryAttempts: Number(import.meta.env.VITE_API_RETRY_ATTEMPTS) || 3,
  retryDelay: Number(import.meta.env.VITE_API_RETRY_DELAY) || 1_000,
  maxRetries: Number(import.meta.env.VITE_API_MAX_RETRIES) || 5,

  /** App metadata */
  appName: import.meta.env.VITE_APP_NAME || 'Customer Service Agent',
  appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',

  /** Is development mode */
  isDev: import.meta.env.DEV === true,
  isProd: import.meta.env.PROD === true,
}

export default env
