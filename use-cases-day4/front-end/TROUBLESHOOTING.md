# Troubleshooting

## CORS Errors in Browser Console

**Symptom:** `Access to fetch has been blocked by CORS policy`

**Cause:** The browser is making requests directly to `http://localhost:8800` without the Vite proxy.

**Fix:**
- In development, ensure `VITE_API_BASE_URL` is empty or unset — the Vite proxy forwards `/chat` and `/health` to the API.
- If you set `VITE_API_BASE_URL=http://localhost:8800`, the REST API must have CORS enabled (`ENABLE_CORS=true`).

---

## API Unreachable / Network Error

**Symptom:** Health check shows "API is unreachable" or requests fail with `TypeError: Failed to fetch`.

**Fix:**
1. Ensure the REST API is running: `cd ../e2e-rest-api && python main.py`
2. Ensure the MCP server is running: `cd ../mcp && python main.py`
3. Check that port 8800 is not blocked by a firewall

---

## Blank Page After Build

**Symptom:** `npm run build` succeeds but opening `dist/index.html` shows a white page.

**Cause:** Vite builds with relative paths that require a web server.

**Fix:** Use `npm run preview` or serve via Docker/Nginx. Do not open `dist/index.html` directly in the browser (file:// protocol).

---

## Docker Container Cannot Reach REST API

**Symptom:** Chat requests fail when running in Docker.

**Cause:** `localhost` inside the container refers to the container itself, not the host.

**Fix:** The Nginx container only serves static files. API requests from the browser go directly to the API host. Ensure:
- The browser can reach `http://localhost:8800` (or the configured API URL)
- CORS is enabled on the REST API if the front-end is served from a different origin

---

## Port 3000 Already in Use

**Symptom:** `Error: listen EADDRINUSE: address already in use 0.0.0.0:3000`

**Fix:**
```bash
# Find the process
netstat -ano | findstr :3000     # Windows
lsof -i :3000                    # macOS / Linux

# Or use a different port
npm run dev -- --port 3001
```

---

## Vite HMR Not Working

**Symptom:** Changes to source files do not reflect in the browser.

**Fix:**
1. Check that the Vite dev server is running (not the Docker build)
2. Hard-refresh the browser: `Ctrl+Shift+R`
3. Clear the Vite cache: `rm -rf node_modules/.vite` then restart `npm run dev`

---

## Streaming Not Working

**Symptom:** Messages appear all at once instead of streaming token-by-token.

**Fix:**
1. Ensure the stream toggle shows "⚡ Stream" (click it to switch from Instant)
2. Verify the REST API's `/chat/stream` endpoint works: `curl -X POST http://localhost:8800/chat/stream -H "Content-Type: application/json" -d '{"message":"hello"}'`
3. Check the browser console for errors in the `useStreamingChat` hook
