# Changelog

All notable changes to the Complaint Management MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned Features
- Pagination for search results
- Complaint categories/tags
- File attachments support
- Analytics dashboard
- Email notifications

---

## [1.0.0] - 2026-02-19

### Added
- **Initial Release** 🎉
- Six MCP tools for comprehensive complaint management:
  - `register_complaint` - Register new customer complaints
  - `get_complaint` - Retrieve complaint details by ID
  - `search_complaints` - Advanced search with OR-logic filtering
  - `resolve_complaint` - Mark complaints as resolved
  - `update_complaint` - Update complaint information
  - `archive_complaint` - Soft-delete complaints
- **Database Features:**
  - SQLite database with SQLAlchemy ORM
  - Automatic table creation on startup
  - Database seeding with 20 sample complaints
  - Soft-delete archival (is_archived flag)
- **Configuration:**
  - Environment-based configuration via .env file
  - Configurable database path
  - Configurable seeding options
  - Configurable server settings (host, port, mount path)
- **Data Model:**
  - Complaint entity with 12 fields
  - Priority enum (LOW, MEDIUM, HIGH, CRITICAL)
  - Status enum (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
  - UTC timestamps for created_at, updated_at, resolution_date
- **Validation:**
  - Comprehensive input validation
  - Order number format validation (ORD-XXXXX)
  - Field length constraints
  - Business rule enforcement
- **Search Capabilities:**
  - OR-logic search across multiple fields
  - Partial text matching (case-insensitive)
  - Status filtering
  - Option to include/exclude archived complaints
- **Documentation:**
  - Complete README with usage examples
  - Contributing guidelines
  - MIT License
  - API documentation for all tools
  - Technical architecture documentation
  - Implementation plan
- **Infrastructure:**
  - FastMCP 2.10.6 integration
  - Streamable HTTP transport
  - Graceful shutdown handling (SIGINT/SIGTERM)
  - Structured logging
  - Error handling with clear error codes
- **Development:**
  - Project structure with organized modules
  - Pydantic schemas for validation
  - Faker integration for seed data generation
  - Utility modules for validators and seeding

### Technical Details
- **Python:** 3.12+
- **FastMCP:** 2.10.6
- **SQLAlchemy:** 2.0+
- **Database:** SQLite 3.x
- **Transport:** Streamable HTTP

### Known Limitations
- No pagination (all search results returned)
- No authentication or authorization
- Single-user/single-tenant only
- No complaint history tracking
- No file attachment support

---

## Development Team

**Core Developer:** Ramkumar  
**Team Members:** Chandini, Priya, Ashok

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-02-19 | Initial release with core features |

---

## Notes

For detailed technical documentation, see:
- `docs/complaint-management-mcp-spec.md` - Requirements specification
- `docs/complaint-management-technical-architecture.md` - Architecture guide
- `docs/complaint-management-implementation-plan.md` - Implementation roadmap

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security improvements
