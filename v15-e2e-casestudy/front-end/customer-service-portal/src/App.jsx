import { BrowserRouter } from 'react-router-dom'
import { UIProvider } from './context/UIContext'
import { SessionProvider } from './context/SessionContext'
import { ChatProvider } from './context/ChatContext'
import ErrorBoundary from './components/common/ErrorBoundary'
import AppRoutes from './routes'

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <UIProvider>
          <SessionProvider>
            <ChatProvider>
              <AppRoutes />
            </ChatProvider>
          </SessionProvider>
        </UIProvider>
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
