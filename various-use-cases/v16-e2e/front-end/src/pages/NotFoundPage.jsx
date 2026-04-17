import { Link } from 'react-router-dom'
import PageContainer from '../shared/components/layout/PageContainer.jsx'

/**
 * 404 Not Found page.
 */
function NotFoundPage() {
  return (
    <PageContainer>
      <div className="container-tight py-6 text-center">
        <div className="mb-4">
          <i className="ti ti-error-404 text-muted" style={{ fontSize: '5rem' }} />
        </div>
        <h1 className="display-6 fw-bold mb-2">Page Not Found</h1>
        <p className="text-muted mb-4">
          The page you are looking for does not exist or has been moved.
        </p>
        <Link to="/" className="btn btn-primary">
          <i className="ti ti-home me-2" />
          Back to Home
        </Link>
      </div>
    </PageContainer>
  )
}

export default NotFoundPage
