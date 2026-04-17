import { useChatContext } from '../../context/ChatContext';
import { useHealthCheck } from '../../hooks/useHealthCheck';
import WelcomeScreen from '../chat/WelcomeScreen';
import MessageList from '../chat/MessageList';
import InputBar from '../input/InputBar';
import ActionBar from '../input/ActionBar';
import Avatar from '../common/Avatar';
import ErrorBanner from '../common/ErrorBanner';

export default function MainPanel() {
  const { state } = useChatContext();
  const { ready, status } = useHealthCheck();

  const activeSession = state.activeSessionId
    ? state.sessions[state.activeSessionId]
    : null;

  const hasMessages = activeSession && activeSession.messages.length > 0;

  return (
    <main className="glass-panel rounded-panel flex-1 flex flex-col p-6 overflow-hidden relative">
      {/* Header */}
      <div className="absolute top-4 right-4 z-10">
        <Avatar />
      </div>

      {/* Health banner */}
      {!ready && (
        <div className="mb-3 px-4 py-2 rounded-card text-[13px] bg-amber-50 border border-amber-200 text-amber-800">
          {status === 'unreachable'
            ? 'API is unreachable. Check that the server is running on port 8800.'
            : 'Service is starting up. Please wait…'}
        </div>
      )}

      {/* Error banner */}
      {state.error && <ErrorBanner />}

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto min-h-0">
        {hasMessages ? <MessageList /> : <WelcomeScreen />}
      </div>

      {/* Input */}
      <div className="mt-4">
        <InputBar disabled={!ready} />
        {!hasMessages && <ActionBar />}
      </div>

      {/* Bottom branding */}
      <p className="text-[12px] text-text-muted text-right mt-2">
        clonescript.ai
      </p>
    </main>
  );
}
