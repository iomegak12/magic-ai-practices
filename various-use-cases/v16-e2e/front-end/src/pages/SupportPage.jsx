import { useState } from 'react'
import PageContainer from '../shared/components/layout/PageContainer.jsx'
import { ChatProvider, ChatView, SessionPanel } from '../features/chat/index.js'

/**
 * Support page — main chat interface.
 * Phase 3: ChatProvider + ChatView
 * Phase 4: SessionPanel sidebar added — responsive two-column layout
 *   • Desktop (lg+): sessions col-lg-3 + chat col-lg-9
 *   • Mobile:        collapsible sessions toggle above the chat
 * Ref: FRONTEND_ARCHITECTURE.md — Routes → SupportPage
 *      UI_COMPONENT_GUIDE.md — Session Selector layout
 */
function SupportPage() {
  const [showSessions, setShowSessions] = useState(false)

  return (
    <PageContainer title="Support" subtitle="Chat with the Customer Service Agent">
      <ChatProvider>
        {/* ── MOBILE: sessions toggle button ─────────────────────────── */}
        <div className="d-lg-none mb-2">
          <button
            type="button"
            className="btn btn-sm btn-outline-secondary d-flex align-items-center gap-2"
            onClick={() => setShowSessions(v => !v)}
          >
            <i className={`ti ${showSessions ? 'ti-chevron-up' : 'ti-layout-list'}`} />
            {showSessions ? 'Hide Sessions' : 'Show Sessions'}
          </button>
        </div>

        {/* ── MOBILE: collapsible session panel ──────────────────────── */}
        {showSessions && (
          <div className="d-lg-none mb-3" style={{ maxHeight: 340, overflow: 'hidden' }}>
            <SessionPanel />
          </div>
        )}

        {/* ── DESKTOP: two-column layout ─────────────────────────────── */}
        <div className="row g-3 align-items-start">
          {/* Sessions sidebar — always visible on lg+ */}
          <div
            className="col-lg-3 d-none d-lg-flex flex-column"
            style={{ height: 'calc(100vh - 196px)', minHeight: 480 }}
          >
            <SessionPanel />
          </div>

          {/* Chat view */}
          <div className="col-12 col-lg-9">
            <ChatView />
          </div>
        </div>
      </ChatProvider>
    </PageContainer>
  )
}

export default SupportPage
