import { useChat } from '../../hooks/useChat';

export default function ExampleCard({ text, icon }) {
  const { send } = useChat();

  return (
    <button
      onClick={() => send(text)}
      className="glass-card rounded-card p-4 text-left hover:shadow-md transition-shadow flex flex-col justify-between min-h-[100px]"
    >
      <p className="text-[13px] text-text-primary">{text}</p>
      <span className="text-base mt-2 self-start">{icon}</span>
    </button>
  );
}
