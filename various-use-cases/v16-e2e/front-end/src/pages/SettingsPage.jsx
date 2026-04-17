import PageContainer from '../shared/components/layout/PageContainer.jsx'

/**
 * Settings page.
 * Phase 1 stub. Theme and tenant settings will be added in Phase 2/6.
 * Ref: FRONTEND_ARCHITECTURE.md — Routes → SettingsPage
 */
function SettingsPage() {
  return (
    <PageContainer title="Settings" subtitle="Configure your preferences">
      <div className="row g-4">

        {/* Theme settings — Phase 2 */}
        <div className="col-12 col-md-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-palette me-2 text-primary" />
                Appearance
              </h3>
            </div>
            <div className="card-body">
              <p className="text-muted small">
                Theme toggle (light/dark) will be available in Phase 2.
              </p>
              <div className="d-flex gap-2">
                <button className="btn btn-sm btn-outline-secondary" disabled>
                  <i className="ti ti-sun me-1" />Light
                </button>
                <button className="btn btn-sm btn-outline-secondary" disabled>
                  <i className="ti ti-moon me-1" />Dark
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Tenant settings — Phase 6 */}
        <div className="col-12 col-md-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-building me-2 text-primary" />
                Tenant
              </h3>
            </div>
            <div className="card-body">
              <p className="text-muted small">
                Tenant management will be available in Phase 6.
              </p>
              <div className="d-flex align-items-center gap-2">
                <span className="badge bg-primary-lt text-primary">
                  <i className="ti ti-building me-1" />
                  default
                </span>
                <span className="text-muted small">Personal Workspace</span>
              </div>
            </div>
          </div>
        </div>

        {/* API config */}
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-api me-2 text-primary" />
                API Configuration
              </h3>
            </div>
            <div className="card-body">
              <dl className="row mb-0">
                <dt className="col-sm-3 text-muted">Base URL</dt>
                <dd className="col-sm-9">
                  <code>{import.meta.env.VITE_API_BASE_URL || 'http://localhost:9080'}</code>
                </dd>
                <dt className="col-sm-3 text-muted">Streaming</dt>
                <dd className="col-sm-9">
                  {import.meta.env.VITE_ENABLE_STREAMING !== 'false'
                    ? <span className="badge bg-success-lt text-success">Enabled</span>
                    : <span className="badge bg-secondary-lt text-secondary">Disabled</span>
                  }
                </dd>
              </dl>
            </div>
          </div>
        </div>

      </div>
    </PageContainer>
  )
}

export default SettingsPage
