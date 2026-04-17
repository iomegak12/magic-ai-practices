# Multi-Tenancy Guide

**Version:** 1.0.0  
**Last Updated:** February 20, 2026

## Table of Contents

- [Overview](#overview)
- [Multi-Tenancy Concept](#multi-tenancy-concept)
- [Tenant Architecture](#tenant-architecture)
- [Tenant Selection UI](#tenant-selection-ui)
- [Tenant Context Management](#tenant-context-management)
- [API Integration](#api-integration)
- [Storage Patterns](#storage-patterns)
- [Routing Strategies](#routing-strategies)
- [Tenant Switching](#tenant-switching)
- [Best Practices](#best-practices)

---

## Overview

This guide explains how to implement multi-tenancy in the Customer Service Agent Web UI. The application supports multiple tenants with data isolation at the API level.

### What is Multi-Tenancy?

Multi-tenancy allows a single instance of the application to serve multiple customers (tenants) with isolated data. Each tenant has:

- **Isolated Sessions**: Sessions are scoped to a tenant
- **Separate History**: Message history per tenant
- **Independent Stats**: Usage statistics per tenant
- **Shared Infrastructure**: Same application instance

---

## Multi-Tenancy Concept

### Tenant Model

```typescript
interface Tenant {
  id: string;           // Unique identifier (e.g., "acme-corp", "default")
  name: string;         // Display name (e.g., "Acme Corporation")
  displayName?: string; // Optional friendly name
  settings?: {          // Optional tenant-specific settings
    allowStreaming?: boolean;
    maxMessageLength?: number;
    theme?: 'light' | 'dark';
  };
  metadata?: any;       // Additional metadata
}
```

### Default Tenant

If no tenant is specified, the system uses **"default"** as the tenant ID.

```typescript
const DEFAULT_TENANT: Tenant = {
  id: 'default',
  name: 'Default Tenant',
  displayName: 'Personal Workspace'
};
```

### Tenant Identification

Tenants are identified by `tenant_id` query parameter in API requests:

```
GET /api/v1/sessions/?tenant_id=acme-corp
GET /api/v1/sessions/sess_123/history?tenant_id=acme-corp
DELETE /api/v1/sessions/sess_123?tenant_id=acme-corp
```

---

## Tenant Architecture

### Data Flow

```
┌─────────────────┐
│   UI Layer      │
│  (React/Vite)   │
└────────┬────────┘
         │ tenant_id in context
         ↓
┌─────────────────┐
│  API Client     │
│  (Axios)        │
└────────┬────────┘
         │ tenant_id in query param
         ↓
┌─────────────────┐
│  Backend API    │
│  (FastAPI)      │
└────────┬────────┘
         │ tenant_id filtering
         ↓
┌─────────────────┐
│   Database      │
│  (per-tenant)   │
└─────────────────┘
```

### Isolation Levels

1. **UI Level**: Tenant selector in navbar
2. **API Client Level**: Automatic tenant_id injection
3. **Backend Level**: Tenant-scoped queries
4. **Storage Level**: Separate database/tables per tenant

---

## Tenant Selection UI

### Tenant Selector Component

**Location**: Top-right corner of navbar

**Visual Design**:
```
┌──────────────────────────────────┐
│ Logo   Title         [v Acme Corp] 👤 │
└──────────────────────────────────┘
                      ↑
                   Tenant Selector
```

**Dropdown Content**:
```
┌────────────────────────────┐
│ Select Tenant              │
├────────────────────────────┤
│ ✓ Acme Corp                │ (Active)
│   Beta Inc.                │
│   Charlie Ltd.             │
├────────────────────────────┤
│ + Add Tenant               │
└────────────────────────────┘
```

### Tenant Indicator

Show current tenant in multiple places:

1. **Navbar**: Dropdown selector
2. **Sidebar**: Small badge
3. **Page Title**: Subtitle (optional)

**Badge Design**:
- Small, rounded badge
- Tenant name or ID
- Color-coded by tenant (optional)
- Icon: 🏢 or tenant logo

### Add Tenant UI

**Form Fields**:
```
┌────────────────────────────┐
│ Add New Tenant          × │
├────────────────────────────┤
│                            │
│ Tenant ID *                │
│ [_______________]          │
│ (lowercase, no spaces)     │
│                            │
│ Display Name *             │
│ [_______________]          │
│                            │
│        [Cancel] [Add]      │
└────────────────────────────┘
```

**Validation**:
- Tenant ID: lowercase, alphanumeric, hyphens only
- Display Name: any string
- Check for duplicate tenant IDs

---

## Tenant Context Management

### React Context

**Create Tenant Context**:

```typescript
// Tenant context structure
interface TenantContextValue {
  currentTenant: Tenant;
  tenants: Tenant[];
  switchTenant: (tenantId: string) => Promise<void>;
  addTenant: (tenant: Tenant) => Promise<void>;
  removeTenant: (tenantId: string) => Promise<void>;
  isLoading: boolean;
  error: Error | null;
}

// Provider component pattern
<TenantProvider>
  <App />
</TenantProvider>
```

### Hook for Tenant Access

```typescript
// Usage in components
const { currentTenant, switchTenant } = useTenant();

// Get current tenant ID
const tenantId = currentTenant.id;

// Switch tenant
await switchTenant('new-tenant-id');
```

### Tenant State Management

**Storage**:
- **Current Tenant**: localStorage (`current_tenant`)
- **Tenant List**: localStorage (`tenant_list`)
- **Tenant Settings**: localStorage (`tenant_settings_${tenantId}`)

**State Updates**:
1. User selects tenant from dropdown
2. Update React context
3. Save to localStorage
4. Clear cached data for old tenant
5. Fetch data for new tenant
6. Update URL (optional)

---

## API Integration

### Automatic Tenant Injection

**Request Interceptor**:

Add `tenant_id` to all requests automatically:

```typescript
// Pseudo-code for axios interceptor
axiosInstance.interceptors.request.use((config) => {
  const tenantId = getTenantFromContext(); // From React context
  
  // Add tenant_id to query params
  if (config.url?.includes('/sessions')) {
    config.params = {
      ...config.params,
      tenant_id: tenantId
    };
  }
  
  // Also add as header for logging
  config.headers['X-Tenant-ID'] = tenantId;
  
  return config;
});
```

**Manual Override**:

Allow overriding tenant for specific requests:

```typescript
// Override tenant for this request only
const response = await apiClient.get('/api/v1/sessions/', {
  params: {
    tenant_id: 'custom-tenant'  // Override
  }
});
```

### Tenant-Scoped Endpoints

**Session Management**:
- GET `/api/v1/sessions/?tenant_id=acme-corp` - List sessions
- GET `/api/v1/sessions/{id}/history?tenant_id=acme-corp` - Get history
- DELETE `/api/v1/sessions/{id}?tenant_id=acme-corp` - Delete session
- POST `/api/v1/sessions/{id}/cleanup?tenant_id=acme-corp` - Cleanup

**Stats Endpoint**:
- GET `/api/v1/sessions/stats` - Returns stats for all tenants
  
  Response includes `sessions_by_tenant`:
  ```json
  {
    "sessions_by_tenant": {
      "default": 10,
      "acme-corp": 25,
      "beta-inc": 5
    }
  }
  ```

**Agent Endpoints** (Not Tenant-Scoped):
- POST `/api/v1/agent/sessions` - Create session (no tenant_id)
- POST `/api/v1/agent/messages` - Send message (no tenant_id)

> **Note**: Agent endpoints do not use tenant_id. Tenancy is for session management only.

---

## Storage Patterns

### LocalStorage Keys

**Pattern**: Prefix all keys with tenant ID

```typescript
// Tenant-specific keys
`tenant_${tenantId}_sessions`       // Cached sessions
`tenant_${tenantId}_settings`       // User settings
`tenant_${tenantId}_drafts`         // Message drafts

// Global keys
`current_tenant_id`                 // Current tenant ID
`tenant_list`                       // Available tenants
```

**Benefits**:
- Isolate data per tenant
- Easy to clear tenant data
- No cross-tenant data leaks

### Clear Tenant Data

```typescript
// Clear all data for a tenant
function clearTenantData(tenantId: string): void {
  const keysToRemove: string[] = [];
  
  // Find all keys for this tenant
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key?.startsWith(`tenant_${tenantId}_`)) {
      keysToRemove.push(key);
    }
  }
  
  // Remove all tenant keys
  keysToRemove.forEach(key => localStorage.removeItem(key));
  
  console.log(`Cleared ${keysToRemove.length} items for tenant ${tenantId}`);
}
```

### IndexedDB (Advanced)

For larger datasets, use IndexedDB with tenant isolation:

```typescript
// Database per tenant
const dbName = `tenant_${tenantId}_sessions`;
const db = await openDB(dbName, 1, {
  upgrade(db) {
    db.createObjectStore('sessions', { keyPath: 'session_id' });
    db.createObjectStore('messages', { keyPath: 'id' });
  }
});
```

---

## Routing Strategies

### Strategy 1: Query Parameter (Recommended)

**Pattern**: `?tenant={tenant_id}`

**Examples**:
- `/chat?tenant=acme-corp`
- `/sessions?tenant=acme-corp`
- `/stats?tenant=acme-corp`

**Pros**:
- Simple implementation
- No routing changes
- Easy to share URLs
- Optional (defaults to current tenant)

**Cons**:
- Visible in URL
- Can be manually changed

### Strategy 2: Path Parameter

**Pattern**: `/t/{tenant_id}/...`

**Examples**:
- `/t/acme-corp/chat`
- `/t/acme-corp/sessions`
- `/t/acme-corp/stats`

**Pros**:
- Clean URLs
- Explicit tenant context
- SEO-friendly

**Cons**:
- Requires routing changes
- More complex implementation
- Harder to switch tenants

### Strategy 3: State Only (Simplest)

**Pattern**: No tenant in URL, use context only

**Pros**:
- Simplest implementation
- No URL pollution
- Controlled by UI only

**Cons**:
- Cannot share tenant-specific URLs
- Must use UI to switch tenants
- Lost on page refresh (unless persisted)

### Recommended Approach

Use **Strategy 1 (Query Parameter)** with fallback to context:

```typescript
// On component mount
useEffect(() => {
  const urlTenant = searchParams.get('tenant');
  const contextTenant = currentTenant.id;
  
  if (urlTenant && urlTenant !== contextTenant) {
    // URL takes precedence
    switchTenant(urlTenant);
  } else if (!urlTenant) {
    // Add tenant to URL
    searchParams.set('tenant', contextTenant);
    setSearchParams(searchParams);
  }
}, []);
```

---

## Tenant Switching

### Switching Flow

```
1. User clicks tenant selector
   ↓
2. Select new tenant from dropdown
   ↓
3. Confirmation: "Switch to Beta Inc.?"
   (if unsaved changes)
   ↓
4. Update React context
   ↓
5. Save to localStorage
   ↓
6. Clear old tenant cache
   ↓
7. Update URL (optional)
   ↓
8. Fetch new tenant data
   ↓
9. Update UI
   ↓
10. Show success toast
```

### Handling State on Switch

**Clear Cached Data**:
- Session list
- Message history
- Stats
- Drafts (optionally, with confirmation)

**Preserve Global State**:
- Theme preference
- UI settings (sidebar collapsed, etc.)
- Navigation history

**API Behavior**:
- Cancel in-flight requests
- Start new requests with new tenant_id
- Clear rate limit trackers

### Unsaved Changes Warning

If user has unsaved changes (draft message):

```
┌────────────────────────────┐
│ Switch Tenant?          × │
├────────────────────────────┤
│                            │
│ You have unsaved changes   │
│ in the current session.    │
│                            │
│ Would you like to:         │
│                            │
│ [ ] Save draft             │
│ [ ] Discard changes        │
│                            │
│    [Cancel] [Continue]     │
└────────────────────────────┘
```

---

## Best Practices

### 1. Default Tenant

Always provide a default tenant:

```typescript
const DEFAULT_TENANT_ID = 'default';

// On app initialization
if (!localStorage.getItem('current_tenant_id')) {
  localStorage.setItem('current_tenant_id', DEFAULT_TENANT_ID);
}
```

### 2. Tenant Validation

Validate tenant before making requests:

```typescript
async function validateTenant(tenantId: string): Promise<boolean> {
  try {
    // Try fetching sessions for this tenant
    await apiClient.get('/api/v1/sessions/', {
      params: { tenant_id: tenantId, limit: 1 }
    });
    return true;
  } catch (error) {
    console.error(`Invalid tenant: ${tenantId}`, error);
    return false;
  }
}
```

### 3. Tenant Context Provider

Wrap entire app in tenant provider:

```typescript
<TenantProvider>
  <Router>
    <App />
  </Router>
</TenantProvider>
```

### 4. Error Handling

Handle tenant-specific errors:

```typescript
if (error.response?.status === 404 && error.response?.data?.detail?.includes('tenant')) {
  // Tenant not found
  showError('Tenant not found. Switching to default tenant.');
  await switchTenant(DEFAULT_TENANT_ID);
}
```

### 5. Tenant Selector Visibility

Show tenant selector only if multiple tenants:

```typescript
{tenants.length > 1 && <TenantSelector />}
```

### 6. Audit Logging

Log tenant switches for audit:

```typescript
function logTenantSwitch(fromTenant: string, toTenant: string): void {
  console.log('[Audit] Tenant switch', {
    from: fromTenant,
    to: toTenant,
    timestamp: new Date().toISOString(),
    user: getCurrentUser(), // If auth is added
  });
  
  // Send to analytics (future)
}
```

### 7. Tenant-Specific Settings

Allow per-tenant settings:

```typescript
interface TenantSettings {
  theme: 'light' | 'dark';
  language: string;
  enableStreaming: boolean;
  maxMessageLength: number;
}

// Save settings per tenant
localStorage.setItem(
  `tenant_${tenantId}_settings`,
  JSON.stringify(settings)
);
```

### 8. URL Sync

Keep URL in sync with current tenant:

```typescript
useEffect(() => {
  const currentUrlTenant = searchParams.get('tenant');
  
  if (currentUrlTenant !== currentTenant.id) {
    searchParams.set('tenant', currentTenant.id);
    setSearchParams(searchParams, { replace: true });
  }
}, [currentTenant.id]);
```

---

## Multi-Tenant UI Patterns

### Tenant Badge in Messages

Show tenant badge in session list:

```
┌────────────────────────────┐
│ Session #12345             │
│ [Acme Corp] 10 messages    │
│ 2 hours ago                │
└────────────────────────────┘
```

### Tenant Filter

Allow filtering by tenant in stats:

```
┌────────────────────────────┐
│ Sessions Statistics        │
├────────────────────────────┤
│ Tenant: [All      ▼]       │
│                            │
│ Total: 45 sessions         │
│ Active: 12 sessions        │
│ Expired: 8 sessions        │
└────────────────────────────┘
```

### Tenant-Specific Colors (Optional)

Assign colors to tenants for visual distinction:

```typescript
const TENANT_COLORS = {
  'default': '#3498db',     // Blue
  'acme-corp': '#e74c3c',   // Red
  'beta-inc': '#2ecc71',    // Green
  'charlie-ltd': '#f39c12', // Orange
};

// Use in UI
<div style={{ borderLeft: `4px solid ${TENANT_COLORS[tenantId]}` }}>
  ...
</div>
```

---

## Security Considerations

### Client-Side Tenancy

**Important**: Tenancy is implemented on the client side for UI convenience. The backend API enforces true isolation.

**Risks**:
- User can manually change tenant_id in URL/DevTools
- No authentication to verify tenant access

**Mitigations**:
1. Backend validates tenant access (if auth is added)
2. Clear separation of tenant data in backend
3. Client-side tenancy is for UX only

### Future: Backend Validation

When authentication is added:

```typescript
// Backend checks user's tenant membership
if (!user.tenants.includes(tenant_id)) {
  throw new HTTPException(403, "Access denied to this tenant");
}
```

### Tenant ID Format

Enforce safe tenant ID format:

```typescript
function isValidTenantId(tenantId: string): boolean {
  // Only lowercase alphanumeric and hyphens
  return /^[a-z0-9-]+$/.test(tenantId);
}
```

---

## Testing Multi-Tenancy

### Manual Testing

**Tenant Switching**:
1. Create sessions in tenant A
2. Switch to tenant B
3. Verify sessions from tenant A are not visible
4. Create sessions in tenant B
5. Switch back to tenant A
6. Verify tenant A sessions are still there

**Data Isolation**:
1. Create session in tenant A
2. Note session ID
3. Switch to tenant B
4. Try accessing session from tenant A (should fail)

**Storage Isolation**:
1. Open DevTools > Application > Local Storage
2. Verify keys are prefixed with tenant IDs
3. Switch tenants
4. Verify data is cleared/loaded correctly

### Automated Testing

```typescript
describe('Multi-Tenancy', () => {
  it('should isolate sessions by tenant', async () => {
    // Create session in tenant A
    await switchTenant('tenant-a');
    const sessionA = await createSession();
    
    // Switch to tenant B
    await switchTenant('tenant-b');
    const sessionsB = await getSessions();
    
    // Session A should not be in tenant B
    expect(sessionsB).not.toContainEqual(sessionA);
  });
  
  it('should inject tenant_id in API requests', async () => {
    await switchTenant('tenant-a');
    
    // Intercept API call
    const request = await apiClient.get('/api/v1/sessions/');
    
    // Verify tenant_id is present
    expect(request.params.tenant_id).toBe('tenant-a');
  });
});
```

---

## Troubleshooting

### Issue: Sessions Not Loading After Tenant Switch

**Symptom**: Session list is empty after switching tenants

**Causes**:
1. tenant_id not injected in API request
2. Cache not cleared
3. API error not handled

**Solution**:
```typescript
// Clear cache on tenant switch
const switchTenant = async (tenantId: string) => {
  // Clear session cache
  sessionCache.clear();
  
  // Update context
  setCurrentTenant(tenantId);
  
  // Fetch new data
  await fetchSessions(tenantId);
};
```

### Issue: Wrong Tenant Data Displayed

**Symptom**: Old tenant's data still showing

**Causes**:
1. State not cleared
2. Request in-flight with old tenant_id
3. Cache not invalidated

**Solution**:
```typescript
// Cancel in-flight requests
axiosInstance.interceptors.request.use((config) => {
  // Add cancellation token
  config.cancelToken = new axios.CancelToken((cancel) => {
    cancelTokens.push(cancel);
  });
  return config;
});

// On tenant switch
cancelTokens.forEach(cancel => cancel('Tenant switched'));
cancelTokens = [];
```

### Issue: Tenant Not Persisting on Refresh

**Symptom**: Reverts to default tenant on page reload

**Causes**:
1. Not saved to localStorage
2. localStorage key mismatch
3. Initialization order issue

**Solution**:
```typescript
// Save immediately on switch
const switchTenant = (tenantId: string) => {
  localStorage.setItem('current_tenant_id', tenantId);
  setCurrentTenant(tenantId);
};

// Load on mount
useEffect(() => {
  const savedTenant = localStorage.getItem('current_tenant_id') || DEFAULT_TENANT_ID;
  setCurrentTenant(savedTenant);
}, []);
```

---

## Summary

This multi-tenancy guide provides:

✅ **Tenant Concept**: Understanding tenant isolation  
✅ **UI Patterns**: Tenant selector, badges, filters  
✅ **Context Management**: React context, hooks  
✅ **API Integration**: Automatic tenant_id injection  
✅ **Storage Patterns**: Tenant-prefixed keys  
✅ **Routing Strategies**: Query params, path, state-only  
✅ **Tenant Switching**: Flow, state management  
✅ **Best Practices**: Defaults, validation, error handling  
✅ **Security**: Client-side limitations, future auth  
✅ **Testing**: Manual and automated approaches

---

## Next Steps

1. Review tenant strategy
2. Implement tenant context
3. Build tenant selector UI
4. Test tenant isolation
5. Add tenant validation (when auth is ready)

For API details, see [API Specification](./API_SPECIFICATION.md).
For integration patterns, see [Integration Guide](./INTEGRATION_GUIDE.md).
