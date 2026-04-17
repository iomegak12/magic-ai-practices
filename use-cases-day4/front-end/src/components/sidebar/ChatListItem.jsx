import { useNavigate } from 'react-router-dom';
import { useChatContext } from '../../context/ChatContext';
import { ACTIONS } from '../../context/chatReducer';

export default function ChatListItem({ session }) {
  const { state, dispatch } = useChatContext();
  const navigate = useNavigate();

  const isActive = state.activeSessionId === session.session_id;

  function handleClick() {
    dispatch({ type: ACTIONS.SET_ACTIVE_SESSION, payload: session.session_id });
    navigate(`/chat/${session.session_id}`);
  }

  return (
    <li>
      <button
        onClick={handleClick}
        className={`w-full text-left text-[13px] px-2 py-1.5 rounded-lg truncate transition-colors
          ${isActive
            ? 'text-text-primary bg-white/50'
            : 'text-text-secondary hover:bg-white/30'
          }`}
        title={session.title}
      >
        {session.title || 'New conversation'}
      </button>
    </li>
  );
}
