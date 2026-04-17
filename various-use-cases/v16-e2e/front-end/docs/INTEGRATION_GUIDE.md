# API Integration Guide

**Version:** 1.0.0  
**Last Updated:** February 20, 2026

## Table of Contents

- [Overview](#overview)
- [API Client Setup](#api-client-setup)
- [Request/Response Patterns](#requestresponse-patterns)
- [Error Handling](#error-handling)
- [Retry Strategies](#retry-strategies)
- [Rate Limit Handling](#rate-limit-handling)
- [Circuit Breaker Pattern](#circuit-breaker-pattern)
- [Timeout Configuration](#timeout-configuration)
- [Connection Resilience](#connection-resilience)
- [Streaming Integration](#streaming-integration)
- [Multi-Tenancy Integration](#multi-tenancy-integration)
- [Testing API Integration](#testing-api-integration)

---

## Overview

This guide provides practical patterns for integrating with the Customer Service Agent API. It covers error handling, retry logic, rate limiting, and connection resilience strategies.

### Integration Principles

1. **Resilience First**: Handle failures gracefully
2. **User Feedback**: Always inform users of operation status
3. **Automatic Recovery**: Retry transient failures automatically
4. **Fail Fast**: Don't retry permanent errors
5. **Observability**: Log all API interactions

---

## API Client Setup

### Base Configuration

```typescript
interface APIConfig {
  baseURL: string;
  timeout: number;
  retryAttempts: number;
  retryDelay: number;
  headers: Record<string, string>;
}

const defaultConfig: APIConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:9080',
  timeout: 30000, // 30 seconds default
  retryAttempts: 3,
  retryDelay: 1000, // 1 second
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
};
```

### Axios Instance Creation

```typescript
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

class APIClient {
  private instance: AxiosInstance;
  private config: APIConfig;
  
  constructor(config: Partial<APIConfig> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.instance = this.createInstance();
    this.setupInterceptors();
  }
  
  private createInstance(): AxiosInstance {
    return axios.create({
      baseURL: this.config.baseURL,
      timeout: this.config.timeout,
      headers: this.config.headers
    });
  }
  
  private setupInterceptors(): void {
    this.setupRequestInterceptors();
    this.setupResponseInterceptors();
  }
  
  // Instance getter for direct access
  public getAxios(): AxiosInstance {
    return this.instance;
  }
}
```

---

## Request/Response Patterns

### Request Interceptors

#### 1. Add Request ID

```typescript
private setupRequestInterceptors(): void {
  this.instance.interceptors.request.use(
    (config) => {
      // Generate unique request ID for tracing
      const requestId = crypto.randomUUID();
      config.headers['X-Request-ID'] = requestId;
      
      // Store for later correlation
      config.metadata = { ...config.metadata, requestId };
      
      return config;
    },
    (error) => Promise.reject(error)
  );
}
```

#### 2. Add Tenant Context

```typescript
this.instance.interceptors.request.use(
  (config) => {
    const tenantId = getTenantFromContext(); // From state/localStorage
    
    if (tenantId) {
      // For session endpoints, add as query parameter
      if (config.url?.includes('/sessions')) {
        config.params = {
          ...config.params,
          tenant_id: tenantId
        };
      }
      
      // Also add as header for logging
      config.headers['X-Tenant-ID'] = tenantId;
    }
    
    return config;
  }
);
```

#### 3. Add Timestamp for Performance Tracking

```typescript
this.instance.interceptors.request.use(
  (config) => {
    config.metadata = {
      ...config.metadata,
      startTime: Date.now()
    };
    return config;
  }
);
```

#### 4. Development Logging

```typescript
this.instance.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.group(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
      console.log('Headers:', config.headers);
      console.log('Params:', config.params);
      console.log('Body:', config.data);
      console.groupEnd();
    }
    return config;
  }
);
```

### Response Interceptors

#### 1. Log Response Time

```typescript
this.instance.interceptors.response.use(
  (response) => {
    const { startTime, requestId } = response.config.metadata || {};
    
    if (startTime) {
      const duration = Date.now() - startTime;
      
      if (import.meta.env.DEV) {
        console.log(`[API Response] ${response.config.url} - ${duration}ms`);
      }
      
      // Send to analytics
      logPerformanceMetric({
        endpoint: response.config.url,
        method: response.config.method,
        duration,
        requestId,
        status: response.status
      });
    }
    
    return response;
  }
);
```

#### 2. Extract Response Data

```typescript
this.instance.interceptors.response.use(
  (response) => {
    // For most endpoints, we just want the data
    // But preserve full response if needed
    response.config.metadata = {
      ...response.config.metadata,
      requestId: response.headers['x-request-id'],
      responseTime: response.headers['x-response-time']
    };
    
    return response;
  }
);
```

---

## Error Handling

### Error Classification

```typescript
enum ErrorType {
  // Network errors
  NETWORK_ERROR = 'NETWORK_ERROR',
  TIMEOUT_ERROR = 'TIMEOUT_ERROR',
  
  // Client errors (4xx)
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  NOT_FOUND = 'NOT_FOUND',
  SESSION_EXPIRED = 'SESSION_EXPIRED',
  
  // Server errors (5xx)
  SERVER_ERROR = 'SERVER_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  
  // Rate limiting
  RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED',
  
  // Unknown
  UNKNOWN_ERROR = 'UNKNOWN_ERROR'
}

interface APIError {
  type: ErrorType;
  message: string;
  statusCode?: number;
  retryable: boolean;
  retryAfter?: number;
  requestId?: string;
  context?: any;
}
```

### Error Transformation

```typescript
private transformError(error: any): APIError {
  // Network error (no response)
  if (error.code === 'ERR_NETWORK' || !error.response) {
    return {
      type: ErrorType.NETWORK_ERROR,
      message: 'Network connection failed. Please check your internet connection.',
      retryable: true
    };
  }
  
  // Timeout error
  if (error.code === 'ECONNABORTED') {
    return {
      type: ErrorType.TIMEOUT_ERROR,
      message: 'Request timed out. Please try again.',
      retryable: true
    };
  }
  
  const { response } = error;
  const requestId = response?.headers?.['x-request-id'];
  
  // Rate limit (429)
  if (response.status === 429) {
    const retryAfter = parseInt(response.headers['retry-after'] || '60');
    return {
      type: ErrorType.RATE_LIMIT_EXCEEDED,
      message: `Rate limit exceeded. Retry after ${retryAfter} seconds.`,
      statusCode: 429,
      retryable: true,
      retryAfter,
      requestId
    };
  }
  
  // Session expired (410)
  if (response.status === 410) {
    return {
      type: ErrorType.SESSION_EXPIRED,
      message: response.data?.detail || 'Session has expired',
      statusCode: 410,
      retryable: false,
      requestId
    };
  }
  
  // Not found (404)
  if (response.status === 404) {
    return {
      type: ErrorType.NOT_FOUND,
      message: response.data?.detail || 'Resource not found',
      statusCode: 404,
      retryable: false,
      requestId
    };
  }
  
  // Validation error (400)
  if (response.status === 400) {
    return {
      type: ErrorType.VALIDATION_ERROR,
      message: response.data?.detail || 'Invalid request',
      statusCode: 400,
      retryable: false,
      requestId,
      context: response.data
    };
  }
  
  // Server error (500)
  if (response.status >= 500) {
    return {
      type: ErrorType.SERVER_ERROR,
      message: 'Server error. Please try again later.',
      statusCode: response.status,
      retryable: true,
      requestId
    };
  }
  
  // Unknown error
  return {
    type: ErrorType.UNKNOWN_ERROR,
    message: error.message || 'An unexpected error occurred',
    retryable: false,
    requestId
  };
}
```

### Error Response Interceptor

```typescript
this.instance.interceptors.response.use(
  (response) => response,
  (error) => {
    const transformedError = this.transformError(error);
    
    // Log error
    logAPIError(transformedError);
    
    // Throw transformed error
    return Promise.reject(transformedError);
  }
);
```

---

## Retry Strategies

### Retry Decision Logic

```typescript
interface RetryConfig {
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
  retryableStatuses: number[];
  retryableMethods: string[];
}

const defaultRetryConfig: RetryConfig = {
  maxAttempts: 3,
  initialDelay: 1000,      // 1 second
  maxDelay: 30000,         // 30 seconds
  backoffMultiplier: 2,    // Exponential backoff
  retryableStatuses: [408, 429, 500, 502, 503, 504],
  retryableMethods: ['GET', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
};

function shouldRetry(config: any, error: APIError): boolean {
  // Don't retry if max attempts reached
  if (config.retryCount >= defaultRetryConfig.maxAttempts) {
    return false;
  }
  
  // Don't retry if error is not retryable
  if (!error.retryable) {
    return false;
  }
  
  // Don't retry POST requests (not idempotent)
  if (!defaultRetryConfig.retryableMethods.includes(config.method?.toUpperCase())) {
    return false;
  }
  
  // Don't retry client errors (except 429)
  if (error.statusCode && error.statusCode >= 400 && error.statusCode < 500 && error.statusCode !== 429) {
    return false;
  }
  
  return true;
}
```

### Exponential Backoff

```typescript
function calculateBackoffDelay(attempt: number): number {
  const delay = defaultRetryConfig.initialDelay * Math.pow(
    defaultRetryConfig.backoffMultiplier,
    attempt
  );
  
  // Add jitter to prevent thundering herd
  const jitter = Math.random() * 0.1 * delay;
  
  return Math.min(delay + jitter, defaultRetryConfig.maxDelay);
}

async function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### Retry Interceptor

```typescript
this.instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;
    const transformedError = this.transformError(error);
    
    // Initialize retry count
    config.retryCount = config.retryCount || 0;
    
    // Check if should retry
    if (!shouldRetry(config, transformedError)) {
      return Promise.reject(transformedError);
    }
    
    // Increment retry count
    config.retryCount += 1;
    
    // Calculate delay
    let delay: number;
    if (transformedError.type === ErrorType.RATE_LIMIT_EXCEEDED && transformedError.retryAfter) {
      // Use server-provided retry-after for rate limits
      delay = transformedError.retryAfter * 1000;
    } else {
      // Use exponential backoff for other errors
      delay = calculateBackoffDelay(config.retryCount - 1);
    }
    
    // Log retry attempt
    console.log(
      `[Retry ${config.retryCount}/${defaultRetryConfig.maxAttempts}] ` +
      `${config.method?.toUpperCase()} ${config.url} after ${delay}ms`
    );
    
    // Wait before retrying
    await sleep(delay);
    
    // Retry request
    return this.instance.request(config);
  }
);
```

---

## Rate Limit Handling

### Proactive Rate Limit Checking

```typescript
class RateLimitTracker {
  private limits = new Map<string, RateLimitInfo>();
  
  interface RateLimitInfo {
    limit: number;
    remaining: number;
    reset: number; // Unix timestamp
  }
  
  // Update from response headers
  updateFromHeaders(endpoint: string, headers: any): void {
    const info: RateLimitInfo = {
      limit: parseInt(headers['x-ratelimit-limit'] || '0'),
      remaining: parseInt(headers['x-ratelimit-remaining'] || '0'),
      reset: parseInt(headers['x-ratelimit-reset'] || '0')
    };
    
    this.limits.set(endpoint, info);
  }
  
  // Check before making request
  async checkRateLimit(endpoint: string): Promise<void> {
    const info = this.limits.get(endpoint);
    
    if (!info) {
      return; // No rate limit info yet
    }
    
    if (info.remaining <= 0) {
      const now = Date.now() / 1000;
      const waitTime = Math.max(0, info.reset - now);
      
      if (waitTime > 0) {
        console.warn(`Rate limit reached for ${endpoint}. Waiting ${waitTime}s...`);
        await sleep(waitTime * 1000);
      }
    }
  }
  
  // Get current status
  getStatus(endpoint: string): RateLimitInfo | null {
    return this.limits.get(endpoint) || null;
  }
}

// Global instance
const rateLimitTracker = new RateLimitTracker();
```

### Integration with API Client

```typescript
// Request interceptor - check rate limit before request
this.instance.interceptors.request.use(
  async (config) => {
    const endpoint = config.url || '';
    await rateLimitTracker.checkRateLimit(endpoint);
    return config;
  }
);

// Response interceptor - update rate limit info
this.instance.interceptors.response.use(
  (response) => {
    const endpoint = response.config.url || '';
    rateLimitTracker.updateFromHeaders(endpoint, response.headers);
    return response;
  }
);
```

### User Feedback for Rate Limits

```typescript
// React hook for rate limit status
function useRateLimitStatus(endpoint: string) {
  const [status, setStatus] = useState<RateLimitInfo | null>(null);
  
  useEffect(() => {
    const interval = setInterval(() => {
      const info = rateLimitTracker.getStatus(endpoint);
      setStatus(info);
    }, 1000);
    
    return () => clearInterval(interval);
  }, [endpoint]);
  
  return status;
}

// Component usage
function RateLimitIndicator({ endpoint }: { endpoint: string }) {
  const status = useRateLimitStatus(endpoint);
  
  if (!status || status.remaining > 10) {
    return null; // Don't show if plenty of capacity
  }
  
  const percentage = (status.remaining / status.limit) * 100;
  const resetDate = new Date(status.reset * 1000);
  
  return (
    <div className="rate-limit-warning">
      <span>API calls remaining: {status.remaining}/{status.limit}</span>
      <span>Resets at: {resetDate.toLocaleTimeString()}</span>
      <progress value={percentage} max={100} />
    </div>
  );
}
```

---

## Circuit Breaker Pattern

### Circuit Breaker Implementation

```typescript
enum CircuitState {
  CLOSED = 'CLOSED',       // Normal operation
  OPEN = 'OPEN',           // Failing, reject requests
  HALF_OPEN = 'HALF_OPEN'  // Testing if recovered
}

interface CircuitBreakerConfig {
  failureThreshold: number;    // Failures before opening
  successThreshold: number;    // Successes before closing from half-open
  timeout: number;             // Time before trying again (half-open)
  monitoringPeriod: number;    // Time window for failure counting
}

class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failureCount: number = 0;
  private successCount: number = 0;
  private lastFailureTime: number = 0;
  private config: CircuitBreakerConfig;
  
  constructor(config: Partial<CircuitBreakerConfig> = {}) {
    this.config = {
      failureThreshold: 5,
      successThreshold: 2,
      timeout: 60000,          // 1 minute
      monitoringPeriod: 120000, // 2 minutes
      ...config
    };
  }
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    // Check circuit state
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailureTime > this.config.timeout) {
        // Try half-open
        this.state = CircuitState.HALF_OPEN;
        this.successCount = 0;
        console.log('[Circuit Breaker] Entering HALF_OPEN state');
      } else {
        // Still open, reject immediately
        throw new Error('Circuit breaker is OPEN. Service unavailable.');
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess(): void {
    this.failureCount = 0;
    
    if (this.state === CircuitState.HALF_OPEN) {
      this.successCount++;
      
      if (this.successCount >= this.config.successThreshold) {
        this.state = CircuitState.CLOSED;
        console.log('[Circuit Breaker] Recovered, entering CLOSED state');
      }
    }
  }
  
  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.state === CircuitState.HALF_OPEN) {
      // Failed while testing, go back to open
      this.state = CircuitState.OPEN;
      console.log('[Circuit Breaker] Failed in HALF_OPEN, returning to OPEN');
      return;
    }
    
    if (this.failureCount >= this.config.failureThreshold) {
      this.state = CircuitState.OPEN;
      console.log('[Circuit Breaker] Failure threshold reached, entering OPEN state');
    }
  }
  
  getState(): CircuitState {
    return this.state;
  }
  
  reset(): void {
    this.state = CircuitState.CLOSED;
    this.failureCount = 0;
    this.successCount = 0;
    console.log('[Circuit Breaker] Manually reset to CLOSED');
  }
}
```

### Integration with API Client

```typescript
class APIClientWithCircuitBreaker extends APIClient {
  private circuitBreaker: CircuitBreaker;
  
  constructor(config?: Partial<APIConfig>) {
    super(config);
    this.circuitBreaker = new CircuitBreaker();
  }
  
  async request<T>(config: AxiosRequestConfig): Promise<T> {
    return this.circuitBreaker.execute(async () => {
      const response = await this.instance.request<T>(config);
      return response.data;
    });
  }
  
  getCircuitState(): CircuitState {
    return this.circuitBreaker.getState();
  }
  
  resetCircuit(): void {
    this.circuitBreaker.reset();
  }
}
```

---

## Timeout Configuration

### Per-Endpoint Timeouts

```typescript
enum Endpoint {
  HEALTH = '/health',
  CREATE_SESSION = '/api/v1/agent/sessions',
  SEND_MESSAGE = '/api/v1/agent/messages',
  SEND_MESSAGE_STREAM = '/api/v1/agent/messages/stream',
  LIST_SESSIONS = '/api/v1/agent/sessions',
  GET_SESSION_HISTORY = '/api/v1/sessions/:id/history',
  DELETE_SESSION = '/api/v1/sessions/:id'
}

const timeoutConfig: Record<string, number> = {
  [Endpoint.HEALTH]: 5000,               // 5 seconds
  [Endpoint.CREATE_SESSION]: 10000,      // 10 seconds
  [Endpoint.SEND_MESSAGE]: 60000,        // 60 seconds (message processing)
  [Endpoint.SEND_MESSAGE_STREAM]: 120000, // 2 minutes (streaming)
  [Endpoint.LIST_SESSIONS]: 15000,       // 15 seconds
  [Endpoint.GET_SESSION_HISTORY]: 20000, // 20 seconds
  [Endpoint.DELETE_SESSION]: 10000       // 10 seconds
};

function getTimeoutForEndpoint(url: string): number {
  // Match endpoint pattern
  for (const [endpoint, timeout] of Object.entries(timeoutConfig)) {
    if (url.includes(endpoint.replace(':id', ''))) {
      return timeout;
    }
  }
  
  // Default timeout
  return 30000; // 30 seconds
}
```

### Timeout Interceptor

```typescript
this.instance.interceptors.request.use(
  (config) => {
    // Set timeout based on endpoint
    const timeout = getTimeoutForEndpoint(config.url || '');
    config.timeout = timeout;
    
    if (import.meta.env.DEV) {
      console.log(`[Timeout] ${config.url} - ${timeout}ms`);
    }
    
    return config;
  }
);
```

---

## Connection Resilience

### Online/Offline Detection

```typescript
class ConnectionMonitor {
  private online: boolean = navigator.onLine;
  private listeners: Array<(online: boolean) => void> = [];
  
  constructor() {
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());
  }
  
  private handleOnline(): void {
    console.log('[Connection] Back online');
    this.online = true;
    this.notify(true);
  }
  
  private handleOffline(): void {
    console.log('[Connection] Offline');
    this.online = false;
    this.notify(false);
  }
  
  isOnline(): boolean {
    return this.online;
  }
  
  subscribe(listener: (online: boolean) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }
  
  private notify(online: boolean): void {
    this.listeners.forEach(listener => listener(online));
  }
}

// Global instance
export const connectionMonitor = new ConnectionMonitor();
```

### React Hook for Connection Status

```typescript
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(connectionMonitor.isOnline());
  
  useEffect(() => {
    const unsubscribe = connectionMonitor.subscribe(setIsOnline);
    return unsubscribe;
  }, []);
  
  return isOnline;
}

// Component usage
function ConnectionIndicator() {
  const isOnline = useOnlineStatus();
  
  if (isOnline) {
    return null; // Don't show anything when online
  }
  
  return (
    <div className="alert alert-warning">
      <strong>No internet connection</strong>
      <p>Please check your network connection</p>
    </div>
  );
}
```

### Request Queue for Offline Support

```typescript
interface QueuedRequest {
  id: string;
  config: AxiosRequestConfig;
  timestamp: number;
  retries: number;
}

class RequestQueue {
  private queue: QueuedRequest[] = [];
  private processing: boolean = false;
  
  enqueue(config: AxiosRequestConfig): string {
    const id = crypto.randomUUID();
    this.queue.push({
      id,
      config,
      timestamp: Date.now(),
      retries: 0
    });
    
    console.log(`[Queue] Enqueued request: ${config.url}`);
    
    // Try processing if online
    if (connectionMonitor.isOnline() && !this.processing) {
      this.process();
    }
    
    return id;
  }
  
  async process(): Promise<void> {
    if (this.processing || !connectionMonitor.isOnline()) {
      return;
    }
    
    this.processing = true;
    
    while (this.queue.length > 0 && connectionMonitor.isOnline()) {
      const request = this.queue[0];
      
      try {
        console.log(`[Queue] Processing: ${request.config.url}`);
        await apiClient.request(request.config);
        
        // Success, remove from queue
        this.queue.shift();
      } catch (error) {
        request.retries++;
        
        if (request.retries >= 3) {
          // Failed too many times, remove from queue
          console.error(`[Queue] Failed after ${request.retries} retries:`, request.config.url);
          this.queue.shift();
        } else {
          // Try again later
          console.warn(`[Queue] Retry ${request.retries}/3:`, request.config.url);
          await sleep(1000 * request.retries);
        }
      }
    }
    
    this.processing = false;
  }
  
  getQueuedCount(): number {
    return this.queue.length;
  }
  
  clear(): void {
    this.queue = [];
    console.log('[Queue] Cleared all queued requests');
  }
}

// Global instance
export const requestQueue = new RequestQueue();

// Auto-process when connection is restored
connectionMonitor.subscribe((online) => {
  if (online) {
    requestQueue.process();
  }
});
```

---

## Streaming Integration

### EventSource Setup

```typescript
interface StreamEvent {
  type: StreamEventType;
  data: any;
}

type StreamEventType = 'start' | 'chunk' | 'tool_call' | 'tool_result' | 'end' | 'error';

class StreamingClient {
  private eventSource: EventSource | null = null;
  
  async streamMessage(
    sessionId: string,
    message: string,
    onEvent: (event: StreamEvent) => void
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      const url = new URL('/api/v1/agent/messages/stream', apiConfig.baseURL);
      url.searchParams.set('session_id', sessionId);
      url.searchParams.set('message', message);
      
      this.eventSource = new EventSource(url.toString());
      
      // Handle different event types
      this.eventSource.addEventListener('start', (e) => {
        const data = JSON.parse(e.data);
        onEvent({ type: 'start', data });
      });
      
      this.eventSource.addEventListener('chunk', (e) => {
        const data = JSON.parse(e.data);
        onEvent({ type: 'chunk', data });
      });
      
      this.eventSource.addEventListener('tool_call', (e) => {
        const data = JSON.parse(e.data);
        onEvent({ type: 'tool_call', data });
      });
      
      this.eventSource.addEventListener('tool_result', (e) => {
        const data = JSON.parse(e.data);
        onEvent({ type: 'tool_result', data });
      });
      
      this.eventSource.addEventListener('end', (e) => {
        const data = JSON.parse(e.data);
        onEvent({ type: 'end', data });
        this.close();
        resolve();
      });
      
      this.eventSource.addEventListener('error', (e) => {
        const data = JSON.parse((e as MessageEvent).data || '{}');
        onEvent({ type: 'error', data });
        this.close();
        reject(new Error(data.error || 'Streaming error'));
      });
      
      // Handle connection errors
      this.eventSource.onerror = (error) => {
        console.error('[Streaming] Connection error:', error);
        this.close();
        reject(new Error('Streaming connection failed'));
      };
    });
  }
  
  close(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}
```

### React Hook for Streaming

```typescript
function useStreamingMessage(sessionId: string) {
  const [chunks, setChunks] = useState<string[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const streamingClientRef = useRef<StreamingClient>(new StreamingClient());
  
  const sendStreamingMessage = useCallback(async (message: string) => {
    setChunks([]);
    setIsStreaming(true);
    setError(null);
    
    try {
      await streamingClientRef.current.streamMessage(
        sessionId,
        message,
        (event) => {
          switch (event.type) {
            case 'chunk':
              setChunks(prev => [...prev, event.data.content]);
              break;
            case 'tool_call':
              console.log('[Streaming] Tool call:', event.data.tool);
              break;
            case 'end':
              setIsStreaming(false);
              break;
            case 'error':
              setError(new Error(event.data.error));
              setIsStreaming(false);
              break;
          }
        }
      );
    } catch (err) {
      setError(err as Error);
      setIsStreaming(false);
    }
  }, [sessionId]);
  
  const cancelStreaming = useCallback(() => {
    streamingClientRef.current.close();
    setIsStreaming(false);
  }, []);
  
  useEffect(() => {
    return () => {
      // Cleanup on unmount
      streamingClientRef.current.close();
    };
  }, []);
  
  return {
    chunks,
    fullMessage: chunks.join(''),
    isStreaming,
    error,
    sendStreamingMessage,
    cancelStreaming
  };
}
```

---

## Multi-Tenancy Integration

### Tenant Context Management

```typescript
interface TenantContext {
  tenantId: string;
  tenantName?: string;
  settings?: Record<string, any>;
}

class TenantManager {
  private static readonly STORAGE_KEY = 'current_tenant';
  private currentTenant: TenantContext;
  private listeners: Array<(tenant: TenantContext) => void> = [];
  
  constructor() {
    this.currentTenant = this.loadFromStorage();
  }
  
  private loadFromStorage(): TenantContext {
    const stored = localStorage.getItem(TenantManager.STORAGE_KEY);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch {
        // Invalid stored data
      }
    }
    
    // Default tenant
    return {
      tenantId: 'default',
      tenantName: 'Default Tenant'
    };
  }
  
  private saveToStorage(): void {
    localStorage.setItem(
      TenantManager.STORAGE_KEY,
      JSON.stringify(this.currentTenant)
    );
  }
  
  getCurrentTenant(): TenantContext {
    return { ...this.currentTenant };
  }
  
  setTenant(tenant: TenantContext): void {
    this.currentTenant = tenant;
    this.saveToStorage();
    this.notify(tenant);
  }
  
  subscribe(listener: (tenant: TenantContext) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }
  
  private notify(tenant: TenantContext): void {
    this.listeners.forEach(listener => listener(tenant));
  }
}

// Global instance
export const tenantManager = new TenantManager();

// Helper function for API client
export function getCurrentTenantId(): string {
  return tenantManager.getCurrentTenant().tenantId;
}
```

### React Hook for Tenant

```typescript
function useTenant() {
  const [tenant, setTenant] = useState(tenantManager.getCurrentTenant());
  
  useEffect(() => {
    const unsubscribe = tenantManager.subscribe(setTenant);
    return unsubscribe;
  }, []);
  
  const switchTenant = useCallback((newTenant: TenantContext) => {
    tenantManager.setTenant(newTenant);
  }, []);
  
  return {
    tenant,
    tenantId: tenant.tenantId,
    tenantName: tenant.tenantName,
    switchTenant
  };
}
```

---

## Testing API Integration

### Mock API Client

```typescript
class MockAPIClient extends APIClient {
  private mocks = new Map<string, any>();
  
  mock(endpoint: string, response: any): void {
    this.mocks.set(endpoint, response);
  }
  
  async request<T>(config: AxiosRequestConfig): Promise<T> {
    const mockResponse = this.mocks.get(config.url || '');
    
    if (mockResponse) {
      // Simulate network delay
      await sleep(100);
      return mockResponse;
    }
    
    return super.request(config);
  }
}
```

### Integration Test Example

```typescript
describe('API Integration', () => {
  let apiClient: MockAPIClient;
  
  beforeEach(() => {
    apiClient = new MockAPIClient();
  });
  
  it('should handle rate limit errors', async () => {
    apiClient.mock('/api/v1/agent/messages', {
      status: 429,
      data: {
        error: 'Rate Limit Exceeded',
        retry_after: 1
      }
    });
    
    await expect(
      apiClient.post('/api/v1/agent/messages', {
        session_id: 'test',
        message: 'Hello'
      })
    ).rejects.toThrow('Rate limit exceeded');
  });
  
  it('should retry on server errors', async () => {
    let attempts = 0;
    apiClient.mock('/api/v1/health', () => {
      attempts++;
      if (attempts < 3) {
        throw new Error('Server error');
      }
      return { status: 'healthy' };
    });
    
    const result = await apiClient.get('/api/v1/health');
    expect(result.status).toBe('healthy');
    expect(attempts).toBe(3);
  });
});
```

---

## Summary

This integration guide provides:

✅ **Robust Error Handling**: Classify and handle all error types  
✅ **Smart Retry Logic**: Exponential backoff with jitter  
✅ **Rate Limit Management**: Proactive and reactive handling  
✅ **Circuit Breaker**: Prevent cascading failures  
✅ **Timeout Configuration**: Per-endpoint timeout tuning  
✅ **Connection Resilience**: Offline support and request queuing  
✅ **Streaming Support**: EventSource integration for real-time  
✅ **Multi-Tenancy**: Tenant context management  
✅ **Testability**: Mock API client for testing

---

## Best Practices

1. **Always handle errors gracefully**: Never let errors crash the app
2. **Provide user feedback**: Keep users informed of operation status
3. **Respect rate limits**: Check headers and implement backoff
4. **Log everything**: All API calls, errors, and retries
5. **Test offline scenarios**: Ensure app works without connection
6. **Monitor performance**: Track API response times
7. **Use circuit breakers**: Protect against failing services
8. **Implement timeouts**: Don't wait forever for responses

For architecture details, see [Frontend Architecture](./FRONTEND_ARCHITECTURE.md).
For API reference, see [API Specification](./API_SPECIFICATION.md).
