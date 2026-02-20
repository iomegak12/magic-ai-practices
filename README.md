# Magic AI Practices

This repository contains practice notebooks and materials for learning AI agent development, Microsoft Agent Framework (MAF), and Model Context Protocol (MCP) servers.

## Structure Changes

- **`maf-101/`** - Microsoft Agent Framework basics
  - `1-simple-agent.ipynb` - Creating basic agents
  - `2-agent-tools.ipynb` - Working with tools
  - `3-agent-session.ipynb` - Managing sessions
  - `4-agent-multi-turn-conversations.ipynb` - Multi-turn conversations
  - `5-workflows.ipynb` - Agent workflows
  - `6-multi-modal.ipynb` - Multi-modal interactions
  - `7-structured-output.ipynb` - Structured outputs
  - `8-background-responses.ipynb` - Background processing
  - `9-background-responses-streaming.ipynb` - Streaming responses

- **`maf-202/`** - Advanced MAF concepts
  - `mcp-use-1.ipynb` - MCP integration basics
  - `mcp-use-2.ipynb` - Advanced MCP usage
  - `exception_guardrails_middleware.ipynb` - Exception handling and guardrails

- **`mcp/`** - MCP Server implementations
  - `main.py` - Task Management MCP server with streamable HTTP support

- **`references/`** - Reference materials and code samples
- **`data/`** - Data files for practice
- **`env/`** - Python virtual environment

## Prerequisites

- Python 3.12+
- Azure CLI (for Azure authentication)
- Azure AI Project endpoint
- Azure OpenAI deployment

## Setup

### 1. Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate  # Windows
# or
source env/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=your-deployment-name
```

### 4. Azure Authentication

```bash
az login
```

## Usage

### Running Notebooks

Open notebooks in VS Code or Jupyter:

```bash
# Make sure virtual environment is activated
code .
```

Select the Python kernel from the `env` folder when running notebooks.

### Running MCP Task Management Server

The MCP server provides task management capabilities via streamable HTTP protocol.

```bash
cd mcp
python main.py
```

Server will be available at: `http://localhost:8000/mcp`

**Available Tools:**
- `create_task(title, description)` - Create a new task with auto-incremented ID
- `get_task(task_id)` - Retrieve a specific task by ID
- `get_all_tasks()` - Get all tasks
- `search_tasks(query)` - Case-insensitive partial search in title/description
- `update_task_completion(task_id, is_completed)` - Update task completion status

**Features:**
- In-memory task storage
- Auto-incrementing task IDs
- ISO format timestamps
- Graceful shutdown (Ctrl+C)
- Comprehensive logging

**Task Structure:**
```python
{
    "task_id": int,           # Auto-incremented
    "title": str,             # Task title
    "description": str,       # Task description
    "created_at": str,        # ISO format timestamp
    "is_completed": bool      # Completion status
}
```

## Key Concepts

### Microsoft Agent Framework (MAF)
- Building AI agents with Azure OpenAI
- Tool integration and function calling
- Session management
- Multi-turn conversations
- Middleware for guardrails and exception handling

### Model Context Protocol (MCP)
- Creating MCP servers with streamable HTTP
- Integrating MCP tools with agents
- Tool definitions and structured outputs

## License

This project is licensed under the MIT License - see the LICENSE file for details.
