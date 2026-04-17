import { useRef, useEffect } from 'react';
import { useChatContext } from '../../context/ChatContext';
import MessageBubble from './MessageBubble';
import StreamingIndicator from './StreamingIndicator';

export default function MessageList() {
  const { state } = useChatContext();
  const bottomRef = useRef(null);

  const session = state.sessions[state.activeSessionId];
  const messages = session?.messages || [];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length, state.streamingContent]);

  return (
    <div className="flex flex-col gap-4 py-4">
      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} />
      ))}

      {/* Show streaming content as a live bubble */}
      {state.isLoading && state.streamingContent && (
        <MessageBubble
          message={{ role: 'assistant', content: state.streamingContent }}
          isStreaming
        />
      )}

      {/* Loading dots when waiting for first token */}
      {state.isLoading && !state.streamingContent && <StreamingIndicator />}

      <div ref={bottomRef} />
    </div>
  );
}
