import { useChatContext } from '../../context/ChatContext';
import { ACTIONS } from '../../context/chatReducer';

export default function StreamToggle() {
  const { state, dispatch } = useChatContext();

  return (
    <button
      onClick={() => dispatch({ type: ACTIONS.TOGGLE_STREAMING })}
      className="bg-white/80 border border-gray-200/55 rounded-full px-3 py-1 text-[12px] text-text-secondary hover:text-text-primary transition-colors"
    >
      {state.streamingEnabled ? '⚡ Stream' : '📄 Instant'}
    </button>
  );
}
