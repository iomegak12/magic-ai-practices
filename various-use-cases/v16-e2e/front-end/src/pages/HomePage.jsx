import { Link } from 'react-router-dom'
import PageContainer from '../shared/components/layout/PageContainer.jsx'

/**
 * Home / Landing page — project overview for MSEv15E2E Customer Service Agent.
 * Ref: FRONTEND_ARCHITECTURE.md — Routes → HomePage
 *      v16-e2e/docs/product-specification.md — product context
 */

// ─── Stat tile used in the "By the Numbers" row ─────────────────────────────
function StatTile({ icon, value, label, color = 'primary' }) {
  return (
    <div className="col-6 col-sm-3">
      <div className={`card card-sm border-${color} h-100`}>
        <div className="card-body text-center p-3">
          <div className={`mb-2 text-${color}`}>
            <i className={`ti ${icon} fs-2`} />
          </div>
          <div className={`fs-1 fw-bold text-${color} lh-1`}>{value}</div>
          <div className="text-muted small mt-1">{label}</div>
        </div>
      </div>
    </div>
  )
}

// ─── Capability card ─────────────────────────────────────────────────────────
function CapabilityCard({ icon, color, title, description, badge }) {
  return (
    <div className="col-12 col-sm-6 col-lg-4">
      <div className="card h-100 shadow-sm">
        <div className="card-body d-flex flex-column p-4">
          <div className={`avatar avatar-md bg-${color}-lt rounded-3 mb-3`}>
            <i className={`ti ${icon} fs-4 text-${color}`} />
          </div>
          <h4 className="card-title mb-1">
            {title}
            {badge && (
              <span className={`badge bg-${color}-lt text-${color} ms-2 fs-6 align-middle`}>
                {badge}
              </span>
            )}
          </h4>
          <p className="text-muted small mb-0 flex-grow-1">{description}</p>
        </div>
      </div>
    </div>
  )
}

// ─── Tech pill ───────────────────────────────────────────────────────────────
function TechPill({ icon, label, color = 'secondary' }) {
  return (
    <span className={`badge bg-${color}-lt text-${color} px-3 py-2 fs-6 d-inline-flex align-items-center gap-1`}>
      <i className={`ti ${icon}`} />
      {label}
    </span>
  )
}

// ─── Main component ──────────────────────────────────────────────────────────
function HomePage() {
  return (
    <PageContainer>
      {/* ── HERO ─────────────────────────────────────────────────────────────── */}
      <div className="row align-items-center py-4 py-md-6 g-4">
        <div className="col-12 col-md-7 order-2 order-md-1">
          <div className="d-flex align-items-center gap-2 mb-3">
            <span className="badge bg-primary text-white px-3 py-2">
              <i className="ti ti-sparkles me-1" />
              MSEv15E2E · v0.1.0
            </span>
            <span className="badge bg-success-lt text-success px-3 py-2">
              <i className="ti ti-circle-check me-1" />
              Production Ready
            </span>
          </div>
          <h1 className="display-5 fw-bold mb-3" style={{ lineHeight: 1.2 }}>
            AI-Powered{' '}
            <span className="text-primary">Customer Service</span>{' '}
            Agent
          </h1>
          <p className="text-muted fs-4 mb-4" style={{ maxWidth: 520 }}>
            Intelligent conversational support with complaint management,
            order tracking, and real-time streaming — built on Azure OpenAI
            and FastAPI.
          </p>
          <div className="d-flex flex-wrap gap-2">
            <Link to="/support" className="btn btn-primary btn-lg px-4">
              <i className="ti ti-headset me-2" />
              Start Chat
            </Link>
            <Link to="/about" className="btn btn-outline-secondary btn-lg px-4">
              <i className="ti ti-info-circle me-2" />
              About the Project
            </Link>
          </div>
        </div>

        <div className="col-12 col-md-5 order-1 order-md-2 text-center">
          <div
            className="bg-primary-lt rounded-4 d-inline-flex align-items-center justify-content-center"
            style={{ width: '100%', maxWidth: 360, aspectRatio: '1 / 1' }}
          >
            <i className="ti ti-robot text-primary" style={{ fontSize: '8rem' }} />
          </div>
        </div>
      </div>

      {/* ── BY THE NUMBERS ───────────────────────────────────────────────────── */}
      <div className="row g-3 mb-5">
        <StatTile icon="ti-message-chatbot" value="∞" label="Concurrent Sessions" color="primary" />
        <StatTile icon="ti-tools"           value="8+"  label="Agent Tools"         color="warning" />
        <StatTile icon="ti-building-skyscraper" value="N"  label="Tenants Supported"  color="success" />
        <StatTile icon="ti-activity"        value="SSE" label="Real-time Streaming" color="danger"  />
      </div>

      {/* ── CAPABILITIES ─────────────────────────────────────────────────────── */}
      <div className="mb-5">
        <div className="mb-4">
          <h2 className="fw-bold mb-1">What the Agent Can Do</h2>
          <p className="text-muted">
            A unified conversational interface backed by a multi-tool AI agent.
          </p>
        </div>
        <div className="row g-3">
          <CapabilityCard
            icon="ti-file-description"
            color="primary"
            title="Complaint Management"
            badge="MCP"
            description="Register, search, resolve, and archive customer complaints through an external MCP server integration with full lifecycle support."
          />
          <CapabilityCard
            icon="ti-shopping-cart"
            color="warning"
            title="Order Management"
            description="Search orders by customer or date range, retrieve order details, and modify order statuses — all powered by local agent tools."
          />
          <CapabilityCard
            icon="ti-mail"
            color="cyan"
            title="Email Communication"
            description="Send contextual email notifications directly from within a conversation, keeping customers informed at every step."
          />
          <CapabilityCard
            icon="ti-bolt"
            color="danger"
            title="Real-time Streaming"
            badge="SSE"
            description="Server-Sent Events stream token-by-token responses, delivering a responsive chat experience without polling."
          />
          <CapabilityCard
            icon="ti-history"
            color="purple"
            title="Session Management"
            description="Multi-turn conversations with full history persistence. Resume any session and review past interactions at any time."
          />
          <CapabilityCard
            icon="ti-building-skyscraper"
            color="success"
            title="Multi-tenancy"
            description="Isolated workspaces per tenant with independent session data, ensuring enterprise-grade data separation and security."
          />
        </div>
      </div>

      {/* ── ARCHITECTURE OVERVIEW ────────────────────────────────────────────── */}
      <div className="row g-4 mb-5 align-items-stretch">
        <div className="col-12 col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header">
              <h3 className="card-title mb-0">
                <i className="ti ti-layers-intersect me-2 text-primary" />
                Architecture at a Glance
              </h3>
            </div>
            <div className="card-body">
              <div className="d-flex flex-column gap-3">
                {[
                  { icon: 'ti-brand-react',   color: 'primary', layer: 'Frontend',     desc: 'React 18 + Vite · Tabler UI · Axios + SSE' },
                  { icon: 'ti-server',         color: 'warning', layer: 'Backend',      desc: 'FastAPI (Python) · Uvicorn · Azure OpenAI' },
                  { icon: 'ti-puzzle',         color: 'success', layer: 'MCP Server',   desc: 'Complaint Management via Model Context Protocol' },
                  { icon: 'ti-database',       color: 'cyan',    layer: 'Data Store',   desc: 'Session & tenant data · Order CRM system' },
                  { icon: 'ti-container',      color: 'purple',  layer: 'Deployment',   desc: 'Docker · Alpine Linux · Docker Compose' },
                ].map(({ icon, color, layer, desc }) => (
                  <div key={layer} className="d-flex align-items-start gap-3">
                    <div className={`avatar avatar-sm bg-${color}-lt rounded-2 flex-shrink-0`}>
                      <i className={`ti ${icon} text-${color}`} />
                    </div>
                    <div>
                      <div className="fw-semibold lh-1">{layer}</div>
                      <div className="text-muted small">{desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header">
              <h3 className="card-title mb-0">
                <i className="ti ti-route me-2 text-warning" />
                How It Works
              </h3>
            </div>
            <div className="card-body">
              <ol className="list-group list-group-flush list-group-numbered">
                {[
                  { title: 'Create a Session',    desc: 'A unique session is created per tenant, preserving full conversation context.' },
                  { title: 'Send a Message',      desc: 'Your message is forwarded to the Azure OpenAI-backed CustomerServiceAgent.' },
                  { title: 'Agent Reasons',       desc: 'The agent selects the right tools — complaint, order, or email — and executes them.' },
                  { title: 'Stream the Response', desc: 'Tokens stream back in real-time via SSE, so you see results as they are generated.' },
                  { title: 'History Persisted',   desc: 'Every turn is stored server-side; switch sessions or replay history any time.' },
                ].map(({ title, desc }) => (
                  <li key={title} className="list-group-item px-0 py-2 border-0">
                    <div className="fw-semibold">{title}</div>
                    <div className="text-muted small">{desc}</div>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        </div>
      </div>

      {/* ── TECH STACK ───────────────────────────────────────────────────────── */}
      <div className="card shadow-sm mb-5">
        <div className="card-header">
          <h3 className="card-title mb-0">
            <i className="ti ti-code me-2 text-success" />
            Technology Stack
          </h3>
        </div>
        <div className="card-body d-flex flex-wrap gap-2">
          <TechPill icon="ti-brand-azure"   label="Azure OpenAI"  color="primary"  />
          <TechPill icon="ti-brand-python"  label="FastAPI"       color="warning"  />
          <TechPill icon="ti-brand-react"   label="React 18"      color="cyan"     />
          <TechPill icon="ti-bolt"          label="Vite 6"        color="purple"   />
          <TechPill icon="ti-puzzle"        label="MCP Protocol"  color="success"  />
          <TechPill icon="ti-activity"      label="SSE Streaming" color="danger"   />
          <TechPill icon="ti-container"     label="Docker"        color="azure"    />
          <TechPill icon="ti-server"        label="Uvicorn"       color="teal"     />
          <TechPill icon="ti-shield-lock"   label="Rate Limiting" color="orange"   />
          <TechPill icon="ti-building"      label="Multi-tenant"  color="lime"     />
        </div>
      </div>

      {/* ── CALL TO ACTION ───────────────────────────────────────────────────── */}
      <div className="card bg-primary text-white shadow mb-4">
        <div className="card-body text-center py-5 px-3">
          <i className="ti ti-headset mb-3" style={{ fontSize: '3rem' }} />
          <h2 className="text-white fw-bold mb-2">Ready to Chat?</h2>
          <p className="text-white-50 mb-4 fs-4">
            Open the Support page to start a session with the AI agent.
          </p>
          <Link to="/support" className="btn btn-white btn-lg px-5">
            <i className="ti ti-arrow-right me-2" />
            Open Support Chat
          </Link>
        </div>
      </div>
    </PageContainer>
  )
}

export default HomePage
