import ChatListItem from './ChatListItem';

export default function ChatListGroup({ label, sessions }) {
  return (
    <div className="mb-3">
      <h3 className="text-[13px] font-bold text-text-primary mb-1">{label}</h3>
      <ul>
        {sessions.map((session) => (
          <ChatListItem key={session.session_id} session={session} />
        ))}
      </ul>
    </div>
  );
}
