/**
 * Parses a raw SSE text chunk into structured events.
 * Returns an array of { type: 'text'|'metadata'|'error'|'done', data }.
 */
export function parseSSE(raw) {
  const events = [];
  const lines = raw.split('\n');
  let nextType = 'text';

  for (const line of lines) {
    if (line.startsWith('event: metadata')) {
      nextType = 'metadata';
    } else if (line.startsWith('event: error')) {
      nextType = 'error';
    } else if (line.startsWith('data: ')) {
      const data = line.slice(6);

      if (data === '[DONE]') {
        events.push({ type: 'done', data: null });
      } else if (nextType === 'metadata') {
        try {
          events.push({ type: 'metadata', data: JSON.parse(data) });
        } catch {
          events.push({ type: 'metadata', data });
        }
        nextType = 'text';
      } else if (nextType === 'error') {
        events.push({ type: 'error', data });
        nextType = 'text';
      } else {
        events.push({ type: 'text', data });
      }
    }
  }

  return events;
}
