# Changelog

All notable changes to **MAGIC-v22-MCP** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] — 2026-05-07

### Added

- **Orders Tools** — `make_order`, `query_orders`, `get_order_details`
- **Complaints Tools** — `register_complaint`, `get_complaint_details`, `search_complaints`, `resolve_complaint`, `close_complaint`
- **Resources** — `stats://orders-summary`, `stats://complaints-summary`, `catalog://{kind}`, `complaints://open`
- **Prompts** — `complaint_triage`, `customer_order_summary`, `complaint_resolution_drafter`, `escalation_decision`
- HS256 JWT Bearer authentication via FastMCP `JWTVerifier`
- SQLite persistence with auto-incrementing `ORD#####` order numbers
- Idempotent demo-data seeder (10 orders, 5 complaints, multi-country customers)
- Rich console startup banner
- Multi-stage Docker build with non-root user
- `docker-compose.yml` with bind-mounted `./data` volume
- Full `pyproject.toml` with uv / hatchling, Python 3.12 constraint
