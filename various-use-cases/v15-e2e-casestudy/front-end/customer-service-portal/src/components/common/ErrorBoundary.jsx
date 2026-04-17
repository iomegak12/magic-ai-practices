import { Component } from 'react'

/**
 * React class-based Error Boundary.
 * Catches render-time errors anywhere in the subtree and shows a fallback UI
 * instead of crashing the whole application.
 *
 * Usage:
 *   <ErrorBoundary>
 *     <YourComponent />
 *   </ErrorBoundary>
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo })
    // In production this would forward to an error tracking service
    console.error('[ErrorBoundary] Uncaught render error:', error, errorInfo)
  }

  handleReload = () => {
    window.location.reload()
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  render() {
    if (!this.state.hasError) return this.props.children

    const message =
      this.state.error?.message || 'An unexpected error occurred.'

    return (
      <div className="container-xl py-5">
        <div className="row justify-content-center">
          <div className="col-md-7">
            <div className="card border-danger">
              <div className="card-header bg-danger-lt">
                <i className="ti ti-alert-triangle me-2 text-danger" />
                <h3 className="card-title text-danger mb-0">Something went wrong</h3>
              </div>
              <div className="card-body">
                <p className="text-muted mb-3">
                  A rendering error was caught and the application has been
                  protected from crashing. You can try recovering or reloading
                  the page.
                </p>
                <div className="bg-light rounded p-3 mb-4 small text-danger font-monospace">
                  {message}
                </div>
                <div className="d-flex gap-2">
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={this.handleReset}
                  >
                    <i className="ti ti-refresh me-2" />
                    Try to recover
                  </button>
                  <button
                    type="button"
                    className="btn btn-outline-secondary"
                    onClick={this.handleReload}
                  >
                    <i className="ti ti-reload me-2" />
                    Reload page
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default ErrorBoundary
