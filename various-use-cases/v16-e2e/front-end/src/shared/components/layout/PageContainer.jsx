/**
 * PageContainer — wraps page content with consistent padding and structure.
 * Accepts an optional `title` and `subtitle` for the page header.
 *
 * Usage:
 *   <PageContainer title="Support" subtitle="Chat with our AI agent">
 *     {children}
 *   </PageContainer>
 */
function PageContainer({ title, subtitle, children, fluid = false }) {
  return (
    <div className="page-body">
      <div className={fluid ? 'container-fluid' : 'container-xl'}>
        {(title || subtitle) && (
          <div className="page-header mb-3">
            <div className="row align-items-center">
              <div className="col">
                {title && <h2 className="page-title">{title}</h2>}
                {subtitle && (
                  <div className="text-muted mt-1">{subtitle}</div>
                )}
              </div>
            </div>
          </div>
        )}
        {children}
      </div>
    </div>
  )
}

export default PageContainer
