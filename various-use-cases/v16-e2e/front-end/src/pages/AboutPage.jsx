import PageContainer from '../shared/components/layout/PageContainer.jsx'

/**
 * About page — author profile + project background.
 * Author profile sourced from: https://github.com/iomegak12
 * Ref: FRONTEND_ARCHITECTURE.md — Routes → AboutPage
 */

// ─── Certification badge ─────────────────────────────────────────────────────
function CertBadge({ icon, title, issuer, color = 'primary' }) {
  return (
    <div className="col-12 col-sm-6">
      <div className={`d-flex align-items-start gap-3 p-3 rounded-3 bg-${color}-lt`}>
        <div className={`avatar avatar-sm bg-${color} rounded-2 flex-shrink-0`}>
          <i className={`ti ${icon} text-white`} />
        </div>
        <div>
          <div className={`fw-semibold text-${color} small lh-sm`}>{title}</div>
          <div className="text-muted" style={{ fontSize: '0.75rem' }}>{issuer}</div>
        </div>
      </div>
    </div>
  )
}

// ─── Tech expertise pill ─────────────────────────────────────────────────────
function ExpertPill({ label }) {
  return (
    <span className="badge bg-secondary-lt text-secondary px-2 py-1 fs-6">{label}</span>
  )
}

// ─── Stat summary tile ───────────────────────────────────────────────────────
function ProfileStat({ value, label }) {
  return (
    <div className="text-center px-3">
      <div className="fs-1 fw-bold text-primary lh-1">{value}</div>
      <div className="text-muted small mt-1">{label}</div>
    </div>
  )
}

// ─── Main page ───────────────────────────────────────────────────────────────
function AboutPage() {
  return (
    <PageContainer title="About" subtitle="Project background and the team behind it">

      {/* ── PROJECT OVERVIEW ─────────────────────────────────────────────────── */}
      <div className="card shadow-sm mb-4">
        <div className="card-header">
          <h3 className="card-title mb-0">
            <i className="ti ti-info-circle me-2 text-primary" />
            About This Project
          </h3>
        </div>
        <div className="card-body">
          <div className="row g-4 align-items-start">
            <div className="col-12 col-md-8">
              <p className="mb-3">
                <strong>MSEv15E2E</strong> (Microsoft Europe v15 End-to-End) is a production-ready
                demonstration of an AI-powered customer service platform built on <strong>Azure OpenAI</strong> and
                the <strong>Agent Framework</strong>. It was developed as an end-to-end reference for
                enterprise AI integration patterns.
              </p>
              <p className="text-muted mb-3">
                The system exposes a conversational REST API backed by a multi-tool AI agent that
                handles complaint management (via MCP Protocol), order operations, and email
                communications — all in a multi-tenant, containerised deployment.
              </p>
              <div className="row g-2">
                {[
                  { icon: 'ti-file-description', color: 'primary',  label: 'Complaint management via MCP server' },
                  { icon: 'ti-shopping-cart',     color: 'warning',  label: 'Order search, retrieval & modification' },
                  { icon: 'ti-mail',              color: 'cyan',     label: 'In-conversation email notifications' },
                  { icon: 'ti-bolt',              color: 'danger',   label: 'Real-time SSE streaming responses' },
                  { icon: 'ti-history',           color: 'purple',   label: 'Multi-turn session persistence' },
                  { icon: 'ti-building',          color: 'success',  label: 'Enterprise multi-tenant isolation' },
                ].map(({ icon, color, label }) => (
                  <div key={label} className="col-12 col-sm-6">
                    <div className="d-flex align-items-center gap-2">
                      <i className={`ti ${icon} text-${color}`} />
                      <span className="text-muted small">{label}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="col-12 col-md-4">
              <dl className="row mb-0">
                {[
                  { label: 'Product',    value: 'MSEv15E2E' },
                  { label: 'Version',    value: <span className="badge bg-primary-lt text-primary">v0.1.0</span> },
                  { label: 'Date',       value: 'Feb 19, 2026' },
                  { label: 'Backend',    value: 'FastAPI + Uvicorn' },
                  { label: 'AI Model',   value: 'Azure OpenAI' },
                  { label: 'Frontend',   value: 'React 18 + Vite 6' },
                  { label: 'Container',  value: 'Docker (Alpine)' },
                  { label: 'Status',     value: <span className="badge bg-success-lt text-success"><i className="ti ti-circle-check me-1" />Production Ready</span> },
                ].map(({ label, value }) => (
                  <div key={label} className="col-6 mb-2">
                    <div className="text-muted small">{label}</div>
                    <div className="fw-semibold small">{value}</div>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* ── AUTHOR PROFILE ───────────────────────────────────────────────────── */}
      <div className="card shadow-sm mb-4">
        <div className="card-header">
          <h3 className="card-title mb-0">
            <i className="ti ti-user me-2 text-warning" />
            Meet the Author
          </h3>
        </div>
        <div className="card-body">
          <div className="row g-4 align-items-start">

            {/* ── Avatar + basics ── */}
            <div className="col-12 col-md-3 text-center">
              <img
                src="https://avatars.githubusercontent.com/u/3188951?v=4"
                alt="Ramkumar JD"
                className="rounded-circle img-fluid mb-3 border border-3 border-primary"
                style={{ width: 140, height: 140, objectFit: 'cover' }}
              />
              <h3 className="fw-bold mb-1">Ramkumar JD</h3>
              <div className="text-muted small mb-2">
                <i className="ti ti-building-skyscraper me-1" />
                Executive Director
              </div>
              <div className="text-muted small mb-2">
                <a
                  href="https://www.redivac.co.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary text-decoration-none"
                >
                  REDIVAC Technologies
                </a>
              </div>
              <div className="text-muted small mb-3">
                <i className="ti ti-map-pin me-1" />
                Bangalore, India
              </div>

              {/* Social links */}
              <div className="d-flex justify-content-center gap-2 flex-wrap">
                <a
                  href="https://github.com/iomegak12"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-secondary"
                  title="GitHub"
                >
                  <i className="ti ti-brand-github" />
                </a>
                <a
                  href="https://linkedin.com/in/ramkumar-j-d-57423611"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-primary"
                  title="LinkedIn"
                >
                  <i className="ti ti-brand-linkedin" />
                </a>
                <a
                  href="mailto:jd.ramkumar@gmail.com"
                  className="btn btn-sm btn-outline-secondary"
                  title="Email"
                >
                  <i className="ti ti-mail" />
                </a>
              </div>
            </div>

            {/* ── Bio ── */}
            <div className="col-12 col-md-9">
              {/* Stats row */}
              <div className="d-flex flex-wrap justify-content-start gap-0 mb-4 border rounded-3 p-3">
                <ProfileStat value="29+" label="Years Experience" />
                <div className="vr mx-2 d-none d-sm-block" />
                <ProfileStat value="16+" label="Live Applications" />
                <div className="vr mx-2 d-none d-sm-block" />
                <ProfileStat value="343" label="GitHub Repos" />
                <div className="vr mx-2 d-none d-sm-block" />
                <ProfileStat value="500+" label="Training Programs" />
              </div>

              <p className="mb-3">
                JD Ramkumar is a distinguished technology leader with nearly <strong>29 years</strong> of
                enterprise software development experience, having worked across 16+ real-time
                international and domestic applications in various leadership and technical roles.
              </p>
              <p className="text-muted mb-3">
                As an <strong>Executive Director and AI Consultant</strong> at REDIVAC Technologies,
                he specialises in Cloud Architecture, AI/ML engineering, Big Data, and full-stack
                development. He has delivered hundreds of corporate training programs to Fortune 500
                companies including <em>Microsoft, Intel, Goldman Sachs, Wells Fargo, GE, Cisco, HP,
                IBM, and JP Morgan</em> — across India, Singapore, Hong Kong, Tokyo, and Bahrain.
              </p>
              <p className="text-muted mb-4">
                Known for his exceptional presentation skills and deep technical expertise, he
                consistently receives outstanding feedback — described by participants as{' '}
                <span className="fst-italic text-primary">
                  "setting the gold standard on technical trainings."
                </span>
              </p>

              {/* Certifications */}
              <h5 className="fw-semibold mb-3">
                <i className="ti ti-certificate me-2 text-warning" />
                Certifications
              </h5>
              <div className="row g-2 mb-4">
                <CertBadge
                  icon="ti-brand-azure"
                  color="primary"
                  title="Azure Solutions Architect Expert"
                  issuer="Microsoft"
                />
                <CertBadge
                  icon="ti-shield-lock"
                  color="danger"
                  title="Azure Security Engineer Associate"
                  issuer="Microsoft"
                />
                <CertBadge
                  icon="ti-cloud"
                  color="warning"
                  title="AWS Solutions Architect Professional"
                  issuer="Amazon Web Services"
                />
                <CertBadge
                  icon="ti-school"
                  color="success"
                  title="Microsoft Certified Trainer (MCT)"
                  issuer="Microsoft"
                />
              </div>

              {/* Tech expertise */}
              <h5 className="fw-semibold mb-3">
                <i className="ti ti-code me-2 text-cyan" />
                Technical Expertise
              </h5>
              <div className="d-flex flex-wrap gap-2">
                {[
                  'Azure', 'AWS', 'AI / ML', 'Azure OpenAI', 'Python', 'C#',
                  'React', 'FastAPI', 'Big Data', 'Microservices', 'Docker',
                  'Kubernetes', 'IoT', 'Power BI', 'Machine Learning', 'LLM Agents',
                ].map(t => <ExpertPill key={t} label={t} />)}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── PROJECT TEAM ─────────────────────────────────────────────────────── */}
      <div className="row g-4 mb-4">
        <div className="col-12 col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header">
              <h3 className="card-title mb-0">
                <i className="ti ti-users me-2 text-success" />
                Development Team
              </h3>
            </div>
            <div className="card-body">
              {[
                { name: 'Ramkumar JD',  role: 'Lead Architect & Developer', avatar: 'https://avatars.githubusercontent.com/u/3188951?v=4' },
                { name: 'Rahul',        role: 'Backend Developer' },
                { name: 'Hemanth Shah', role: 'Product Manager' },
              ].map(({ name, role, avatar }) => (
                <div key={name} className="d-flex align-items-center gap-3 mb-3">
                  {avatar ? (
                    <img
                      src={avatar}
                      alt={name}
                      className="avatar rounded-circle"
                      style={{ width: 40, height: 40, objectFit: 'cover' }}
                    />
                  ) : (
                    <span className="avatar avatar-sm bg-primary-lt rounded-circle fw-bold text-primary">
                      {name.charAt(0)}
                    </span>
                  )}
                  <div>
                    <div className="fw-semibold">{name}</div>
                    <div className="text-muted small">{role}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-12 col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header">
              <h3 className="card-title mb-0">
                <i className="ti ti-link me-2 text-cyan" />
                Project Links
              </h3>
            </div>
            <div className="card-body d-flex flex-column gap-3">
              {[
                {
                  icon: 'ti-brand-github',
                  color: 'secondary',
                  label: 'GitHub Repository',
                  desc: 'Source code and history',
                  href: 'https://github.com/iomegak12/magic-ai-practices',
                },
                {
                  icon: 'ti-building-skyscraper',
                  color: 'primary',
                  label: 'REDIVAC Technologies',
                  desc: 'Company website',
                  href: 'https://www.redivac.co.in',
                },
                {
                  icon: 'ti-brand-linkedin',
                  color: 'azure',
                  label: 'LinkedIn Profile',
                  desc: 'Ramkumar JD',
                  href: 'https://linkedin.com/in/ramkumar-j-d-57423611',
                },
              ].map(({ icon, color, label, desc, href }) => (
                <a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="d-flex align-items-center gap-3 text-decoration-none p-2 rounded-2 hover-bg"
                  style={{ transition: 'background 0.15s' }}
                >
                  <span className={`avatar avatar-sm bg-${color}-lt rounded-2 flex-shrink-0`}>
                    <i className={`ti ${icon} text-${color}`} />
                  </span>
                  <div>
                    <div className={`fw-semibold text-${color}`}>{label}</div>
                    <div className="text-muted small">{desc}</div>
                  </div>
                  <i className="ti ti-external-link text-muted ms-auto" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  )
}

export default AboutPage
