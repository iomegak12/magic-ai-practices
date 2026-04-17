# Changelog

All notable changes to MSAv15Service will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-19

### Added

#### Core Features
- Initial release of MSAv15Service
- FastAPI-based REST API service
- Microsoft Agent Framework integration
- Azure OpenAI powered customer service agent

#### API Endpoints
- `POST /chat` - Conversational interface with customer service agent
  - Multi-turn conversation support via session management
  - Streaming response support using Server-Sent Events
  - Non-streaming response support (default)
- `GET /health` - Service health check with dependency verification
- `GET /` - Root endpoint with service information

#### Order Management (Native Tools)
- 6 custom Python tools integrated with order_manager library:
  1. `create_customer_order` - Create new customer orders
  2. `get_customer_orders` - Retrieve all orders for a customer
  3. `get_order_details` - Get detailed order information by ID
  4. `search_orders_by_customer_name` - Search orders by partial name match
  5. `update_order_status` - Update order status
  6. `search_orders_advanced` - Advanced multi-filter order search

#### Complaint Management (MCP Integration)
- MCP HTTP client integration for external complaint management server
- MCPStreamableHTTPTool configured for `http://localhost:8000/mcp`
- Supports all complaint operations via external server:
  - create_complaint
  - get_complaint
  - update_complaint
  - list_complaints
  - filter_complaints
  - delete_complaint

#### Session Management
- In-memory session storage for multi-turn conversations
- Automatic session creation with UUID generation
- Session expiration based on TTL (60 minutes default)
- Session cleanup functionality
- Turn count tracking per session

#### Database Features
- SQLite database integration for order storage
- Auto-seeding functionality with 25 sample orders
- Configurable seeding (enabled/disabled via environment variable)
- Sample data includes diverse Australian addresses and products
- Docker volume support for data persistence

#### Configuration Management
- Environment-based configuration using Pydantic Settings
- `.env` file support
- Comprehensive configuration options:
  - Service settings (name, version, port)
  - Azure OpenAI credentials
  - Database configuration
  - MCP server URL
  - CORS settings
  - Rate limiting options
  - Logging level

#### System Prompt
- Templated agent system prompt loaded from file
- Professional customer service representative persona
- Clear guidelines for order and complaint handling
- Modular and easy to update without code changes

#### Docker Support
- Dockerfile with Python 3.12-slim base image
- Multi-stage build optimization
- Non-root user for security
- Health check integration
- docker-compose.yml for orchestration
- Named volume for database persistence
- No version field in compose file (modern format)

#### Middleware
- CORS middleware with configurable origins
- Support for all origins by default (`*`)
- Configurable rate limiting (disabled by default)

#### Documentation
- Comprehensive README.md with quick start guide
- API usage examples (curl commands)
- Architecture diagram
- Configuration reference
- CONTRIBUTING.md with development guidelines
- CHANGELOG.md (this file)
- MIT LICENSE
- Interactive API documentation (Swagger UI)
- ReDoc alternative documentation
- OpenAPI schema generation

#### Code Organization
- Modular project structure
- Separation of concerns:
  - `main.py` outside app folder (as per specification)
  - `app/` - Application core
  - `app/tools/` - Modularized order tools
  - `app/routers/` - API endpoints
  - `app/services/` - Business logic
  - `app/prompts/` - Agent templates
- Type hints throughout codebase
- Comprehensive docstrings
- Error handling with user-friendly messages

#### Testing Infrastructure
- Test directory structure
- Example test files for health and chat endpoints
- Support for pytest and pytest-asyncio

### Technical Details

#### Dependencies
- FastAPI >= 0.109.0
- uvicorn[standard] >= 0.27.0
- pydantic >= 2.5.0
- pydantic-settings >= 2.1.0
- agent-framework (Microsoft Agent Framework)
- azure-ai-projects
- azure-identity
- sqlalchemy >= 2.0.0
- python-dotenv >= 1.0.0
- httpx >= 0.25.0
- structlog >= 24.1.0

#### Python Version
- Python 3.12+

#### External Dependencies
- Azure OpenAI (via Azure CLI authentication)
- External MCP server for complaint management
- Docker and Docker Compose (for containerized deployment)

### Architecture

#### Request Flow
```
Client → FastAPI → Session Manager → Agent Service → Tools
                                           ↓
                                    Order Manager (SQLite)
                                    MCP Server (HTTP)
```

#### Component Interaction
- FastAPI handles HTTP requests
- Session Manager maintains conversation state
- Agent Service orchestrates MAF agent
- Order Tools wrap order_manager library
- MCP Tool communicates with external server

### Performance Targets
- API Response Time: < 2s (non-streaming)
- Startup Time: < 30s
- Container Size: < 500MB
- Health Check: < 100ms
- Database Seeding: 25 records < 5s

### Security Features
- Non-root user in Docker container
- Environment-based secrets management
- No hardcoded credentials
- Azure CLI credential authentication
- CORS protection (configurable)

### Known Limitations
- Session storage is in-memory (not distributed)
- MCP server must be running externally
- Streaming implementation uses simulated chunking
- Tool usage tracking not yet implemented
- Token usage tracking not yet implemented

### Future Enhancements (Planned)
- API key authentication
- Redis for distributed session storage
- Prometheus metrics integration
- Enhanced error logging
- WebSocket support
- Load testing results
- Performance optimizations

---

## Contributors

- **Product Manager**: Ramkumar (Ram)
- **Development Team (CAP)**:
  - Chandini
  - Ashok
  - Priya

---

**Note**: This is the initial release. Future versions will follow semantic versioning.
