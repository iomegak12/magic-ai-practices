import { useState, useRef } from 'react';
import { useChat } from '../../hooks/useChat';
import StreamToggle from './StreamToggle';

export default function InputBar({ disabled }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const { send, isLoading } = useChat();

  function handleSubmit() {
    const trimmed = text.trim();
    if (!trimmed || isLoading || disabled) return;
    send(trimmed);
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleInput(e) {
    setText(e.target.value);
    // Auto-resize
    const el = e.target;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
  }

  return (
    <div className="glass-card rounded-input p-3.5 relative">
      <textarea
        ref={textareaRef}
        value={text}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        placeholder="✦ Ask Anything...."
        disabled={isLoading || disabled}
        rows={1}
        className="w-full bg-transparent outline-none resize-none text-[15px] text-text-primary placeholder:text-[var(--color-placeholder)] pr-14"
      />

      {/* Bottom row: stream toggle + send */}
      <div className="flex items-center justify-between mt-2">
        <div className="flex items-center gap-3">
          <button className="text-[12px] text-text-secondary hover:text-text-primary flex items-center gap-1">
            📎 <span>Attach</span>
          </button>
          <StreamToggle />
        </div>

        <button
          onClick={handleSubmit}
          disabled={!text.trim() || isLoading || disabled}
          className="bg-[var(--color-send-btn)] hover:bg-[var(--color-send-btn-hover)] text-white rounded-full w-10 h-10 flex items-center justify-center disabled:opacity-40 transition-colors"
          aria-label="Send message"
        >
          ↑
        </button>
      </div>
    </div>
  );
}
