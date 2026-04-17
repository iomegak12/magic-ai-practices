import PageContainer from '../shared/components/layout/PageContainer.jsx'

/**
 * Contact page — contact form stub.
 * Phase 1 stub.
 */
function ContactPage() {
  return (
    <PageContainer title="Contact" subtitle="Get in touch with our team">
      <div className="row justify-content-center">
        <div className="col-12 col-md-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Send a Message</h3>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label" htmlFor="contact-name">Name</label>
                <input
                  id="contact-name"
                  type="text"
                  className="form-control"
                  placeholder="Your name"
                />
              </div>
              <div className="mb-3">
                <label className="form-label" htmlFor="contact-email">Email</label>
                <input
                  id="contact-email"
                  type="email"
                  className="form-control"
                  placeholder="your@email.com"
                />
              </div>
              <div className="mb-3">
                <label className="form-label" htmlFor="contact-message">Message</label>
                <textarea
                  id="contact-message"
                  className="form-control"
                  rows={4}
                  placeholder="How can we help you?"
                />
              </div>
              <button type="button" className="btn btn-primary w-100">
                <i className="ti ti-send me-2" />
                Send Message
              </button>
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  )
}

export default ContactPage
