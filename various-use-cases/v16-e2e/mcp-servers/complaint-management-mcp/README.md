# Complaint Management MCP Server

**Version:** 1.0.0  
**MCP Framework:** FastMCP 2.10.6  
**Python:** 3.12+

A Model Context Protocol (MCP) server for managing customer complaints and orders. This server provides comprehensive complaint management capabilities through MCP tools, enabling AI assistants and clients to interact with the complaint system seamlessly.

---

## 🚀 Features

- **Register Complaints** - Create new customer complaints with order details
- **Retrieve Complaints** - Get detailed information about specific complaints
- **Search Complaints** - Advanced search with OR-logic filtering by customer, order, title, or status
- **Resolve Complaints** - Mark complaints as resolved with timestamps and remarks
- **Update Complaints** - Modify complaint details (title, description, remarks)
- **Archive Complaints** - Soft-delete complaints while preserving data

### Key Capabilities

✅ **Persistent Storage** - SQLite database with SQLAlchemy ORM  
✅ **Auto-Seeding** - Automatically populate with 20 sample complaints on first run  
✅ **Soft-Delete** - Archive complaints without data loss  
✅ **Validation** - Comprehensive input validation and error handling  
✅ **Configuration** - Easy setup via environment variables  
✅ **HTTP Transport** - Streamable HTTP protocol for MCP communication

---

## 📋 Technical Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.12 |
| MCP Framework | FastMCP | 2.10.6 |
| Transport | Streamable HTTP | - |
| ORM | SQLAlchemy | 2.0+ |
| Database | SQLite | 3.x |
| Configuration | python-dotenv | 1.0+ |
| Validation | Pydantic | 2.0+ |
| Test Data | Faker | 20.0+ |

---

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. **Navigate to project directory**
   ```bash
   cd v16-e2e/mcp-servers/complaint-management-mcp
   ```

2. **Activate existing virtual environment**
   ```bash
   # From workspace root
   env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

5. **Edit `.env` file** (optional)
   - Adjust server port, database path, or seeding settings

---

## ⚙️ Configuration

Configuration is managed through the `.env` file. Copy `.env.example` and customize as needed.

### Server Settings
```ini
MCP_SERVER_NAME=complaint-management-server
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_MOUNT_PATH=/mcp
```

### Database Settings
```ini
DATABASE_PATH=db/complaints.db  # Relative to project root
DATABASE_ECHO=false              # Set to true for SQL query logging
```

### Seeding Settings
```ini
AUTO_SEED_DATABASE=true   # Auto-create 20 sample complaints
SEED_RECORD_COUNT=20      # Number of records to seed
```

---

## 🚀 Quick Start

### Start the Server

```bash
python server.py
```

You should see:
```
INFO - Starting complaint-management-server...
INFO - Server available at http://0.0.0.0:8000/mcp
INFO - Database initialized
INFO - Seeded 20 sample complaints
INFO - Press Ctrl+C to stop the server gracefully
```

### Test the Server

The server exposes MCP tools via HTTP at `http://localhost:8000/mcp`

---

## 📚 MCP Tools Documentation

### 1. Register Complaint

**Tool Name:** `register_complaint`

**Description:** Register a new customer complaint

**Parameters:**
- `title` (string, required) - Complaint title (5-200 characters)
- `description` (string, required) - Detailed description (minimum 10 characters)
- `customer_name` (string, required) - Customer name (2-100 characters)
- `order_number` (string, required) - Order number (format: ORD-XXXXX)
- `priority` (string, optional) - Priority level: LOW, MEDIUM (default), HIGH, CRITICAL
- `remarks` (string, optional) - Additional remarks

**Example:**
```
"Register a complaint for customer John Doe, order ORD-10001, about a damaged product with high priority"
```

---

### 2. Get Complaint

**Tool Name:** `get_complaint`

**Description:** Retrieve detailed information about a specific complaint

**Parameters:**
- `complaint_id` (integer, required) - The complaint ID

**Example:**
```
"Show me details of complaint ID 5"
```

---

### 3. Search Complaints

**Tool Name:** `search_complaints`

**Description:** Search complaints using multiple filter criteria (OR logic)

**Parameters:**
- `customer_name` (string, optional) - Filter by customer name (partial match)
- `order_number` (string, optional) - Filter by order number (partial match)
- `title` (string, optional) - Filter by title (partial match)
- `status` (string, optional) - Filter by status: OPEN, IN_PROGRESS, RESOLVED, CLOSED
- `include_archived` (boolean, optional) - Include archived complaints (default: false)

**Examples:**
```
"Find all complaints from customer John Doe"
"Search for complaints related to order ORD-10001"
"Show me all open complaints"
"Find complaints with HIGH priority or from John Doe"
```

---

### 4. Resolve Complaint

**Tool Name:** `resolve_complaint`

**Description:** Mark a complaint as resolved

**Parameters:**
- `complaint_id` (integer, required) - The complaint ID to resolve
- `remarks` (string, optional) - Resolution notes

**Example:**
```
"Resolve complaint ID 3 with remark 'Refund processed'"
```

---

### 5. Update Complaint

**Tool Name:** `update_complaint`

**Description:** Update complaint details (title, description, remarks only)

**Parameters:**
- `complaint_id` (integer, required) - The complaint ID to update
- `title` (string, optional) - New title
- `description` (string, optional) - New description
- `remarks` (string, optional) - New remarks

**Example:**
```
"Update complaint 5 title to 'Product quality issue - Resolved'"
```

---

### 6. Archive Complaint

**Tool Name:** `archive_complaint`

**Description:** Archive a complaint (soft-delete)

**Parameters:**
- `complaint_id` (integer, required) - The complaint ID to archive

**Example:**
```
"Archive complaint ID 8"
```

---

## 📊 Data Model

### Complaint Entity

| Field | Type | Description |
|-------|------|-------------|
| `complaint_id` | Integer | Unique identifier (auto-increment) |
| `title` | String | Complaint title |
| `description` | Text | Detailed description |
| `customer_name` | String | Customer name |
| `order_number` | String | Order number (ORD-XXXXX) |
| `created_at` | DateTime | Creation timestamp (UTC) |
| `updated_at` | DateTime | Last update timestamp (UTC) |
| `priority` | Enum | LOW, MEDIUM, HIGH, CRITICAL |
| `status` | Enum | OPEN, IN_PROGRESS, RESOLVED, CLOSED |
| `remarks` | Text | Additional notes |
| `is_archived` | Boolean | Soft-delete flag |
| `resolution_date` | DateTime | When complaint was resolved |

---

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Manual Testing

Use the provided test scenarios in `tests/manual_test_scenarios.rest` with a REST client like:
- VS Code REST Client extension
- Postman
- curl

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Core Developer:** Ramkumar  
**Team Members:** Chandini, Priya, Ashok

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For issues, questions, or contributions:
- Create an issue in the repository
- Contact the core development team
- Review the documentation in `/docs` folder

---

## 🗂️ Project Structure

```
complaint-management-mcp/
├── .env                          # Environment configuration
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This file
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
├── requirements.txt              # Python dependencies
├── server.py                     # Main server entry point
├── db/                           # Database directory (gitignored)
├── src/                          # Source code
│   ├── config.py                 # Configuration management
│   ├── models.py                 # SQLAlchemy models
│   ├── database.py               # Database connection
│   ├── enums.py                  # Enum definitions
│   ├── schemas.py                # Pydantic schemas
│   ├── tools/                    # MCP tools implementation
│   └── utils/                    # Utility modules
└── tests/                        # Test suite
```

---

## 📅 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

**Built with ❤️ by Ramkumar and Team**
