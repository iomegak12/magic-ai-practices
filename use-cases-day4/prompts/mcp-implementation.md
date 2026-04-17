# Plan: MCP Server — Customer Orders & Complaints

Build a FastMCP server at `use-cases-day4/mcp/` with 7 tools, recommended resources & prompts, SQLite storage, streamable HTTP on port 8700, per-IP rate limiting, colorama banner, Docker multi-stage build, and full documentation.

---

## Recommended Enums

| Category | Values | Default |
|---|---|---|
| **Order Statuses** | Pending, Processing, Shipped, Delivered, Cancelled, Returned | — |
| **Complaint Priorities** | Low, Medium, High, Critical | **Medium** |
| **Complaint Statuses** | Open, In Progress, Resolved, Closed, Escalated | **Open** |

---

## Project Structure

```
use-cases-day4/mcp/
├── main.py                         # Minimal bootstrap
├── requirements.txt
├── .env / .env.example
├── .gitignore / .dockerignore
├── Dockerfile                      # Multi-stage build
├── docker-compose.yml              # iomega/magic-training-mcp
├── README.md / TROUBLESHOOTING.md / CHANGELOG.md / CONTRIBUTING.md
├── config/
│   ├── __init__.py
│   └── settings.py                 # Config + enums + .env loading
├── database/
│   ├── __init__.py
│   ├── connection.py               # Engine + session context manager
│   └── seed.py                     # 25 orders + ~100-125 complaints
├── models/
│   ├── __init__.py
│   ├── order.py                    # Order ORM (Mapped[T] style)
│   └── complaint.py                # Complaint ORM (Mapped[T] style)
├── tools/
│   ├── __init__.py                 # register_tools(mcp)
│   ├── order_tools.py              # 3 tools
│   └── complaint_tools.py          # 4 tools
├── resources/
│   ├── __init__.py                 # register_resources(mcp)
│   └── definitions.py
├── prompts/
│   ├── __init__.py                 # register_prompts(mcp)
│   └── definitions.py
└── middleware/
    ├── __init__.py
    └── rate_limiter.py             # Per-IP ASGI middleware
```

---

## Steps

### Phase 1 — Foundation (config, models, database)

1. **`config/settings.py`** — `Settings` class with .env loading
   - SERVER_NAME, SERVER_HOST, SERVER_PORT=8700
   - DB_NAME=orders_complaints.db
   - RATE_LIMIT_ENABLED=False, RATE_LIMIT_MAX_REQUESTS=50, RATE_LIMIT_WINDOW_SECONDS=60
   - SEED_ON_STARTUP=True
   - Enum lists: VALID_ORDER_STATUSES, VALID_COMPLAINT_PRIORITIES, VALID_COMPLAINT_STATUSES

2. **`models/order.py`** — Order ORM with auto-gen IDs (ORD10001+), `to_dict()`
   - Fields: order_id (PK), order_date, customer_name, product_sku, billing_address, quantity, unit_price, order_status, remarks

3. **`models/complaint.py`** — Complaint ORM with FK to orders, auto-gen IDs (COMP10001+), `to_dict()`
   - Fields: complaint_id (PK), complaint_reg_date, order_id (FK), complaint_description, priority (default "Medium"), assigned_to (default "Unassigned"), complaint_status (default "Open"), resolution_note (nullable)

4. **`database/connection.py`** — SQLAlchemy engine + `get_session()` context manager + `init_db()`

5. **`database/seed.py`** — 25 orders (Indian customers, Microsoft IT products like Surface Pro, Xbox Controller, MS Keyboard, Surface Go, etc.), 4-5 complaints per order (~100-125 total), varied statuses/priorities

### Phase 2 — Tools (7 tools with structured response format)

All tools return: `{"operation": "...", "success": bool, "message"/"error": "...", "result": ..., "count": N}`

6. **Order tools** (`tools/order_tools.py`):
   - `get_orders_by_customer(customer_name)` — partial match, case-insensitive (SQL LIKE `%name%` + LOWER)
   - `search_orders_by_sku(product_sku)` — exact match
   - `search_orders_by_status(order_status)` — validated against allowed statuses

7. **Complaint tools** (`tools/complaint_tools.py`):
   - `get_complaints_by_order(order_id)` — exact match on order_id
   - `get_complaints_by_customer(customer_name)` — join with orders, partial/case-insensitive match
   - `register_complaint(order_id, complaint_description, priority?)` — validates order exists, auto-generates COMP ID, defaults priority=Medium, status=Open, assigned_to=Unassigned
   - `resolve_complaint(complaint_id, resolution_note)` — validates complaint exists & not already resolved, sets status=Resolved + stores resolution_note

8. **`tools/__init__.py`** — `register_tools(mcp)` imports and decorates all 7 tools

### Phase 3 — Resources (5 recommended)

9. **`resources/definitions.py`**:
   - `orders://summary` — total orders + breakdown by status
   - `complaints://summary` — total complaints + breakdown by status & priority
   - `config://statuses` — all valid enums (order statuses, complaint priorities, complaint statuses)
   - `orders://recent` — last 10 orders by date
   - `complaints://unresolved` — all open/in-progress complaints

10. **`resources/__init__.py`** — `register_resources(mcp)`

### Phase 4 — Prompts (4 recommended)

11. **`prompts/definitions.py`**:
    - `analyze_customer_orders(customer_name)` — "Analyze all orders for {customer_name}, summarize order history, highlight any issues..."
    - `complaint_resolution_guide(complaint_id)` — "Review complaint {complaint_id}, suggest resolution steps..."
    - `escalation_review()` — "Review all high-priority and critical unresolved complaints, recommend escalation actions..."
    - `order_status_inquiry(customer_name)` — "Help customer {customer_name} understand their current order statuses..."

12. **`prompts/__init__.py`** — `register_prompts(mcp)`

### Phase 5 — Middleware & Bootstrap

13. **`middleware/rate_limiter.py`** — custom ASGI middleware
    - In-memory per-IP tracking with TTL window
    - Returns HTTP 429 when limit exceeded (with Retry-After header)
    - Completely bypassed when RATE_LIMIT_ENABLED=False

14. **`main.py`** — minimal bootstrap:
    - Import FastMCP, colorama, settings
    - Display colorama startup banner (server name, port, DB path, rate-limit status)
    - Create `FastMCP` instance
    - Call `register_tools(mcp)`, `register_resources(mcp)`, `register_prompts(mcp)`
    - Init DB + conditional seed
    - `mcp.run(transport="http", host=..., port=...)`

### Phase 6 — Environment & Docker

15. **`.env`** and **`.env.example`** — all configurable settings with defaults

16. **`Dockerfile`** — multi-stage:
    - Stage 1 (builder): `python:3.12-slim`, install deps into venv
    - Stage 2 (runtime): `python:3.12-slim`, copy venv + app, non-root user, expose 8700

17. **`docker-compose.yml`** — image `iomega/magic-training-mcp`, env_file, volume for DB persistence, port 8700

18. **`.dockerignore`** — exclude .git, __pycache__, .env, *.db, .venv, etc.

19. **`.gitignore`** — Python standard + .env, *.db, etc.

### Phase 7 — Documentation

20. **`README.md`** — project overview, setup, usage, tool/resource/prompt inventory, Docker instructions

21. **`TROUBLESHOOTING.md`** — common issues (port conflicts, DB locks, rate limiting, Docker)

22. **`CHANGELOG.md`** — initial v1.0.0 entry

23. **`CONTRIBUTING.md`** — dev setup, code style, PR guidelines

24. **`requirements.txt`** — fastmcp, sqlalchemy, python-dotenv, colorama, uvicorn

---

## Decisions

- **No create_order tool** — orders come from seed data only
- **SQLite** stored at project root (`orders_complaints.db`), path configurable via .env
- **Modern SQLAlchemy** (`Mapped[T]`, `mapped_column()`) — consistent with existing workspace patterns
- **`resolution_note`** added to complaint model — populated only when resolving
- **Auto-ID generation**: query max existing ID, increment (ORD10001+, COMP10001+)
- **Structured response format**: `{"operation", "success", "message"/"error", "result", "count"}`
- **Rate limiter**: custom in-memory ASGI middleware (no external dependency), disabled by default
- **Read-only tools** annotated with `readOnlyHint=True` for better client UX

---

## Reference Patterns (from existing workspace)

- `v15-e2e-casestudy/mcp-servers/main.py` — colorama banner, tool registration, signal handling
- `v15-e2e-casestudy/mcp-servers/complaint_manager/config.py` — Config class with validation lists
- `v15-e2e-casestudy/mcp-servers/complaint_manager/database.py` — session context manager
- `v15-e2e-casestudy/mcp-servers/complaint_manager/tools.py` — structured response dict format
- `customers_complaints/models.py` — modern `Mapped[T]` ORM with relationships
- `customers_complaints/seed.py` — Indian names + IT product seed data

---

## Verification

1. `python main.py` — colorama banner displayed, server listening on port 8700
2. Test all 7 tools via MCP client at `http://localhost:8700/mcp`
3. Test resources: `orders://summary`, `complaints://summary`, `config://statuses`
4. Rate limiting: enable in .env, send 51 rapid requests → verify 429 on 51st
5. `docker-compose up --build` → container starts, tools accessible

---

## Further Considerations

1. **`assign_complaint` tool** — assign a complaint to a support executive? *Recommend adding*
2. **Pagination** — search tools support `limit`/`offset`? *Recommend yes, default limit=50*
3. **MCP annotations** — read-only tools get `readOnlyHint=True` for better client UX
