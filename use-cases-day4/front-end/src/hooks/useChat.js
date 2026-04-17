import { useCallback } from 'react';
import { useChatContext } from '../context/ChatContext';
import { ACTIONS } from '../context/chatReducer';
import { sendMessage } from '../api/chat';
import { useStreamingChat } from './useStreamingChat';
import { v4 as uuidv4 } from 'uuid';

export function useChat() {
  const { state, dispatch } = useChatContext();
  const { sendStreaming } = useStreamingChat();

  const send = useCallback(
    async (text) => {
      // Create a new session if none is active
      let sessionId = state.activeSessionId;
      if (!sessionId) {
        sessionId = uuidv4();
        dispatch({ type: ACTIONS.NEW_SESSION, payload: { session_id: sessionId } });
      }

      dispatch({ type: ACTIONS.ADD_USER_MESSAGE, payload: { content: text } });
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      dispatch({ type: ACTIONS.CLEAR_ERROR });

      try {
        if (state.streamingEnabled) {
          await sendStreaming({ message: text, session_id: sessionId });
        } else {
          const data = await sendMessage({ message: text, session_id: sessionId });
          dispatch({ type: ACTIONS.ADD_ASSISTANT_MESSAGE, payload: data });
        }
      } catch (err) {
        const message =
          err.message || err.error || 'Something went wrong. Please try again.';
        dispatch({ type: ACTIONS.SET_ERROR, payload: message });
      } finally {
        dispatch({ type: ACTIONS.SET_LOADING, payload: false });
      }
    },
    [state.activeSessionId, state.streamingEnabled, dispatch, sendStreaming]
  );

  return {
    send,
    sessions: state.sessions,
    activeSessionId: state.activeSessionId,
    isLoading: state.isLoading,
    streamingEnabled: state.streamingEnabled,
    streamingContent: state.streamingContent,
    error: state.error,
  };
}
