# MAGIC-v22-MCP

**MAGIC-v22-MCP** is a Model Context Protocol (MCP) server exposing **Customer Orders & Order-specific Complaints** management via Tools, Resources, and Prompts over Streamable HTTP.

| | |
|---|---|
| **Transport** | Streamable HTTP (`/mcp`) |
| **Auth** | HS256 JWT Bearer |
| **Persistence** | SQLite (stdlib `sqlite3`) |
| **Runtime** | Python 3.12 / uv |

---

## Quickstart — uv (local)

```bash
# 1. Clone & enter the project
cd 0-mcp-servers/magic-v22-mcp

# 2. Create .env (see table below)
cp .env.example .env
# Edit .env — set JWT_SECRET at minimum

# 3. Install & run
uv sync
uv run magic-v22-mcp
```

Server starts at `http://0.0.0.0:9898/mcp`.

---

## Quickstart — Docker

```bash
cp .env.example .env   # configure JWT_SECRET
docker compose up --build
```

Data is persisted in `./data/` via a bind mount.

---

## Environment Variables

| Variable | Default | Required | Description |
|---|---|---|---|
| `JWT_SECRET` | — | ✅ | Shared secret for HS256 JWT signing/verification |
| `JWT_ALGORITHM` | `HS256` | | JWT algorithm |
| `MCP_HOST` | `0.0.0.0` | | Bind host |
| `MCP_PORT` | `9898` | | Bind port |
| `DB_PATH` | `./data/magic_v22.db` | | SQLite file path |
| `LOG_LEVEL` | `INFO` | | Python log level |

---

## MCP Surface

### 🔧 Tools (8)

| Tool | Description |
|---|---|
| `make_order` | Create a new customer order |
| `query_orders` | Search orders by customer name and/or product SKU |
| `get_order_details` | Retrieve a single order by ID |
| `register_complaint` | Register a complaint against an existing order |
| `get_complaint_details` | Retrieve a single complaint by ID |
| `search_complaints` | Search complaints with multiple optional filters |
| `resolve_complaint` | Resolve a complaint (assigns resolver team + remarks) |
| `close_complaint` | Close a resolved complaint |

### 📦 Resources (4)

| URI | Description |
|---|---|
| `stats://orders-summary` | Aggregated order statistics (total, revenue, by-status) |
| `stats://complaints-summary` | Aggregated complaint statistics |
| `catalog://{kind}` | Enum catalog — `order-statuses`, `complaint-statuses`, `complaint-priorities`, `resolver-teams` |
| `complaints://open` | All active complaints (OPEN / IN_PROGRESS / REOPENED) |

### 💬 Prompts (4)

| Prompt | Arguments | Description |
|---|---|---|
| `complaint_triage` | `order_id` | Priority + team recommendation for an order's complaints |
| `customer_order_summary` | `customer_name` | Order history summary + patterns |
| `complaint_resolution_drafter` | `complaint_id` | Draft professional resolution note |
| `escalation_decision` | `complaint_id` | Escalate / reassign / keep based on SLA age |

---

## Connecting from a FastMCP Agent (Python)

```python
from fastmcp import Client

async with Client(
    "http://localhost:9898/mcp",
    headers={"Authorization": "Bearer <YOUR_JWT>"},
) as client:
    tools = await client.list_tools()
    result = await client.call_tool("query_orders", {"customer_name": "Priya"})
```

---

## Generating a Test JWT

```python
import jwt, datetime

token = jwt.encode(
    {"sub": "test", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
    "your-jwt-secret",
    algorithm="HS256",
)
print(token)
```

---

## Project Layout

```
src/magic_v22_mcp/
├── __init__.py          # Package identity
├── __main__.py          # python -m entry point
├── auth.py              # JWTVerifier (HS256)
├── config.py            # pydantic-settings (loads .env)
├── console.py           # Rich startup banner
├── db.py                # SQLite connection + schema + ORD sequence
├── enums.py             # StrEnum domain enumerations
├── models.py            # Pydantic domain models
├── seed.py              # Idempotent demo-data seeder
├── server.py            # main() — wires everything together
├── mcp/
│   ├── tools.py         # 8 MCP tools
│   ├── resources.py     # 4 MCP resources
│   └── prompts.py       # 4 MCP prompts
├── repositories/
│   ├── orders_repo.py
│   └── complaints_repo.py
└── services/
    ├── order_service.py
    └── complaint_service.py
```
