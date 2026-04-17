# Troubleshooting

## MCP Server Connection Failed

**Symptom:** Agent returns errors when querying orders or complaints.

**Cause:** The Orders & Complaints MCP server is not running on port 8700.

**Fix:**
```bash
cd use-cases-day4/mcp
python main.py
```

Verify with:
```bash
curl http://localhost:8700/mcp
```

---

## Azure Authentication Errors

**Symptom:** `401 Unauthorized` or `DefaultAzureCredentialError` on startup.

### Using `AZURE_AUTH_METHOD=cli`
Ensure you are logged in:
```bash
az login
az account show
```

### Using `AZURE_AUTH_METHOD=api_key`
Verify `AZURE_OPENAI_API_KEY` is set correctly in `.env`.

---

## Port 8800 Already in Use

**Symptom:** `OSError: [Errno 98] Address already in use`

**Fix:** Either stop the process using port 8800 or change `SERVER_PORT` in `.env`:
```bash
# Find the process
netstat -ano | findstr :8800     # Windows
lsof -i :8800                    # macOS / Linux

# Or change the port
SERVER_PORT=8801
```

---

## Rate Limiting Unexpectedly Blocking Requests

**Symptom:** 429 responses even with low traffic.

**Fix:** Rate limiting is disabled by default. Check `.env`:
```
ENABLE_RATE_LIMITING=false
```

If enabled, adjust the limit:
```
RATE_LIMIT_PER_MINUTE=120
```

---

## Docker Container Cannot Reach MCP Server

**Symptom:** MCP tool calls fail inside Docker.

**Cause:** `localhost:8700` inside the container refers to the container itself, not the host.

**Fix:** Use the host network address:
```
MCP_ORDERS_URL=http://host.docker.internal:8700/mcp
```

Or run both services in the same Docker network.

---

## SQLite Database Locked

**Symptom:** `sqlite3.OperationalError: database is locked`

**Cause:** Multiple processes accessing the same database file.

**Fix:** Ensure only one instance of the API is running, or use separate `DB_PATH` values for each instance.

---

## Guardrail Classification Errors

**Symptom:** Messages pass through without classification (logs show "Classification error").

**Cause:** The guardrail classifier uses `AZURE_OPENAI_API_KEY` regardless of `AZURE_AUTH_METHOD`. If the key is missing or invalid, guardrails fail open.

**Fix:** Ensure `AZURE_OPENAI_API_KEY` is set in `.env` even when using `AZURE_AUTH_METHOD=cli`.

---

## OpenTelemetry / Jaeger Not Receiving Traces

**Symptom:** No traces appear in Jaeger UI.

**Fix:**
1. Ensure `ENABLE_OBSERVABILITY=true` in `.env`
2. Start Jaeger:
   ```bash
   docker run -d --name jaeger \
     -e COLLECTOR_OTLP_ENABLED=true \
     -p 16686:16686 -p 4317:4317 -p 4318:4318 \
     jaegertracing/all-in-one:latest
   ```
3. Verify `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`
