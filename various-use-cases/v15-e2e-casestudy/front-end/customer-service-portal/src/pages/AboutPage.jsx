const TECH_STACK = [
  { layer: 'Frontend',         value: 'React 19 + Vite 7 · Tabler Admin CDN',          icon: 'ti-brand-react',      color: 'text-cyan'   },
  { layer: 'Build Tool',       value: 'Vite 7 — ESM, code-splitting, hot reload',       icon: 'ti-bolt',             color: 'text-yellow' },
  { layer: 'Agent Framework',  value: 'Microsoft Agent Framework v15 (MAF)',            icon: 'ti-robot',            color: 'text-blue'   },
  { layer: 'AI Model',         value: 'Azure OpenAI GPT-4o · Streaming + non-streaming',icon: 'ti-brain',            color: 'text-purple' },
  { layer: 'Backend',          value: 'FastAPI · async Python · SSE responses',         icon: 'ti-server',           color: 'text-green'  },
  { layer: 'Container',        value: 'Docker + Docker Compose · msav15-network',       icon: 'ti-brand-docker',     color: 'text-blue'   },
  { layer: 'State Mgmt',       value: 'React Context API · localStorage persistence',   icon: 'ti-components',       color: 'text-orange' },
]

const CERTS = [
  { label: 'Azure Solutions Architect Expert',       color: 'bg-blue-lt text-blue'   },
  { label: 'Azure Security Engineer Associate',      color: 'bg-cyan-lt text-cyan'   },
  { label: 'AWS Certified Solutions Architect Pro',  color: 'bg-yellow-lt text-dark' },
  { label: 'Microsoft Certified Trainer (MCT)',      color: 'bg-purple-lt text-purple' },
]

const TEAM = [
  {
    name: 'Chandini',
    role: 'Frontend Developer',
    initials: 'CH',
    color: 'bg-green-lt',
    textColor: 'text-green',
    description: 'Specialises in React component architecture and Tabler UI integration.',
  },
  {
    name: 'Ashok',
    role: 'Frontend Developer',
    initials: 'AK',
    color: 'bg-purple-lt',
    textColor: 'text-purple',
    description: 'Owns API integration, SSE streaming implementation, and React Context state management.',
  },
  {
    name: 'Priya',
    role: 'Frontend Developer',
    initials: 'PR',
    color: 'bg-orange-lt',
    textColor: 'text-orange',
    description: 'Focuses on UX polish, accessibility, responsive design, and Docker deployment.',
  },
]

const AboutPage = () => {
  return (
    <div className="container-xl">

      {/* ── Page header ──────────────────────────────────────────── */}
      <div className="page-header mb-4">
        <div className="row align-items-center">
          <div className="col">
            <h2 className="page-title">About MSAv15 Service</h2>
            <div className="text-muted mt-1">
              Microsoft Agent Framework v15 · End-to-End Case Study
            </div>
          </div>
          <div className="col-auto">
            <span className="badge bg-blue text-white fs-6 px-3 py-2">
              <i className="ti ti-tag me-1" />v1.0.0
            </span>
          </div>
        </div>
      </div>

      {/* ── Project lead profile ─────────────────────────────────── */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="row align-items-start g-4">

            {/* Avatar + identity */}
            <div className="col-md-auto text-center">
              <img
                src="https://avatars.githubusercontent.com/u/3188951?v=4"
                alt="Ramkumar JD"
                className="avatar avatar-xl rounded-circle mb-2"
                style={{ width: 96, height: 96 }}
              />
              <div className="fw-bold mt-1">Ramkumar JD</div>
              <div className="text-muted small">@iomegak12</div>
              <div className="d-flex gap-2 justify-content-center mt-2 flex-wrap">
                <a
                  href="https://github.com/iomegak12"
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-sm btn-outline-secondary"
                  title="GitHub"
                >
                  <i className="ti ti-brand-github me-1" />GitHub
                </a>
                <a
                  href="https://linkedin.com/in/ramkumar-j-d-57423611"
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-sm btn-outline-secondary"
                  title="LinkedIn"
                >
                  <i className="ti ti-brand-linkedin me-1" />LinkedIn
                </a>
                <a
                  href="mailto:jd.ramkumar@gmail.com"
                  className="btn btn-sm btn-outline-secondary"
                  title="Email"
                >
                  <i className="ti ti-mail me-1" />Email
                </a>
              </div>
            </div>

            {/* Bio + org */}
            <div className="col-md">
              <div className="d-flex align-items-center gap-2 mb-1">
                <span className="badge bg-blue-lt text-blue">Executive Director</span>
                <span className="badge bg-orange-lt text-orange">AI Consultant</span>
                <span className="badge bg-purple-lt text-purple">Product Manager — MSAv15</span>
              </div>
              <h3 className="mb-1">Ramkumar JD</h3>
              <div className="text-muted mb-2">
                <i className="ti ti-building me-1" />
                <a href="https://www.redivac.co.in" target="_blank" rel="noreferrer" className="text-muted">
                  REDIVAC Technologies Private Limited
                </a>
                <span className="mx-2">·</span>
                <i className="ti ti-map-pin me-1" />Bangalore, India
              </div>

              <p className="text-muted mb-3" style={{ maxWidth: 640 }}>
                JD Ramkumar is a distinguished technology leader with nearly{' '}
                <strong>29 years of enterprise software development experience</strong>, having worked
                across 16+ real-time international and domestic applications. He holds multiple
                prestigious certifications and his technical expertise spans cloud platforms (Azure,
                AWS), AI/ML, big data analytics, containerisation, microservices, and full-stack
                development. As a corporate trainer he has delivered hundreds of programs to Fortune 500
                companies including <em>Microsoft, Intel, Goldman Sachs, Wells Fargo, GE, Cisco, IBM,
                JP Morgan</em> across India, Singapore, Hong Kong, Tokyo, and Bahrain.
              </p>

              {/* Certifications */}
              <div className="d-flex flex-wrap gap-2 mb-3">
                {CERTS.map((c) => (
                  <span key={c.label} className={`badge ${c.color} px-2 py-1`}>
                    <i className="ti ti-certificate me-1" />{c.label}
                  </span>
                ))}
              </div>

              {/* GitHub stats */}
              <div className="row g-3">
                {[
                  { icon: 'ti-book',       color: 'text-blue',   label: 'Public Repos', value: '343+' },
                  { icon: 'ti-users',      color: 'text-green',  label: 'Followers',    value: '33'   },
                  { icon: 'ti-git-commit', color: 'text-purple', label: 'Contributions (2025)', value: '254' },
                  { icon: 'ti-world',      color: 'text-orange', label: 'Website',      value: 'redivac.co.in' },
                ].map((s) => (
                  <div className="col-auto" key={s.label}>
                    <div className="d-flex align-items-center gap-1 text-muted small">
                      <i className={`ti ${s.icon} ${s.color}`} />
                      <span>{s.label}:</span>
                      <strong>{s.value}</strong>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Project overview ─────────────────────────────────────── */}
      <div className="card mb-4">
        <div className="card-header">
          <h3 className="card-title">
            <i className="ti ti-info-circle me-2 text-primary" />
            About this Project
          </h3>
        </div>
        <div className="card-body">
          <p className="mb-3">
            The <strong>MSAv15 Customer Service Portal</strong> is the front-end component of a
            comprehensive end-to-end case study demonstrating{' '}
            <strong>Microsoft Agent Framework v15</strong> capabilities. It is built as a training
            and practice project for the MAGIC AI Practices curriculum, showing how to design,
            build, and deploy an AI-powered customer service agent using modern cloud-native tools.
          </p>
          <div className="row g-3">
            {[
              { icon: 'ti-target',     color: 'text-blue',   label: 'Goal',         value: 'Demonstrate MAF v15 end-to-end with a realistic business case study'  },
              { icon: 'ti-tools',      color: 'text-green',  label: 'Use Case',     value: 'Order management & complaint handling via AI agent tool-calling'       },
              { icon: 'ti-school',     color: 'text-purple', label: 'Context',      value: 'MAGIC AI Practices training curriculum — iomegak12/magic-ai-practices' },
              { icon: 'ti-lock-open',  color: 'text-orange', label: 'Access',       value: 'No authentication (demo/training environment)'                         },
            ].map((item) => (
              <div className="col-sm-6" key={item.label}>
                <div className="d-flex gap-2 align-items-start">
                  <i className={`ti ${item.icon} mt-1 ${item.color}`} />
                  <div>
                    <div className="fw-semibold small">{item.label}</div>
                    <div className="text-muted small">{item.value}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="row row-cards mb-4">
        {/* ── Technology stack ─────────────────────────────────── */}
        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-stack me-2 text-primary" />Technology Stack
              </h3>
            </div>
            <div className="card-body p-0">
              <table className="table table-vcenter card-table">
                <tbody>
                  {TECH_STACK.map((t) => (
                    <tr key={t.layer}>
                      <td style={{ width: 32 }}>
                        <i className={`ti ${t.icon} ${t.color}`} />
                      </td>
                      <td className="text-muted small" style={{ width: 130 }}>{t.layer}</td>
                      <td className="fw-medium small">{t.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* ── Key features ─────────────────────────────────────── */}
        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-star me-2 text-primary" />Key Features
              </h3>
            </div>
            <div className="card-body">
              {[
                { icon: 'ti-message-chatbot', color: 'bg-blue-lt',   text: 'text-blue',   title: 'AI Chat Interface',   desc: 'Real-time conversation with MAF v15 agent'              },
                { icon: 'ti-bolt',            color: 'bg-yellow-lt', text: 'text-yellow', title: 'SSE Streaming',       desc: 'Word-by-word streaming via fetch() + ReadableStream'    },
                { icon: 'ti-messages',        color: 'bg-green-lt',  text: 'text-green',  title: 'Session Management',  desc: 'Multi-session support with localStorage persistence'    },
                { icon: 'ti-moon',            color: 'bg-purple-lt', text: 'text-purple', title: 'Dark / Light Theme',  desc: 'Instant theme toggle, persisted across sessions'        },
                { icon: 'ti-shield-check',    color: 'bg-red-lt',    text: 'text-red',    title: 'Error Boundaries',    desc: 'React ErrorBoundary + 422/500 error parsing + retry'    },
                { icon: 'ti-brand-docker',    color: 'bg-cyan-lt',   text: 'text-cyan',   title: 'Docker Compose',      desc: 'One command to run the full stack locally'              },
              ].map((f) => (
                <div className="d-flex gap-3 mb-3" key={f.title}>
                  <span className={`avatar avatar-sm rounded ${f.color}`}>
                    <i className={`ti ${f.icon} ${f.text}`} />
                  </span>
                  <div>
                    <div className="fw-semibold small">{f.title}</div>
                    <div className="text-muted small">{f.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── CAP development team ─────────────────────────────────── */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <i className="ti ti-users me-2 text-primary" />CAP Development Team
          </h3>
          <div className="card-options">
            <span className="badge bg-secondary-lt">MSAv15FE</span>
          </div>
        </div>
        <div className="card-body">
          <div className="row row-cards">
            {TEAM.map((member) => (
              <div className="col-sm-4" key={member.name}>
                <div className="card card-sm h-100 text-center">
                  <div className="card-body py-4">
                    <span
                      className={`avatar avatar-lg rounded-circle ${member.color} fw-bold mb-3 d-inline-flex`}
                      style={{ width: 64, height: 64, fontSize: 22 }}
                    >
                      <span className={member.textColor}>{member.initials}</span>
                    </span>
                    <div className="fw-bold">{member.name}</div>
                    <div className={`small fw-semibold ${member.textColor} mb-2`}>{member.role}</div>
                    <p className="text-muted small mb-0">{member.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  )
}

export default AboutPage
