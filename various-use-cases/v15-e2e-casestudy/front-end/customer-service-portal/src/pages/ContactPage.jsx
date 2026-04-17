import { useNavigate } from 'react-router-dom'

const SUPPORT_CHANNELS = [
  {
    icon: 'ti-message-chatbot',
    color: 'bg-primary-lt',
    textColor: 'text-primary',
    title: 'Support Chat',
    badge: 'Recommended',
    badgeColor: 'bg-green',
    description: 'Get immediate AI-powered assistance for orders and complaints.',
    action: 'chat',
    actionLabel: 'Open Support Chat',
  },
  {
    icon: 'ti-mail',
    color: 'bg-blue-lt',
    textColor: 'text-blue',
    title: 'Email Support',
    description: 'Reach the development team for non-urgent technical queries.',
    action: 'email',
    actionLabel: 'support@example.com',
    actionHref: 'mailto:support@example.com',
  },
  {
    icon: 'ti-book',
    color: 'bg-green-lt',
    textColor: 'text-green',
    title: 'API Documentation',
    description: 'Browse interactive backend API docs powered by FastAPI.',
    action: 'link',
    actionLabel: 'Open API Docs ↗',
    actionHref: 'http://localhost:9080/docs',
  },
]

const ContactPage = () => {
  const navigate = useNavigate()

  return (
    <div className="container-xl">

      {/* ── Page Header ─────────────────────────────── */}
      <div className="page-header mb-4">
        <div className="row align-items-center">
          <div className="col">
            <h2 className="page-title">Contact Us</h2>
            <div className="text-muted mt-1">Get in touch with the MSAv15 team</div>
          </div>
        </div>
      </div>

      <div className="row row-cards mb-4">

        {/* ── Primary Contact ──────────────────────────── */}
        <div className="col-md-5">
          <div className="card h-100">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-address-book me-2 text-primary" />
                Contact Information
              </h3>
            </div>
            <div className="card-body">

              {/* Product Manager */}
              <div className="d-flex gap-3 align-items-start mb-4 pb-4 border-bottom">
                <span className="avatar avatar-md bg-blue-lt rounded-circle fw-bold flex-shrink-0" style={{ width: 52, height: 52, fontSize: 20 }}>
                  <span className="text-blue">RM</span>
                </span>
                <div>
                  <div className="fw-bold">Ramkumar</div>
                  <div className="text-muted small mb-2">Product Manager · MSAv15FE</div>
                  <a href="mailto:ram@example.com" className="d-flex align-items-center gap-1 small text-muted text-decoration-none">
                    <i className="ti ti-mail text-blue" />
                    ram@example.com
                  </a>
                </div>
              </div>

              {/* Development Team */}
              <div className="d-flex gap-3 align-items-start mb-4 pb-4 border-bottom">
                <span className="avatar avatar-md bg-green-lt rounded-circle fw-bold flex-shrink-0" style={{ width: 52, height: 52, fontSize: 20 }}>
                  <span className="text-green">CAP</span>
                </span>
                <div>
                  <div className="fw-bold">CAP Development Team</div>
                  <div className="text-muted small mb-2">Chandini · Ashok · Priya</div>
                  <a href="mailto:support@example.com" className="d-flex align-items-center gap-1 small text-muted text-decoration-none">
                    <i className="ti ti-mail text-green" />
                    support@example.com
                  </a>
                </div>
              </div>

              {/* Note */}
              <div className="alert alert-info mb-0">
                <div className="d-flex gap-2">
                  <i className="ti ti-info-circle flex-shrink-0 mt-1" />
                  <div className="small">
                    For immediate customer assistance, please use the{' '}
                    <button
                      className="btn btn-link p-0 small fw-semibold"
                      onClick={() => navigate('/support')}
                    >
                      Support Chat
                    </button>{' '}
                    as the primary channel.
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        {/* ── Support Channels ─────────────────────────── */}
        <div className="col-md-7">
          <div className="card h-100">
            <div className="card-header">
              <h3 className="card-title">
                <i className="ti ti-antenna me-2 text-primary" />
                Support Channels
              </h3>
            </div>
            <div className="card-body d-flex flex-column gap-3">
              {SUPPORT_CHANNELS.map((ch) => (
                <div
                  key={ch.title}
                  className="card card-sm mb-0 shadow-none border"
                >
                  <div className="card-body d-flex gap-3 align-items-center">
                    <span className={`avatar avatar-md rounded ${ch.color} flex-shrink-0`}>
                      <i className={`ti ${ch.icon} ${ch.textColor} fs-4`} />
                    </span>
                    <div className="flex-grow-1">
                      <div className="d-flex align-items-center gap-2 mb-1">
                        <span className="fw-semibold">{ch.title}</span>
                        {ch.badge && (
                          <span className={`badge ${ch.badgeColor} text-white`}>{ch.badge}</span>
                        )}
                      </div>
                      <div className="text-muted small">{ch.description}</div>
                    </div>
                    <div className="flex-shrink-0">
                      {ch.action === 'chat' ? (
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => navigate('/support')}
                        >
                          <i className="ti ti-arrow-right me-1" />
                          {ch.actionLabel}
                        </button>
                      ) : (
                        <a
                          href={ch.actionHref}
                          target={ch.action === 'link' ? '_blank' : undefined}
                          rel="noopener noreferrer"
                          className="btn btn-outline-secondary btn-sm"
                        >
                          {ch.actionLabel}
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── Feedback Notice ──────────────────────────── */}
      <div className="card bg-primary-lt border-0">
        <div className="card-body d-flex gap-3 align-items-center">
          <i className="ti ti-sparkles text-primary fs-2 flex-shrink-0" />
          <div>
            <div className="fw-bold mb-1">Have feedback or a feature request?</div>
            <div className="text-muted small">
              We&apos;re continuously improving the portal. Reach out to the team via email or
              raise it directly with Ramkumar (PM) at{' '}
              <a href="mailto:ram@example.com">ram@example.com</a>.
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}

export default ContactPage
