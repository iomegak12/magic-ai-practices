import { useState, useEffect, useRef } from 'react';
import { checkReadiness } from '../api/health';

export function useHealthCheck() {
  const [ready, setReady] = useState(false);
  const [status, setStatus] = useState('checking');
  const [checks, setChecks] = useState(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    let cancelled = false;

    async function poll() {
      try {
        const data = await checkReadiness();
        if (cancelled) return;
        setReady(data.ready);
        setStatus(data.status);
        setChecks(data.checks || null);

        if (data.ready && intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      } catch {
        if (!cancelled) {
          setReady(false);
          setStatus('unreachable');
        }
      }
    }

    poll();
    intervalRef.current = setInterval(poll, 5000);

    return () => {
      cancelled = true;
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return { ready, status, checks };
}
