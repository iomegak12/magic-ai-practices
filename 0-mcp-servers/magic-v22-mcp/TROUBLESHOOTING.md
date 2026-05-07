# Troubleshooting

Common issues and remedies for **MAGIC-v22-MCP**.

---

## 401 Unauthorized — bad or missing JWT

**Symptom:** Every request returns HTTP 401.

**Causes & Fixes:**

| Cause | Fix |
|---|---|
| `JWT_SECRET` in `.env` does not match the secret used to sign the token | Regenerate the token with the same secret that the server loads |
| Token has expired (`exp` claim in the past) | Issue a new token with a future `exp` |
| `Authorization` header missing or not prefixed with `Bearer ` | Use `Authorization: Bearer <token>` (note the space) |
| Algorithm mismatch (`JWT_ALGORITHM` ≠ signing algorithm) | Ensure both sides use `HS256` (or whichever algorithm is configured) |

**Quick test — generate a fresh token:**

```python
import jwt, datetime
token = jwt.encode(
    {"sub": "test", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
    "your-jwt-secret",   # must match JWT_SECRET in .env
    algorithm="HS256",
)
print(token)
```

---

## Database Locked

**Symptom:** `sqlite3.OperationalError: database is locked`

**Causes & Fixes:**

- Another process is holding a write lock. Ensure only one instance of the server runs against the same `DB_PATH`.
- In Docker, verify only one container is mounting `./data`.
- If using SQLite WAL mode manually, ensure `PRAGMA journal_mode=WAL` is consistent.

---

## Port Already in Use

**Symptom:** `[Errno 98] Address already in use` or `[WinError 10048]`

**Fix:**

```bash
# Find the process using port 9898
# Linux/macOS
lsof -i :9898
kill -9 <PID>

# Windows
netstat -ano | findstr :9898
taskkill /PID <PID> /F
```

Or change the port: set `MCP_PORT=9899` in `.env`.

---

## Docker Volume Permissions

**Symptom:** `PermissionError` when the container tries to create/write the SQLite database.

**Fix:**

```bash
# Ensure the host ./data directory is writable
mkdir -p ./data
chmod 777 ./data        # or chown to UID 1000 (the non-root user)
```

On SELinux systems add `:z` to the volume mount in `docker-compose.yml`:

```yaml
volumes:
  - ./data:/app/data:z
```

---

## FastMCP Version Mismatch

**Symptom:** `ImportError: cannot import name 'JWTVerifier' from 'fastmcp.server.auth.providers.jwt'`

**Cause:** The project requires `fastmcp >= 2.9.0`. Older versions may not expose `JWTVerifier` or the `auth=` parameter on `FastMCP`.

**Fix:**

```bash
uv sync          # respects pyproject.toml constraints
# or manually
uv add "fastmcp>=2.9.0"
```

Check installed version:

```bash
uv run python -c "import fastmcp; print(fastmcp.__version__)"
```

---

## Server Starts But Tools Return Errors

**Symptom:** Tool calls fail with `ToolError: Order not found` or similar.

**Check:**

1. The seeder ran — look for a log line `Seeding demo data …` on first start.
2. The `DB_PATH` points to a writable location. Default is `./data/magic_v22.db` relative to the working directory.
3. In Docker, the volume is correctly mounted so the database persists between restarts.
