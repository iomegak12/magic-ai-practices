# Plan: MAGIC-v22-MCP — Orders & Complaints FastMCP Server

Build a FastMCP server (`MAGIC-v22-MCP`) exposing Customer Orders & Order-specific Complaints management as Tools, Resources, and Prompts. Streamable HTTP on `0.0.0.0:9898/mcp` with HS256 JWT bearer auth. SQLite persistence via SQLAlchemy-free lightweight layer (sqlite3 stdlib + dataclasses), seeded with realistic multi-country names. uv-managed Python 3.12 env, multi-stage slim Dockerfile, docker-compose with `./data` volume. Modular `src/magic_v22_mcp/` layout. Colorful Rich startup banner.

## Decisions (locked from MCQ answers)

- **Location**: `0-mcp-servers/magic-v22-mcp/`
- **Storage**: SQLite (file `./data/magic_v22.db`), accessed via stdlib `sqlite3` + dataclass models (no ORM)
- **Seed**: auto-seed ~10 orders + 5 complaints if DB empty; mix of US / Canada / Australia / India full names
- **order_number**: caller may supply; if omitted, server auto-generates next sequential `ORDxxxxx` (starts at `ORD10001`); validation: regex `^ORD\d{5,}$`, unique
- **Order statuses**: `PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED`
- **Complaint priorities**: `LOW, MEDIUM, HIGH, CRITICAL`
- **Complaint statuses**: `OPEN, IN_PROGRESS, RESOLVED, CLOSED, REOPENED, CANCELLED`
- **Resolver teams**: `CUSTOMER_SUPPORT, ORDER_FULFILLMENT, LOGISTICS, BILLING, RETURNS_AND_REFUNDS, QUALITY_ASSURANCE, TECHNICAL_SUPPORT`
- **resolve vs close**: `resolve_complaint` sets RESOLVED (requires `resolved_by` team + `resolution_remarks`); `close_complaint` only allowed from RESOLVED → CLOSED
- **Auth**: HS256 JWT, secret from `.env` `JWT_SECRET`; verify signature + `exp`. No issuer/audience checks. No token-mint helper.
- **Endpoint path**: `/mcp` (FastMCP default for streamable HTTP)
- **Resources** (4): `stats://orders-summary`, `stats://complaints-summary`, `catalog://{kind}` (order-statuses, complaint-statuses, complaint-priorities, resolver-teams — single template), `complaints://open`
- **Prompts** (4): `complaint_triage`, `customer_order_summary`, `complaint_resolution_drafter`, `escalation_decision`
- **Docker compose**: single `mcp` service, volume mounts `./data` for SQLite
- **Layout**: src-layout (`src/magic_v22_mcp/...`)
- **Tests**: none for this iteration
- **Console**: `rich` (Panel + Table)
- **No order updates** of any kind (immutable once created)

## Steps

### Phase 1 — Project scaffolding
1. Create `0-mcp-servers/magic-v22-mcp/` with src-layout skeleton.
2. `pyproject.toml` (uv-compatible, Python 3.12) with deps: `fastmcp`, `pyjwt[crypto]`, `python-dotenv`, `rich`, `pydantic`. No SQLAlchemy.
3. `.python-version` → `3.12`.
4. Standard files: `.gitignore` (Python + venv + .env + data/ + __pycache__), `.dockerignore`, `LICENSE` (MIT, holder = Ramkumar), `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md` (Keep-a-Changelog format, v0.1.0 entry), `TROUBLESHOOTING.md`.
5. `.env.example` with `JWT_SECRET`, `JWT_ALGORITHM=HS256`, `MCP_HOST=0.0.0.0`, `MCP_PORT=9898`, `DB_PATH=./data/magic_v22.db`, `LOG_LEVEL=INFO`.

### Phase 2 — Domain & persistence (`src/magic_v22_mcp/`)
6. `enums.py` — `OrderStatus`, `ComplaintPriority`, `ComplaintStatus`, `ResolverTeam` (str Enums).
7. `models.py` — Pydantic models `Order`, `Complaint` matching exact field list from requirements (no extra fields). Field-level validation for `order_number` regex, `units > 0`, `order_amount >= 0`.
8. `db.py` — sqlite3 connection helper (`get_conn()`), schema bootstrap (`init_db()`) with `orders` + `complaints` tables (FK `complaints.order_id → orders.order_id`), and a `_meta` table for next ORD sequence.
9. `seed.py` — idempotent seeder (only runs when both tables empty); ~10 orders w/ diverse names (US/Canada/Australia/India), ~5 complaints across priorities/statuses.
10. `repositories/orders_repo.py` — `insert_order`, `get_by_id`, `search(customer_substr, sku_substr)`, `next_order_number()`, `exists_order_number()`.
11. `repositories/complaints_repo.py` — `insert_complaint`, `get_by_id`, `search(filters: order_id?, customer_substr?, registered_by?, priority?, status?, resolved_by?, description_substr?)`, `update_status_resolve`, `update_status_close`. All text searches use `LIKE` with `LOWER()` for case-insensitive partial match.

### Phase 3 — Services (business logic)
12. `services/order_service.py` — wraps repo, encapsulates: `make_order` (auto-generate ORDxxxxx if not given, default status PENDING), `query_orders`, `get_order_details`. Raises domain errors on invalid state.
13. `services/complaint_service.py` — `register_complaint` (validates linked order exists, default OPEN, no `resolved_by`/`resolution_remarks` yet), `get_complaint_details`, `search_complaints`, `resolve_complaint` (requires team enum + remarks; only from OPEN/IN_PROGRESS/REOPENED), `close_complaint` (only from RESOLVED). All transitions enforced here, not in repos.

### Phase 4 — MCP surface
14. `mcp/tools.py` — register all 8 tools with proper type hints + `Annotated[..., Field(description=...)]`:
    - `make_order(customer_name, product_sku, units, order_amount, remarks, order_number?)`
    - `query_orders(customer_name?, product_sku?)` (partial-match)
    - `get_order_details(order_id)`
    - `register_complaint(order_id, registered_by, complaint_description, priority)`
    - `get_complaint_details(complaint_id)`
    - `search_complaints(...all filters optional...)`
    - `resolve_complaint(complaint_id, resolved_by_team, resolution_remarks)`
    - `close_complaint(complaint_id)`
    - Read-only operations get `annotations={"readOnlyHint": True}`. Use `ToolError` for domain errors so messages reach the LLM cleanly.
15. `mcp/resources.py`:
    - `stats://orders-summary` → JSON: total, by_status, total_revenue
    - `stats://complaints-summary` → JSON: total, by_status, by_priority, by_resolver_team
    - `catalog://{kind}` template (RFC 6570 single-segment param) — returns enum values for one of the 4 catalog kinds; unknown kind raises `ResourceError`
    - `complaints://open` → JSON list of OPEN+IN_PROGRESS+REOPENED complaints
16. `mcp/prompts.py` — 4 prompts. Each fetches relevant context from services and returns either a `str` (single user msg) or `list[Message]`:
    - `complaint_triage(order_id)` — given order context, ask LLM to recommend priority + likely resolver team
    - `customer_order_summary(customer_name)` — summarize order history (uses partial-match query)
    - `complaint_resolution_drafter(complaint_id)` — drafts a resolution note in the voice of the resolver team
    - `escalation_decision(complaint_id)` — analyzes complaint + age + priority and recommends escalate/reassign/keep

### Phase 5 — Server, auth, console
17. `config.py` — Pydantic `Settings` loaded from `.env` (host, port, db_path, jwt_secret, jwt_algorithm, log_level, server_name="MAGIC-v22-MCP", description="Magic v22 - Orders and Complaints Services", version from `__about__`).
18. `auth.py` — implement a FastMCP `TokenVerifier` (or compatible) that decodes the bearer JWT with HS256 + secret, validates `exp`, returns the verified token; reject otherwise. Wire as `auth=` on `FastMCP(...)`.
19. `console.py` — `print_startup_banner(settings)` using `rich`: Panel header (server name + description + version), Table with key/value rows for transport, host:port, MCP path, auth scheme, DB path, log level, list of registered tools/resources/prompts, sample curl/connect snippet.
20. `server.py` — minimal entry point: load settings, init DB, run seed, build `FastMCP(name=..., instructions=..., auth=...)`, register tools/resources/prompts via the `mcp/` modules, print banner, then `mcp.run(transport="http", host=..., port=..., path="/mcp")`. Configure stdlib `logging` to console only (no JSON, no file) at `LOG_LEVEL`.
21. `__main__.py` — `python -m magic_v22_mcp` → calls `server.main()`.

### Phase 6 — Containerization
22. `Dockerfile` — multi-stage:
    - **Stage 1 (builder)**: `python:3.12-slim` + install `uv`; copy `pyproject.toml` + lockfile; `uv sync --frozen --no-dev` into `/app/.venv`.
    - **Stage 2 (runtime)**: `python:3.12-slim`; copy `/app/.venv` and `src/`; non-root user; `EXPOSE 9898`; CMD runs `python -m magic_v22_mcp`. **No HEALTHCHECK** (per requirement).
23. `.dockerignore` — exclude `.venv`, `data/`, `*.db`, `__pycache__`, `.git`, `.env`, IDE files.
24. `docker-compose.yml` — single `mcp` service: build context `.`, ports `9898:9898`, `env_file: .env`, volume `./data:/app/data`, `restart: unless-stopped`.

### Phase 7 — Docs
25. `README.md` — overview, requirements, quickstart (uv local + docker), env vars table, tools/resources/prompts catalog, sample MAF agent connection snippet.
26. `CONTRIBUTING.md` — branch flow, uv commands, code style, PR checklist.
27. `CHANGELOG.md` — `## [0.1.0] - 2026-05-07` Added section with all features.
28. `TROUBLESHOOTING.md` — common issues: 401 (bad/expired JWT), DB locked, port in use, container can't write to `/app/data`, FastMCP version mismatch.

## Relevant files

- `0-mcp-servers/magic-v22-mcp/pyproject.toml` — uv project metadata + deps
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/server.py` — entry: builds FastMCP, registers components, prints banner, `mcp.run(transport="http", ...)`
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/config.py` — Settings from `.env`
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/auth.py` — HS256 JWT TokenVerifier
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/console.py` — Rich banner
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/enums.py` — 4 enum classes
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/models.py` — Pydantic Order / Complaint models
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/db.py` — sqlite3 conn + schema init
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/seed.py` — idempotent seeder
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/repositories/orders_repo.py`, `complaints_repo.py`
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/services/order_service.py`, `complaint_service.py`
- `0-mcp-servers/magic-v22-mcp/src/magic_v22_mcp/mcp/tools.py`, `resources.py`, `prompts.py`
- `0-mcp-servers/magic-v22-mcp/Dockerfile`, `docker-compose.yml`, `.dockerignore`
- `0-mcp-servers/magic-v22-mcp/.env.example`, `.gitignore`, `LICENSE`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `TROUBLESHOOTING.md`

## Verification

1. `uv sync` succeeds; `uv run python -m magic_v22_mcp` boots, prints the Rich banner, listens on `0.0.0.0:9898`.
2. Without `Authorization: Bearer <jwt>` → 401; with valid HS256 token signed by `JWT_SECRET` → MCP handshake succeeds.
3. From a FastMCP `Client` (or curl `tools/list` over streamable HTTP) confirm: 8 tools, 4 resources (one is a template), 4 prompts visible.
4. End-to-end happy path: `make_order` → returned order_id; `register_complaint` against it; `resolve_complaint` then `close_complaint`; `search_complaints` with partial description match returns it.
5. Negative tests (manual): `close_complaint` from OPEN → ToolError; duplicate `order_number` → ToolError; unknown `catalog://xyz` → ResourceError.
6. `docker compose up --build` produces a running container; SQLite file appears in `./data/magic_v22.db`; same handshake works on host port 9898.
7. After restart, seeded data persists (because `./data` is volume-mounted).
8. Connect from a Microsoft Agent Framework notebook (e.g., pattern from `maf-202/202-4-mcp-use-1.ipynb`) using streamable HTTP + bearer header to confirm interoperability.

## Scope boundaries

- **Included**: 8 tools, 4 resources, 4 prompts, JWT auth, SQLite persistence, seed, Docker + compose, docs.
- **Excluded**: order updates of any kind, customer entity (customer is just a name string), pagination, rate limiting, tests, CI workflows, OpenTelemetry/observability, refresh tokens, RBAC/scopes, multi-tenancy.
