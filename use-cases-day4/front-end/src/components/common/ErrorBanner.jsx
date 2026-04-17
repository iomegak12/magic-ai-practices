import { useChatContext } from '../../context/ChatContext';
import { ACTIONS } from '../../context/chatReducer';

export default function ErrorBanner() {
  const { state, dispatch } = useChatContext();

  if (!state.error) return null;

  return (
    <div className="mb-3 px-4 py-3 rounded-card bg-red-50 border border-red-200 text-red-800 text-[13px] flex items-start justify-between gap-3">
      <div>
        <p className="font-medium">Error</p>
        <p>{state.error}</p>
      </div>
      <button
        onClick={() => dispatch({ type: ACTIONS.DISMISS_ERROR })}
        className="text-red-400 hover:text-red-600 shrink-0"
        aria-label="Dismiss error"
      >
        ✕
      </button>
    </div>
  );
}
