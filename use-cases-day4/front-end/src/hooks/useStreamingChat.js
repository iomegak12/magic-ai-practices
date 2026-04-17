import { useCallback } from 'react';
import { useChatContext } from '../context/ChatContext';
import { ACTIONS } from '../context/chatReducer';
import { sendMessageStream } from '../api/chat';

export function useStreamingChat() {
  const { dispatch } = useChatContext();

  const sendStreaming = useCallback(
    async ({ message, session_id }) => {
      let reader;
      try {
        reader = await sendMessageStream({ message, session_id });
        const decoder = new TextDecoder();
        let buffer = '';
        let isMetadataNext = false;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop(); // keep incomplete last line

          for (const line of lines) {
            if (line.startsWith('event: metadata')) {
              isMetadataNext = true;
            } else if (line.startsWith('event: error')) {
              isMetadataNext = false;
            } else if (line.startsWith('data: ')) {
              const data = line.slice(6);

              if (data === '[DONE]') {
                dispatch({ type: ACTIONS.COMMIT_STREAM });
                break;
              }

              if (isMetadataNext) {
                const meta = JSON.parse(data);
                dispatch({ type: ACTIONS.COMMIT_STREAM, payload: meta });
                isMetadataNext = false;
              } else {
                dispatch({ type: ACTIONS.APPEND_STREAM_CHUNK, payload: data });
              }
            }
          }
        }
      } catch (err) {
        dispatch({
          type: ACTIONS.SET_ERROR,
          payload: err.message || 'Stream failed',
        });
      } finally {
        reader?.cancel();
      }
    },
    [dispatch]
  );

  return { sendStreaming };
}
