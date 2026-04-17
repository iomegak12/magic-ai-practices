import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useChatContext } from '../../context/ChatContext';
import { ACTIONS } from '../../context/chatReducer';
import { groupChatsByDate } from '../../utils/groupChatsByDate';
import NavItem from '../sidebar/NavItem';
import ChatListGroup from '../sidebar/ChatListGroup';
import UpgradeCard from '../sidebar/UpgradeCard';

export default function Sidebar() {
  const { state, dispatch } = useChatContext();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);

  const groups = groupChatsByDate(state.sessions);

  function handleNewChat() {
    dispatch({ type: ACTIONS.SET_ACTIVE_SESSION, payload: null });
    navigate('/');
  }

  if (collapsed) {
    return (
      <aside className="glass-panel rounded-panel w-14 shrink-0 flex flex-col items-center py-4 gap-4">
        <button
          onClick={() => setCollapsed(false)}
          className="text-text-secondary hover:text-text-primary text-xl"
          aria-label="Expand sidebar"
        >
          ☰
        </button>
      </aside>
    );
  }

  return (
    <aside className="glass-panel rounded-panel w-[280px] shrink-0 flex flex-col px-6 py-7 overflow-hidden">
      {/* Logo */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-[28px] font-bold text-text-primary">
          clonescript.ai
        </h1>
        <button
          onClick={() => setCollapsed(true)}
          className="text-text-muted hover:text-text-primary md:hidden lg:hidden"
          aria-label="Collapse sidebar"
        >
          ✕
        </button>
      </div>

      {/* Nav */}
      <nav className="flex flex-col gap-0.5">
        <NavItem icon="✦" label="New Chat" onClick={handleNewChat} />
        <NavItem icon="📚" label="Library" to="/library" />
        <NavItem icon="⚙" label="Settings" to="/settings" />
        <NavItem icon="?" label="Help" />
      </nav>

      {/* Divider */}
      <div className="border-b border-[var(--color-divider)] my-4" />

      {/* Chat list */}
      <div className="flex-1 overflow-y-auto min-h-0">
        <p className="text-text-secondary text-[13px] font-medium mb-2">
          Chat List
        </p>
        {groups.map((group) => (
          <ChatListGroup key={group.label} label={group.label} sessions={group.sessions} />
        ))}
        {groups.length === 0 && (
          <p className="text-text-muted text-[13px] mt-2">No conversations yet.</p>
        )}
      </div>

      {/* Upgrade card */}
      <UpgradeCard />
    </aside>
  );
}
