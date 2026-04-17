import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { checkHealth } from '../services/healthService'
import { useSession } from '../context/SessionContext'
import { HEALTH_STATUS } from '../utils/constants'

const WHAT_WE_BUILD = [
  {
    icon: 'ti-robot',
    color: 'bg-blue-lt',
    iconColor: 'text-blue',
    title: 'Microsoft Agent Framework v15',
    description:
      'End-to-end case study for MAF v15 — exploring how AI agents handle customer conversations with tool-calling, session management, and streaming responses.',
  },
  {
    icon: 'ti-brand-azure',
    color: 'bg-cyan-lt',
    iconColor: 'text-cyan',
    title: 'Azure OpenAI Integration',
    description:
      'GPT-4o powers the backend agent. The frontend consumes both non-streaming (full JSON) and SSE streaming responses from a FastAPI service hosted on Azure.',
  },
  {
    icon: 'ti-stack',
    color: 'bg-purple-lt',
    iconColor: 'text-purple',
    title: 'Full-Stack Practice Project',
    description:
      'React 19 + Vite frontend with Tabler UI. FastAPI backend with MAF v15. Containerised with Docker Compose. Session state persisted to localStorage.',
  },
]

const STACK = [
  { icon: 'ti-brand-react',  color: 'text-cyan',   label: 'React 19 + Vite 7' },
  { icon: 'ti-server',       color: 'text-blue',   label: 'FastAPI + MAF v15'  },
  { icon: 'ti-brain',        color: 'text-purple', label: 'Azure OpenAI GPT-4o'},
  { icon: 'ti-brand-docker', color: 'text-blue',   label: 'Docker Compose'     },
]

const HomePage = () => {
  const navigate = useNavigate()
  const { sessions } = useSession()
  const [health, setHealth] = useState(null)
  const [loadingHealth, setLoadingHealth] = useState(true)

  useEffect(() => {
    checkHealth().then((data) => {
      setHealth(data)
      setLoadingHealth(false)
    })
  }, [])

  const isHealthy    = health?.status === HEALTH_STATUS.HEALTHY
  const isUnavailable = health?.status === HEALTH_STATUS.UNAVAILABLE

  const statusColor = loadingHealth ? 'secondary'
    : isHealthy     ? 'success'
    : isUnavailable ? 'danger'
    : 'warning'

  const statusLabel = loadingHealth ? 'Checking...'
    : isHealthy     ? 'Operational'
    : isUnavailable ? 'Unavailable'
    : 'Degraded'

  return (
    <div className="container-xl">

      {/* ── Page header ──────────────────────────────────────────── */}
      <div className="page-header mb-4">
        <div className="row align-items-center">
          <div className="col">
            <h2 className="page-title">MSAv15 — Customer Service Portal</h2>
            <div className="text-muted mt-1">
              Microsoft Agent Framework v15 · End-to-End Case Study
            </div>
          </div>
        </div>
      </div>

      {/* ── Hero ─────────────────────────────────────────────────── */}
      <div
        className="card mb-4 border-0 overflow-hidden"
        style={{ background: 'linear-gradient(135deg, #206bc4 0%, #0054a6 60%, #003d7a 100%)' }}
      >
        <div className="card-body py-5 px-5 text-white">
          <div className="row align-items-center">
            <div className="col-md-8">
              <div className="badge bg-white-lt text-white mb-3 px-3 py-2">
                <i className="ti ti-school me-2" />
                Training Practice · MAF v15
              </div>
              <h1 className="text-white fw-bold mb-3" style={{ fontSize: '1.9rem' }}>
                AI-Powered Customer Service Agent
              </h1>
              <p className="opacity-80 mb-4" style={{ maxWidth: 560 }}>
                This portal is the front-end component of the MSAv15 end-to-end case study.
                It connects to a <strong className="text-white">FastAPI + Microsoft Agent Framework v15</strong> backend
                that uses <strong className="text-white">Azure OpenAI GPT-4o</strong> to intelligently handle
                customer order queries and complaint management through natural conversation.
              </p>
              <div className="d-flex flex-wrap gap-2 mb-4">
                {STACK.map((s) => (
                  <span key={s.label} className="badge bg-white-lt px-3 py-2">
                    <i className={`ti ${s.icon} ${s.color} me-1`} />
                    {s.label}
                  </span>
                ))}
              </div>
              <button
                className="btn btn-lg btn-white text-primary fw-semibold px-5"
                onClick={() => navigate('/support')}
              >
                <i className="ti ti-message-chatbot me-2" />
                Open Support Chat
              </button>
            </div>
            <div className="col-md-4 text-center d-none d-md-block">
              <div
                className="avatar rounded-circle bg-white-lt mx-auto"
                style={{ width: 120, height: 120, fontSize: 60 }}
              >
                <i className="ti ti-headset text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Quick stats ───────────────────────────────────────────── */}
      <div className="row row-cards mb-4">
        <div className="col-sm-4">
          <div className="card">
            <div className="card-body d-flex align-items-center gap-3">
              <span className={`avatar bg-${statusColor}-lt`}>
                <i className={`ti ti-heartbeat text-${statusColor}`} />
              </span>
              <div>
                <div className="text-muted small">Backend Service</div>
                <div className="fw-bold">
                  <span className={`badge bg-${statusColor}-lt text-${statusColor}`}>
                    {statusLabel}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-sm-4">
          <div className="card">
            <div className="card-body d-flex align-items-center gap-3">
              <span className="avatar bg-blue-lt">
                <i className="ti ti-code text-blue" />
              </span>
              <div>
                <div className="text-muted small">API Version</div>
                <div className="fw-bold">
                  {loadingHealth ? '...' : health?.version && health.version !== 'unknown'
                    ? `v${health.version}` : 'N/A'}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-sm-4">
          <div className="card">
            <div className="card-body d-flex align-items-center gap-3">
              <span className="avatar bg-purple-lt">
                <i className="ti ti-messages text-purple" />
              </span>
              <div>
                <div className="text-muted small">Chat Sessions</div>
                <div className="fw-bold">{sessions.length}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── What we're building ───────────────────────────────────── */}
      <div className="row row-cards mb-4">
        {WHAT_WE_BUILD.map((f) => (
          <div className="col-md-4" key={f.title}>
            <div className="card h-100">
              <div className="card-body">
                <div className={`avatar avatar-md mb-3 rounded ${f.color}`}>
                  <i className={`ti ${f.icon} ${f.iconColor} fs-4`} />
                </div>
                <h3 className="card-title">{f.title}</h3>
                <p className="text-muted mb-0 small">{f.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Case-study architecture note ─────────────────────────── */}
      <div className="card mb-4">
        <div className="card-header">
          <h3 className="card-title">
            <i className="ti ti-topology-ring me-2 text-primary" />
            Case Study Architecture
          </h3>
        </div>
        <div className="card-body p-0">
          <table className="table table-vcenter card-table">
            <tbody>
              {[
                { layer: 'Frontend',  detail: 'React 19 + Vite · Tabler Admin CDN · React Context API · SSE streaming via fetch()',  badge: 'Port 9090', color: 'bg-cyan-lt text-cyan' },
                { layer: 'Backend',   detail: 'FastAPI · Microsoft Agent Framework v15 · Tool-calling agent (orders + complaints)',   badge: 'Port 9080', color: 'bg-blue-lt text-blue' },
                { layer: 'AI Model',  detail: 'Azure OpenAI GPT-4o · Streaming & non-streaming response modes',                      badge: 'Azure',     color: 'bg-purple-lt text-purple' },
                { layer: 'Storage',   detail: 'Session state persisted in browser localStorage · Max 10 sessions enforced',          badge: 'Local',     color: 'bg-green-lt text-green'  },
                { layer: 'Container', detail: 'Docker Compose orchestrates frontend + backend · shared msav15-network',              badge: 'Docker',    color: 'bg-orange-lt text-orange' },
              ].map((r) => (
                <tr key={r.layer}>
                  <td style={{ width: 110 }}>
                    <span className={`badge ${r.color} px-2 py-1`}>{r.layer}</span>
                  </td>
                  <td className="text-muted small">{r.detail}</td>
                  <td style={{ width: 80 }}>
                    <span className="badge bg-secondary-lt">{r.badge}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card-footer">
          <button className="btn btn-primary" onClick={() => navigate('/support')}>
            <i className="ti ti-arrow-right me-2" />
            Try the Chat Agent
          </button>
          <button
            className="btn btn-outline-secondary ms-2"
            onClick={() => navigate('/about')}
          >
            <i className="ti ti-info-circle me-2" />
            About this Project
          </button>
        </div>
      </div>

    </div>
  )
}

export default HomePage
