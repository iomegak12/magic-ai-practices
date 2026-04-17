export const ACTIONS = {
  NEW_SESSION: 'NEW_SESSION',
  SET_ACTIVE_SESSION: 'SET_ACTIVE_SESSION',
  ADD_USER_MESSAGE: 'ADD_USER_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  APPEND_STREAM_CHUNK: 'APPEND_STREAM_CHUNK',
  COMMIT_STREAM: 'COMMIT_STREAM',
  ADD_ASSISTANT_MESSAGE: 'ADD_ASSISTANT_MESSAGE',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  TOGGLE_STREAMING: 'TOGGLE_STREAMING',
  DISMISS_ERROR: 'DISMISS_ERROR',
};

export const initialState = {
  sessions: {},
  activeSessionId: null,
  isLoading: false,
  streamingEnabled: true,
  streamingContent: '',
  toolsUsed: [],
  error: null,
};

function appendMessageToSession(sessions, sessionId, message) {
  const session = sessions[sessionId] || {
    session_id: sessionId,
    title: '',
    messages: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  return {
    ...sessions,
    [sessionId]: {
      ...session,
      messages: [...session.messages, message],
      updatedAt: new Date().toISOString(),
    },
  };
}

export function chatReducer(state, action) {
  switch (action.type) {
    case ACTIONS.NEW_SESSION: {
      const { session_id } = action.payload;
      return {
        ...state,
        activeSessionId: session_id,
        sessions: {
          ...state.sessions,
          [session_id]: {
            session_id,
            title: '',
            messages: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          },
        },
      };
    }

    case ACTIONS.SET_ACTIVE_SESSION:
      return { ...state, activeSessionId: action.payload };

    case ACTIONS.ADD_USER_MESSAGE: {
      const sessionId = state.activeSessionId;
      if (!sessionId) return state;

      const userMsg = {
        role: 'user',
        content: action.payload.content,
        timestamp: new Date().toISOString(),
      };

      const updatedSessions = appendMessageToSession(state.sessions, sessionId, userMsg);

      // Auto-generate title from first user message
      const session = updatedSessions[sessionId];
      if (!session.title && session.messages.length === 1) {
        session.title = action.payload.content.slice(0, 40);
      }

      return { ...state, sessions: updatedSessions };
    }

    case ACTIONS.SET_LOADING:
      return { ...state, isLoading: action.payload };

    case ACTIONS.APPEND_STREAM_CHUNK:
      return { ...state, streamingContent: state.streamingContent + action.payload };

    case ACTIONS.COMMIT_STREAM: {
      const meta = action.payload || {};
      const finalMessage = {
        role: 'assistant',
        content: state.streamingContent,
        toolsUsed: meta.tools_used || [],
        timestamp: meta.timestamp || new Date().toISOString(),
      };

      const sessionId = meta.session_id || state.activeSessionId;
      return {
        ...state,
        activeSessionId: sessionId,
        streamingContent: '',
        toolsUsed: meta.tools_used || [],
        sessions: appendMessageToSession(state.sessions, sessionId, finalMessage),
      };
    }

    case ACTIONS.ADD_ASSISTANT_MESSAGE: {
      const { session_id, response, tools_used, timestamp } = action.payload;
      const sid = session_id || state.activeSessionId;
      const assistantMsg = {
        role: 'assistant',
        content: response,
        toolsUsed: tools_used || [],
        timestamp: timestamp || new Date().toISOString(),
      };

      return {
        ...state,
        activeSessionId: sid,
        toolsUsed: tools_used || [],
        sessions: appendMessageToSession(state.sessions, sid, assistantMsg),
      };
    }

    case ACTIONS.SET_ERROR:
      return { ...state, error: action.payload };

    case ACTIONS.CLEAR_ERROR:
    case ACTIONS.DISMISS_ERROR:
      return { ...state, error: null };

    case ACTIONS.TOGGLE_STREAMING:
      return { ...state, streamingEnabled: !state.streamingEnabled };

    default:
      return state;
  }
}
