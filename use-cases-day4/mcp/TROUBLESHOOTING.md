# Troubleshooting Guide

## Common Issues

### 1. Port Already in Use

**Symptom:** `OSError: [Errno 98] Address already in use` or `OSError: [WinError 10048]`

**Fix:**
- Change `SERVER_PORT` in `.env` to an available port
- Or kill the process using the port:
  ```bash
  # Linux/macOS
  lsof -ti:8700 | xargs kill -9
  # Windows
  netstat -ano | findstr :8700
  taskkill /PID <pid> /F
  ```

### 2. Database Locked

**Symptom:** `sqlite3.OperationalError: database is locked`

**Fix:**
- Ensure only one server instance is running
- Delete the `.db` file and restart (data will be re-seeded):
  ```bash
  rm orders_complaints.db
  python main.py
  ```

### 3. Seed Data Not Loading

**Symptom:** No orders or complaints after startup

**Fix:**
- Verify `SEED_ON_STARTUP=true` in `.env`
- If the database already has data, seeding is skipped. Delete the `.db` file to force re-seed.

### 4. Rate Limiting Blocking Requests

**Symptom:** HTTP 429 "Rate limit exceeded" responses

**Fix:**
- Set `RATE_LIMIT_ENABLED=false` in `.env` to disable
- Or increase `RATE_LIMIT_MAX_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS`

### 5. Module Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'fastmcp'`

**Fix:**
```bash
pip install -r requirements.txt
```

### 6. Docker Container Won't Start

**Symptom:** Container exits immediately

**Fix:**
- Check logs: `docker-compose logs mcp-server`
- Verify `.env` file exists and has valid values
- Rebuild: `docker-compose up --build`

### 7. Cannot Connect to MCP Server

**Symptom:** Connection refused from MCP client

**Fix:**
- Verify the server is running: `curl http://localhost:8700/mcp`
- Check `SERVER_HOST` is `0.0.0.0` (not `127.0.0.1`) for Docker/remote access
- Ensure firewall allows the port

### 8. Invalid Order Status / Priority Errors

**Symptom:** Tool returns `"success": false` with an invalid status message

**Fix:** Use only valid values:
- **Order statuses:** Pending, Processing, Shipped, Delivered, Cancelled, Returned
- **Complaint priorities:** Low, Medium, High, Critical
- **Complaint statuses:** Open, In Progress, Resolved, Closed, Escalated
