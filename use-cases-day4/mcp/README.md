# Orders & Complaints MCP Server

A **FastMCP**-based Model Context Protocol server that exposes tools, resources, and prompts for managing customer eCommerce orders and their associated complaints.

## Features

| Category | Count | Description |
|----------|-------|-------------|
| **Tools** | 7 | Query orders, search complaints, register & resolve complaints |
| **Resources** | 5 | Order/complaint summaries, config enums, recent orders, unresolved complaints |
| **Prompts** | 4 | Customer analysis, resolution guide, escalation review, status inquiry |

## Tech Stack

- **FastMCP** — MCP server framework (streamable HTTP transport)
- **SQLAlchemy** — ORM with SQLite backend
- **Colorama** — Styled console output
- **python-dotenv** — Environment configuration
- **Docker** — Containerised deployment (multi-stage build)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env as needed (port, DB path, rate limiting, etc.)
```

### 3. Run the server

```bash
python main.py
```

The server starts on `http://0.0.0.0:8700/mcp` by default.

### 4. Docker

```bash
docker-compose up --build
```

## Configuration (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_NAME` | `orders-complaints-mcp-server` | Server display name |
| `SERVER_HOST` | `0.0.0.0` | Bind host |
| `SERVER_PORT` | `8700` | Bind port |
| `DB_NAME` | `orders_complaints.db` | SQLite database filename |
| `SEED_ON_STARTUP` | `true` | Auto-seed sample data on first run |
| `RATE_LIMIT_ENABLED` | `false` | Enable per-IP rate limiting |
| `RATE_LIMIT_MAX_REQUESTS` | `50` | Max requests per IP in window |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Rate limit window in seconds |

## Tools

### Order Tools (read-only)
| Tool | Description |
|------|-------------|
| `get_orders_by_customer` | Search orders by customer name (partial, case-insensitive) |
| `search_orders_by_sku` | Search orders by exact product SKU |
| `search_orders_by_status` | Search orders by status (Pending, Processing, Shipped, Delivered, Cancelled, Returned) |

### Complaint Tools
| Tool | Description |
|------|-------------|
| `get_complaints_by_order` | Get complaints for a specific order ID |
| `get_complaints_by_customer` | Get complaints by customer name (via order join) |
| `register_complaint` | Register a new complaint against an order |
| `resolve_complaint` | Resolve a complaint with a resolution note |

## Resources

| URI | Description |
|-----|-------------|
| `orders://summary` | Order totals by status |
| `complaints://summary` | Complaint totals by status & priority |
| `config://statuses` | All valid system enums |
| `orders://recent` | Last 10 orders by date |
| `complaints://unresolved` | Open / In-Progress complaints |

## Prompts

| Prompt | Description |
|--------|-------------|
| `analyze_customer_orders` | Analyse a customer's complete order history |
| `complaint_resolution_guide` | Step-by-step resolution guidance for a complaint |
| `escalation_review` | Review high-priority unresolved complaints |
| `order_status_inquiry` | Help customer understand order statuses |

## Project Structure

```
mcp/
├── main.py                  # Entry point (minimal bootstrap)
├── config/
│   └── settings.py          # Centralised configuration
├── models/
│   ├── base.py              # SQLAlchemy Base
│   ├── order.py             # Order ORM model
│   └── complaint.py         # Complaint ORM model
├── database/
│   ├── connection.py        # Engine + session manager
│   └── seed.py              # Sample data (25 orders, ~110 complaints)
├── tools/
│   ├── __init__.py          # Tool registration
│   ├── order_tools.py       # Order query implementations
│   └── complaint_tools.py   # Complaint CRUD implementations
├── resources/
│   ├── __init__.py          # Resource registration
│   └── definitions.py       # Resource implementations
├── prompts/
│   ├── __init__.py          # Prompt registration
│   └── definitions.py       # Prompt templates
├── middleware/
│   └── rate_limiter.py      # Per-IP ASGI rate limiter
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Container orchestration
└── .env.example             # Environment template
```

## Seed Data

On first run (when `SEED_ON_STARTUP=true`), the server populates the database with:
- **25 orders** — Indian customers purchasing Microsoft IT products (Surface Pro, Xbox Controller, Surface Go, etc.)
- **4–5 complaints per order** (~110 total) — varied priorities, statuses, and complaint descriptions

## License

Internal use only.
