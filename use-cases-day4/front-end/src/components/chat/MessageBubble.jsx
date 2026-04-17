import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import ToolCallBadge from './ToolCallBadge';

export default function MessageBubble({ message, isStreaming }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[75%] rounded-card px-4 py-3 ${
          isUser
            ? 'bg-[#1a1a2e] text-white'
            : 'glass-card text-text-primary'
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="prose prose-sm max-w-none prose-p:my-1 prose-headings:my-2 prose-pre:my-2 prose-ul:my-1 prose-ol:my-1">
            <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
              {message.content}
            </ReactMarkdown>
          </div>
        )}

        {/* Tool badges */}
        {!isUser && !isStreaming && message.toolsUsed?.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1.5">
            {message.toolsUsed.map((tool, i) => (
              <ToolCallBadge key={i} tool={tool} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
