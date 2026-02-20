import env from '../../../core/config/env.js'

/**
 * Application footer.
 * Shows app name, version, and copyright.
 * Ref: FRONTEND_ARCHITECTURE.md — Layout Components
 */
function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="footer footer-transparent d-print-none">
      <div className="container-xl">
        <div className="row text-center align-items-center flex-row-reverse">

          <div className="col-12 col-lg-auto mt-3 mt-lg-0">
            <ul className="list-inline list-inline-dots mb-0">
              <li className="list-inline-item">
                <span className="text-muted">
                  {env.appName}
                </span>
              </li>
              <li className="list-inline-item">
                <span className="badge bg-primary-lt text-primary">
                  v{env.appVersion}
                </span>
              </li>
            </ul>
          </div>

          <div className="col-lg-auto me-lg-auto">
            <ul className="list-inline list-inline-dots mb-0">
              <li className="list-inline-item">
                <span className="text-muted">
                  &copy; {year} Customer Service Agent. All rights reserved.
                </span>
              </li>
            </ul>
          </div>

        </div>
      </div>
    </footer>
  )
}

export default Footer
