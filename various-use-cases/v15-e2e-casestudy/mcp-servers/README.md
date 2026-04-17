# Complaint Management MCP Server

A production-ready Model Context Protocol (MCP) server for managing customer complaints related to orders. Built with FastMCP, SQLAlchemy ORM, and SQLite.

## Features

- **Complete CRUD Operations**: Create, Read, Update, Delete complaints
- **Advanced Filtering**: Filter by status, priority, customer name, and order ID
- **Auto-generated IDs**: Sequential complaint IDs with auto-increment
- **Timestamps**: Automatic registration and update timestamps
- **Validation**: Built-in validation for status and priority values
- **Structured Output**: All tools return consistent JSON responses
- **Modular Architecture**: Clean separation of concerns

## Project Structure

```
mcp-servers/
├── main.py                      # FastMCP server entry point
├── .env                         # Configuration (database path)
├── requirements.txt             # Python dependencies
├── db/                          # SQLite database folder (auto-created)
│   └── complaints.db           # Database file (auto-created)
└── complaint-manager/          # Core business logic
    ├── __init__.py             # Package initialization
    ├── config.py               # Configuration management
    ├── models.py               # SQLAlchemy ORM models
    ├── database.py             # Database connection & session management
    └── tools.py                # MCP tool implementations
```

## Installation

### Option 1: Local Installation

#### 1. Install Dependencies

```bash
cd mcp-servers
pip install -r requirements.txt
```

#### 2. Configure Environment

Edit `.env` file if needed (default configuration works out of the box):

```env
DATABASE_PATH=db/complaints.db
SEED_DATABASE=true
```

**Configuration Options:**
- `DATABASE_PATH`: SQLite database location (relative to mcp-servers folder)
- `SEED_DATABASE`: Set to `true` to auto-seed with 15 sample complaints (only if database is empty)

#### 3. Run the Server

```bash
cd mcp-servers
python main.py
```

### Option 2: Docker Installation

#### 1. Configure Docker Environment (Optional)

Edit `.env.docker` if needed (default configuration works out of the box):

```env
SERVER_NAME=complaint-management-server
SERVER_VERSION=1.0.0
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
MCP_MOUNT_PATH=/mcp
DATABASE_PATH=db/complaints.db
SEED_DATABASE=true
```

#### 2. Build and Run with Docker Compose

```bash
cd mcp-servers
docker-compose up -d
```

#### 3. View Logs

```bash
docker-compose logs -f
```

#### 4. Stop the Server

```bash
docker-compose down
```

### Server Behavior

The server will:
- Initialize the SQLite database automatically
- Create the `db` folder and tables if they don't exist
- Seed sample data if `SEED_DATABASE=true` and database is empty
- Start listening on `http://0.0.0.0:8000/mcp`

## Data Model

### Complaint Fields

| Field | Type | Description | Auto-Generated |
|-------|------|-------------|----------------|
| `complaint_id` | Integer | Unique complaint identifier | ✓ (Auto-increment) |
| `description` | Text | Detailed complaint description | ✗ |
| `customer_name` | String | Customer name | ✗ |
| `order_id` | String | Associated order ID | ✗ |
| `complaint_registration_date` | DateTime | When complaint was created | ✓ (Auto-set) |
| `remarks` | Text | Additional notes/remarks | ✗ (Optional) |
| `priority` | String | Complaint priority | ✗ (Default: "Medium") |
| `status` | String | Complaint status | ✗ (Default: "New") |
| `updated_at` | DateTime | Last update timestamp | ✓ (Auto-updated) |

### Valid Values

**Priority Levels**: `Low`, `Medium`, `High`, `Critical`

**Status Values**: `New`, `Open`, `In Progress`, `Resolved`, `Closed`

## MCP Tools

### 1. create_complaint

Create a new customer complaint.

**Parameters:**
- `description` (string, required): Detailed complaint description
- `customer_name` (string, required): Customer name
- `order_id` (string, required): Associated order ID
- `priority` (string, optional): Low|Medium|High|Critical (default: "Medium")
- `remarks` (string, optional): Additional notes

**Example:**
```json
{
  "description": "Product arrived damaged",
  "customer_name": "John Doe",
  "order_id": "ORD-12345",
  "priority": "High",
  "remarks": "Customer requested immediate replacement"
}
```

### 2. get_complaint

Retrieve a specific complaint by ID.

**Parameters:**
- `complaint_id` (integer, required): Complaint ID to retrieve

**Example:**
```json
{
  "complaint_id": 1
}
```

### 3. update_complaint

Update an existing complaint (any combination of fields).

**Parameters:**
- `complaint_id` (integer, required): Complaint ID to update
- `status` (string, optional): New|Open|In Progress|Resolved|Closed
- `priority` (string, optional): Low|Medium|High|Critical
- `remarks` (string, optional): Updated remarks
- `description` (string, optional): Updated description

**Example:**
```json
{
  "complaint_id": 1,
  "status": "In Progress",
  "remarks": "Investigation started"
}
```

### 4. list_complaints

List all complaints (newest first).

**Parameters:**
- `limit` (integer, optional): Maximum results (default: 100)

**Example:**
```json
{
  "limit": 50
}
```

### 5. filter_complaints

Filter complaints by multiple criteria.

**Parameters:**
- `status` (string, optional): Filter by status
- `priority` (string, optional): Filter by priority
- `customer_name` (string, optional): Filter by customer (partial match)
- `order_id` (string, optional): Filter by order ID
- `limit` (integer, optional): Maximum results (default: 100)

**Examples:**
```json
// Get all high priority complaints
{
  "priority": "High",
  "limit": 50
}

// Get all open complaints for a customer
{
  "customer_name": "John",
  "status": "Open"
}

// Get all complaints for a specific order
{
  "order_id": "ORD-12345"
}
```

### 6. delete_complaint

Permanently delete a complaint.

**Parameters:**
- `complaint_id` (integer, required): Complaint ID to delete

**Example:**
```json
{
  "complaint_id": 1
}
```

## Response Format

All tools return structured JSON responses:

```json
{
  "operation": "create_complaint",
  "success": true,
  "message": "Complaint created successfully",
  "result": {
    "complaint_id": 1,
    "description": "Product arrived damaged",
    "customer_name": "John Doe",
    "order_id": "ORD-12345",
    "complaint_registration_date": "2026-02-18T10:30:00",
    "remarks": "Customer requested immediate replacement",
    "priority": "High",
    "status": "New",
    "updated_at": "2026-02-18T10:30:00"
  }
}
```

**Error Response:**
```json
{
  "operation": "update_complaint",
  "success": false,
  "error": "Complaint with ID 999 not found",
  "result": null
}
```

## Technology Stack

- **FastMCP**: MCP server framework
- **SQLAlchemy**: Python ORM for database operations
- **SQLite**: Lightweight embedded database
- **python-dotenv**: Environment variable management
- **uvicorn**: ASGI server
- **Docker**: Containerization support

## Docker Deployment

### Dockerfile Features
- Based on Python 3.12 slim image
- Optimized layer caching
- Minimal dependencies
- Production-ready configuration

### Docker Compose
- Single service deployment
- Persistent volume for database
- Network isolation
- Auto-restart on failure
- Environment variable configuration

## Configuration

### Environment Variables

#### Local Development (.env)

```env
# Server Configuration
SERVER_NAME=complaint-management-server
SERVER_VERSION=1.0.0
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
MCP_MOUNT_PATH=/mcp

# Database Configuration
DATABASE_PATH=db/complaints.db

# Seed Database with Sample Data (true/false)
SEED_DATABASE=true
```

#### Docker Deployment (.env.docker)

Same configuration as `.env` but specifically for Docker Compose deployment. Modify `.env.docker` to change Docker container settings without affecting local development.

### Sample Data

When `SEED_DATABASE=true`, the server automatically seeds the database with **15 sample complaints** on first run:
- Various customers (John Smith, Sarah Johnson, etc.)
- Multiple order IDs (ORD-10001 through ORD-10015)
- All priority levels (Low, Medium, High, Critical)
- All status types (New, Open, In Progress, Resolved, Closed)
- Realistic scenarios (damaged products, wrong items, late delivery, etc.)

**Note**: Seeding only occurs if the database is completely empty. If any complaints exist, seeding is skipped.

### Server Configuration (complaint-manager/config.py)

```python
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
MCP_MOUNT_PATH = "/mcp"
```

## Logging

The server provides comprehensive logging:
- Database initialization
- Tool operations (create, update, delete)
- Error tracking
- Graceful shutdown events

## Graceful Shutdown

Press `Ctrl+C` to stop the server gracefully. The server will:
- Log shutdown initiation
- Close database connections
- Clean up resources

## Training Use Cases

### Scenario 1: Customer Reports Defective Product
```python
# Create complaint
create_complaint(
    description="Laptop screen has dead pixels",
    customer_name="Alice Smith",
    order_id="ORD-78901",
    priority="High"
)

# Update status as team investigates
update_complaint(complaint_id=1, status="In Progress")

# Close with resolution
update_complaint(
    complaint_id=1,
    status="Resolved",
    remarks="Replacement laptop shipped"
)
```

### Scenario 2: Track All High Priority Issues
```python
# Filter by priority
filter_complaints(priority="High")

# Filter by priority and status
filter_complaints(priority="Critical", status="Open")
```

### Scenario 3: Order-Specific Investigation
```python
# Get all complaints for an order
filter_complaints(order_id="ORD-12345")
- To reset: delete `db/complaints.db` and restart server

### Seeding Issues
- Ensure `SEED_DATABASE=true` in `.env`
- Seeding only works on empty database
- Check logs for seed operation status
- To re-seed: delete database file and restart

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python 3.8+ is being used
- Check working directory is `mcp-servers/`

### Port Already in Use
- Change port in `complaint-manager/config.py`
- Or stop the process using port 8000
- Docker: change port mapping in `docker-compose.yml`
- GraphQL API support
- WebSocket real-time updates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Designed for Agentic AI Training by Ramkumar**

© 2026 - Professional Training on Agentic AI Systems
- Rebuild: `docker-compose up --build`
- Clean restart: `docker-compose down -v && docker-compose up -d`lters for precise queries
5. **Regular Cleanup**: Archive or delete old resolved complaints

## Troubleshooting

### Database Issues
- Database and tables are auto-created on first run
- Check `db/` folder permissions
- Review logs for initialization errors

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python 3.8+ is being used

### Port Already in Use
- Change port in `complaint-manager/config.py`
- Or stop the process using port 8000

## Future Enhancements

- Search functionality (full-text search)
- Export to CSV/Excel
- Email notifications on status changes
- Attachment support
- Complaint analytics dashboard
- Multi-tenancy support

---

**Designed for Agentic AI Training by Ramkumar**
