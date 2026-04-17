# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-16

### Added
- FastMCP server with streamable HTTP transport on port 8700
- **7 MCP Tools:**
  - `get_orders_by_customer` — partial, case-insensitive order search
  - `search_orders_by_sku` — exact SKU match
  - `search_orders_by_status` — status-filtered order search
  - `get_complaints_by_order` — complaints by order ID
  - `get_complaints_by_customer` — complaints by customer name (order join)
  - `register_complaint` — create new complaint with auto-ID
  - `resolve_complaint` — resolve with mandatory resolution note
- **5 MCP Resources:**
  - `orders://summary` — order totals by status
  - `complaints://summary` — complaint totals by status & priority
  - `config://statuses` — all valid system enums
  - `orders://recent` — last 10 orders
  - `complaints://unresolved` — open/in-progress complaints
- **4 MCP Prompts:**
  - `analyze_customer_orders` — customer order analysis
  - `complaint_resolution_guide` — resolution guidance
  - `escalation_review` — high-priority complaint review
  - `order_status_inquiry` — customer-facing status summary
- SQLite database with SQLAlchemy ORM (modern `Mapped[T]` style)
- Seed script: 25 orders (Indian customers, Microsoft IT products) with 4–5 complaints each
- Per-client-IP rate limiting middleware (disabled by default, configurable via `.env`)
- Colorama startup banner with configuration and component summary
- Multi-stage Docker build with non-root user
- Docker Compose with volume persistence and health check
- Full documentation: README, TROUBLESHOOTING, CONTRIBUTING, CHANGELOG
