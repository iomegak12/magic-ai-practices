const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/**
 * Non-streaming: POST /chat
 * Returns the full response JSON.
 */
export async function sendMessage({ message, session_id = null }) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.json();
}

/**
 * Streaming: POST /chat/stream
 * Returns a ReadableStream reader for SSE consumption.
 */
export async function sendMessageStream({ message, session_id = null }) {
  const res = await fetch(`${BASE_URL}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.body.getReader();
}
