# MSAv15Service - Customer Service Agent REST API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)

REST API service exposing an AI-powered customer service agent capable of handling order management and complaint management through conversational interactions, built with Microsoft Agent Framework.

## 🎯 Features

- 🤖 **Conversational AI Agent** - Multi-turn conversation support with session management
- 📦 **Order Management** - 6 native Python tools for order operations (CRUD)
- 📋 **Complaint Management** - Integration with external MCP servers
- 🔄 **Streaming Support** - Optional Server-Sent Events for real-time responses
- 🐳 **Containerized** - Docker-ready with volumes for data persistence
- 📊 **Auto-seeding** - Configurable database initialization with 25 sample orders
- 📚 **Interactive API Docs** - Auto-generated Swagger/OpenAPI documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (for containerized deployment)
- Azure OpenAI credentials (configured in Azure CLI)
- External MCP server running at `http://localhost:8000/mcp` (for complaint management)

### Local Development Setup

1. **Clone and navigate to the project:**
   ```bash
   cd v15-e2e-casestudy/api-service
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

5. **Run the service:**
   ```bash
   python main.py
   ```

6. **Access the API:**
   - **Service**: http://localhost:9080
   - **Interactive Docs**: http://localhost:9080/docs
   - **ReDoc**: http://localhost:9080/redoc
   - **Health Check**: http://localhost:9080/health

### Docker Deployment

1. **Create `.env.docker` file** (copy from `.env.docker.example` and configure with your credentials)
   ```bash
   cp .env.docker.example .env.docker
   # Edit .env.docker with your Azure OpenAI credentials
   ```

2. **Build and run:**
   ```bash
   docker-compose up -d
   ```

3. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop service:**
   ```bash
   docker-compose down
   ```

## 📖 API Usage

### Health Check

```bash
curl http://localhost:9080/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "MSAv15Service",
  "version": "0.1.0",
  "timestamp": "2026-02-19T10:30:00Z",
  "dependencies": {
    "database": "connected",
    "mcp_server": "reachable"
  }
}
```

### Chat (Non-Streaming)

```bash
curl -X POST http://localhost:9080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "customer-123",
    "message": "I want to place an order for a laptop",
    "stream": false
  }'
```

**Response:**
```json
{
  "session_id": "customer-123",
  "response": "I'll help you place an order...",
  "timestamp": "2026-02-19T10:30:00Z",
  "metadata": {
    "turn_count": 1,
    "tools_used": ["create_customer_order"],
    "tokens_used": 450
  }
}
```

### Chat (Streaming)

```bash
curl -X POST http://localhost:9080/chat \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "session_id": "customer-123",
    "message": "Show me my orders",
    "stream": true
  }'
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         MSAv15Service (FastAPI)                     │
│         Port: 9080                                   │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
       ┌───────▼────────┐    ┌───────▼─────────────┐
       │ Native Tools    │    │ MCP HTTP Tool       │
       │ (6 functions)   │    │ (External Server)   │
       └───────┬────────┘    └───────┬─────────────┘
               │                      │
       ┌───────▼────────┐    ┌───────▼─────────────┐
       │ OrderManager   │    │ Complaint MCP       │
       │ (SQLite)       │    │ Server              │
       └────────────────┘    └─────────────────────┘
     orders.db             complaints.db
```

## 🛠️ Configuration

All configuration is managed via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVICE_PORT` | API service port | `9080` |
| `AZURE_AI_PROJECT_ENDPOINT` | Azure AI project endpoint | **Required** |
| `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` | Deployment name | `gpt-4o` |
| `ORDER_DB_PATH` | Order database path | `./data/orders.db` |
| `ORDER_DB_SEEDING_ENABLED` | Enable auto-seeding | `true` |
| `ORDER_DB_SEED_COUNT` | Number of sample orders | `25` |
| `MCP_COMPLAINT_SERVER_URL` | External MCP server URL | `http://localhost:8000/mcp` |

See `.env.example` for complete list.

## 📦 Order Management Tools

The agent has access to 6 order management tools:

1. **create_customer_order** - Create new orders
2. **get_customer_orders** - Get all orders for a customer
3. **get_order_details** - Get single order details
4. **search_orders_by_customer_name** - Search by partial name
5. **update_order_status** - Update order status
6. **search_orders_advanced** - Multi-filter search

## 📋 Complaint Management

Complaint management is handled by an external MCP server providing:
- create_complaint
- get_complaint
- update_complaint
- list_complaints
- filter_complaints
- delete_complaint

## 🧪 Testing

```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

## 📂 Project Structure

```
api-service/
├── main.py                    # FastAPI application (outside app/)
├── app/
│   ├── config.py              # Configuration management
│   ├── schemas.py             # Pydantic models
│   ├── prompts/
│   │   └── agent_system_prompt.txt
│   ├── routers/
│   │   ├── health.py
│   │   └── chat.py
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── session_manager.py
│   │   └── seeding_service.py
│   └── tools/
│       └── order_tools.py     # Modularized order tools
├── data/                      # Database storage (Docker volume)
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Product Manager**: Ramkumar (Ram)
- **Development Team (CAP)**:
  - Chandini
  - Ashok
  - Priya

## 🙏 Acknowledgments

- Built with [Microsoft Agent Framework](https://microsoft.github.io/agent-framework/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Integrated with Azure OpenAI

---

**Version**: 0.1.0  
**Last Updated**: February 19, 2026
