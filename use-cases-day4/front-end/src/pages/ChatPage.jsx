import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useChatContext } from '../context/ChatContext';
import { ACTIONS } from '../context/chatReducer';
import Sidebar from '../components/layout/Sidebar';
import MainPanel from '../components/layout/MainPanel';

export default function ChatPage() {
  const { sessionId } = useParams();
  const { dispatch } = useChatContext();

  useEffect(() => {
    if (sessionId) {
      dispatch({ type: ACTIONS.SET_ACTIVE_SESSION, payload: sessionId });
    }
  }, [sessionId, dispatch]);

  return (
    <div className="max-w-[1200px] mx-auto my-6 px-4 h-[calc(100vh-48px)] flex gap-4">
      <Sidebar />
      <MainPanel />
    </div>
  );
}
