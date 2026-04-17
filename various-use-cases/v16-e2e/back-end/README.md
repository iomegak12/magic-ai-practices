# MSEv15E2E - Customer Service Agent REST API

**Version:** 0.1.0  
**Status:** In Development  

Modern REST API service that exposes an AI-powered customer service agent with integrated MCP server, order management, and email capabilities.

## 🚀 Features

- **AI-Powered Agent**: Azure OpenAI GPT-4o based customer service agent
- **MCP Server Integration**: External complaint management via MCP protocol
- **Order Management**: SQLite-based order tracking and management
- **Email Capabilities**: Automated email sending via SMTP
- **Streaming Support**: Server-Sent Events (SSE) for real-time responses
- **Multi-tenant**: Tenant isolation for enterprise deployments
- **Rate Limiting**: Configurable IP-based rate limiting
- **Docker Ready**: Multi-stage Alpine-based container
- **Comprehensive Logging**: File rotation and structured logging

## 📋 Prerequisites

- Python 3.11+
- Azure OpenAI account with GPT-4o deployment
- Gmail account with app password (for email features)
- MCP server running at http://localhost:8000/mcp (optional)

## 🔧 Installation

### Local Development

1. **Clone the repository**
```bash
cd v16-e2e/back-end
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the server**
```bash
python server.py
```

The API will be available at http://localhost:9080

### Docker Deployment

1. **Build the image**
```bash
docker build -t msev15-e2e-service .
```

2. **Run with docker-compose**
```bash
docker-compose up -d
```

## 📖 API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:9080/docs
- **Alternative API Docs**: http://localhost:9080/redoc
- **Health Check**: http://localhost:9080/health

### Key Endpoints

#### Chat (Non-Streaming)
```bash
POST /api/v1/chat
{
  "session_id": "user-123",
  "message": "I need help with order #12345",
  "tenant_id": "company-A"
}
```

#### Chat (Streaming)
```bash
POST /api/v1/chat/stream
{
  "session_id": "user-123",
  "message": "Check my orders"
}
```

#### Session Management
```bash
GET    /api/v1/sessions/{session_id}/history
DELETE /api/v1/sessions/{session_id}
GET    /api/v1/sessions?tenant_id=company-A
```

## 🛠️ Configuration

All configuration via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_PORT` | API server port | 9080 |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Required |
| `MCP_SERVER_URL` | MCP server endpoint | http://localhost:8000/mcp |
| `ENABLE_RATE_LIMITING` | Enable rate limiting | false |
| `RATE_LIMIT_PER_MINUTE` | Requests per minute | 100 |

See [.env.example](.env.example) for complete configuration options.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_chat.py
```

## 🗂️ Project Structure

```
back-end/
├── app/                    # Application code
│   ├── api/               # FastAPI routes & middleware
│   ├── agent/             # Agent framework integration
│   ├── tools/             # Tool implementations
│   ├── session/           # Session management
│   ├── config/            # Configuration
│   ├── utils/             # Utilities & logging
│   └── startup/           # Startup/shutdown handlers
├── data/                  # Database files (gitignored)
├── logs/                  # Log files (gitignored)
├── tests/                 # Test suite
├── server.py              # Entry point
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker build
└── docker-compose.yml     # Container orchestration
```

## 📝 Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👥 Team

- **Product Manager**: Hemanth Shah
- **Developers**: Ramkumar, Rahul

## 📞 Support

For issues and support, please contact the development team.

---

**Built with** ❤️ **using FastAPI, Azure OpenAI, and Agent Framework**
