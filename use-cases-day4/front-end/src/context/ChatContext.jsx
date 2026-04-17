import { createContext, useContext, useReducer, useEffect } from 'react';
import { chatReducer, initialState } from './chatReducer';

const STORAGE_KEY = 'clonescript_sessions';

const ChatContext = createContext(null);

function loadPersistedState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const sessions = JSON.parse(raw);
      return { ...initialState, sessions };
    }
  } catch {
    // Ignore corrupt data
  }
  return initialState;
}

export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, null, loadPersistedState);

  // Persist sessions to localStorage on every change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.sessions));
    } catch {
      // Storage full or unavailable — silently ignore
    }
  }, [state.sessions]);

  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const ctx = useContext(ChatContext);
  if (!ctx) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return ctx;
}
