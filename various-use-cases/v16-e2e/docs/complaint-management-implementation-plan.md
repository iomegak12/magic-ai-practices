# Complaint Management MCP Server - Implementation Plan

**Version:** 1.0.0  
**Date:** February 19, 2026  
**Project:** Complaint Management MCP Server  
**Core Developer:** Ramkumar  
**Team:** Chandini, Priya, Ashok

---

## Implementation Overview

**Total Estimated Time:** 18 days  
**Technology Stack:** Python 3.12, FastMCP 2.10.6, SQLAlchemy, SQLite  
**Project Location:** `v16-e2e/mcp-servers/complaint-management-mcp/`

---

## Phase 1: Project Setup & Foundation (Days 1-2)

### Objectives
- Create complete project structure
- Setup Python virtual environment
- Initialize documentation files
- Configure version control

### Tasks
1. **Project Structure Creation**
   ```
   complaint-management-mcp/
   ├── .env
   ├── .env.example
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   ├── CONTRIBUTING.md
   ├── CHANGELOG.md
   ├── requirements.txt
   ├── server.py
   ├── db/
   ├── src/
   │   ├── __init__.py
   │   ├── config.py
   │   ├── models.py
   │   ├── database.py
   │   ├── enums.py
   │   ├── schemas.py
   │   ├── tools/
   │   │   └── __init__.py
   │   └── utils/
   │       └── __init__.py
   └── tests/
       └── __init__.py
   ```

2. **Virtual Environment Setup**
   ```bash
   cd v16-e2e/mcp-servers/complaint-management-mcp
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Dependencies Installation**
   Create `requirements.txt`:
   ```
   fastmcp==2.10.6
   sqlalchemy>=2.0.0
   python-dotenv>=1.0.0
   pydantic>=2.0.0
   faker>=20.0.0
   ```
   Install: `pip install -r requirements.txt`

4. **Documentation Files**
   - LICENSE (MIT)
   - README.md (structure from spec doc)
   - CONTRIBUTING.md (team info)
   - CHANGELOG.md (v1.0.0 template)

5. **.gitignore**
   ```gitignore
   __pycache__/
   *.py[cod]
   db/
   *.db
   .env
   venv/
   logs/
   ```

6. **.env.example**
   ```ini
   MCP_SERVER_NAME=complaint-management-server
   MCP_SERVER_DESCRIPTION=MCP Server for managing customer complaints
   MCP_SERVER_VERSION=1.0.0
   MCP_SERVER_HOST=0.0.0.0
   MCP_SERVER_PORT=8000
   MCP_MOUNT_PATH=/mcp
   DATABASE_PATH=db/complaints.db
   DATABASE_ECHO=false
   AUTO_SEED_DATABASE=true
   SEED_RECORD_COUNT=20
   LOG_LEVEL=INFO
   TIMEZONE=UTC
   ```

### Deliverables
✅ Complete folder structure  
✅ Virtual environment activated  
✅ Dependencies installed  
✅ All documentation files created  
✅ Git repository initialized

---

## Phase 2: Core Infrastructure (Days 3-5)

### Objectives
- Implement configuration management
- Define data models and enums
- Setup database connection
- Create validation schemas

### Tasks

#### 1. **Enums Definition** (`src/enums.py`)
```python
from enum import Enum

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Status(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
```

#### 2. **Configuration Management** (`src/config.py`)
- Load environment variables using `python-dotenv`
- Define Config class with all settings
- Validate configuration on load
- Provide default values

**Key Features:**
- Server config (name, host, port)
- Database config (path, echo)
- Seeding config (auto_seed, count)
- Logging config (level, format)

#### 3. **Database Models** (`src/models.py`)
- Define `Complaint` SQLAlchemy model
- Include all fields from spec
- Add indexes for optimization
- Implement `to_dict()` method

**Model Fields:**
- complaint_id (PK, auto-increment)
- title, description, customer_name, order_number
- created_at, updated_at (UTC timestamps)
- priority (enum), status (enum)
- remarks, is_archived, resolution_date

#### 4. **Database Connection** (`src/database.py`)
- Create SQLAlchemy engine
- Setup session factory
- Implement session management
- Create tables on startup

#### 5. **Pydantic Schemas** (`src/schemas.py`)
- Request/response schemas for each tool
- Field validators
- Type definitions

### Deliverables
✅ Enums defined (Priority, Status)  
✅ Config loader implemented  
✅ Complaint model created  
✅ Database connection established  
✅ Pydantic schemas ready

---

## Phase 3: Utilities & Supporting Services (Days 6-7)

### Objectives
- Implement input validators
- Create database seeding service
- Setup logging infrastructure

### Tasks

#### 1. **Input Validators** (`src/utils/validators.py`)

**Functions to Implement:**
```python
def validate_title(title: str) -> tuple[bool, str]
def validate_description(description: str) -> tuple[bool, str]
def validate_customer_name(name: str) -> tuple[bool, str]
def validate_order_number(order_num: str) -> tuple[bool, str]
def validate_priority(priority: str) -> tuple[bool, str]
def validate_status(status: str) -> tuple[bool, str]
```

**Validation Rules:**
- Title: 5-200 chars, no special chars except `-_,.`
- Description: min 10 chars
- Customer name: 2-100 chars, letters and spaces
- Order number: `ORD-\d{5,}` pattern
- Priority/Status: valid enum values

#### 2. **Database Seeder** (`src/utils/seed_data.py`)

**Implementation:**
- Use Faker library for realistic data
- Generate 20 sample complaints
- Randomize priorities and statuses
- Set varied timestamps (past 30 days)
- Follow distribution from spec:
  - Priority: 30% LOW, 40% MED, 20% HIGH, 10% CRIT
  - Status: 40% OPEN, 30% IN_PROG, 20% RESOLVED, 10% CLOSED
  - Archived: 10% (2 records)

**Key Function:**
```python
def seed_database(session, count: int) -> int
```

#### 3. **Logger Configuration** (`src/utils/logger.py`)

**Setup:**
- Console and file handlers
- Configurable log levels
- Formatted output with timestamps
- Sanitize sensitive data

### Deliverables
✅ All validators implemented  
✅ Seeding service ready  
✅ Logger configured  
✅ Unit tests for validators

---

## Phase 4: MCP Tools Implementation (Days 8-12)

### Objectives
- Implement all 6 MCP tools
- Add error handling
- Format responses consistently

### Tool 1: **Register Complaint** (`src/tools/register.py`)

**Function Signature:**
```python
@mcp.tool(name="register_complaint", description="...")
def register_complaint(
    title: str,
    description: str,
    customer_name: str,
    order_number: str,
    priority: str = "MEDIUM",
    remarks: str = None
) -> dict
```

**Implementation Steps:**
1. Validate all inputs
2. Create Complaint instance
3. Set defaults (status=OPEN, created_at=UTC now)
4. Insert to database
5. Return success response with complaint_id

---

### Tool 2: **Get Complaint** (`src/tools/get.py`)

**Function Signature:**
```python
@mcp.tool(name="get_complaint", description="...")
def get_complaint(complaint_id: int) -> dict
```

**Implementation Steps:**
1. Query complaint by ID
2. Check if exists
3. Check if archived (optional flag)
4. Return complaint data

---

### Tool 3: **Search Complaints** (`src/tools/search.py`)

**Function Signature:**
```python
@mcp.tool(name="search_complaints", description="...")
def search_complaints(
    customer_name: str = None,
    order_number: str = None,
    title: str = None,
    status: str = None,
    include_archived: bool = False
) -> dict
```

**Implementation Steps:**
1. Build OR query with provided filters
2. Apply `is_archived=False` filter (unless included)
3. Use LIKE for text fields (case-insensitive)
4. Use exact match for status
5. Return list with count

**OR Query Logic:**
```python
filters = []
if customer_name:
    filters.append(Complaint.customer_name.ilike(f"%{customer_name}%"))
if order_number:
    filters.append(Complaint.order_number.ilike(f"%{order_number}%"))
# ... etc
query = query.filter(or_(*filters))
```

---

### Tool 4: **Resolve Complaint** (`src/tools/resolve.py`)

**Function Signature:**
```python
@mcp.tool(name="resolve_complaint", description="...")
def resolve_complaint(
    complaint_id: int,
    remarks: str = None
) -> dict
```

**Implementation Steps:**
1. Query complaint by ID
2. Check if exists
3. Check if already resolved (idempotent)
4. Check if archived (error)
5. Update status to RESOLVED
6. Set resolution_date = UTC now
7. Append remarks if provided
8. Update updated_at
9. Commit and return

---

### Tool 5: **Update Complaint** (`src/tools/update.py`)

**Function Signature:**
```python
@mcp.tool(name="update_complaint", description="...")
def update_complaint(
    complaint_id: int,
    title: str = None,
    description: str = None,
    remarks: str = None
) -> dict
```

**Implementation Steps:**
1. Validate at least one field provided
2. Query complaint by ID
3. Check if archived (error)
4. Update only provided fields
5. Update updated_at
6. Return updated fields list

**Restrictions:**
- Cannot update status (use resolve_complaint)
- Cannot update priority
- Cannot update archived complaints

---

### Tool 6: **Archive Complaint** (`src/tools/archive.py`)

**Function Signature:**
```python
@mcp.tool(name="archive_complaint", description="...")
def archive_complaint(complaint_id: int) -> dict
```

**Implementation Steps:**
1. Query complaint by ID
2. Check if exists
3. Check if already archived (idempotent)
4. Set is_archived = True
5. Update updated_at
6. Commit and return

---

### Error Handling Strategy

**For All Tools:**
```python
try:
    # Tool logic
    return {
        "success": True,
        "message": "...",
        "data": {...}
    }
except ValidationError as e:
    return {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": str(e)
        }
    }
except NotFoundError:
    return {
        "success": False,
        "error": {
            "code": "COMPLAINT_NOT_FOUND",
            "message": f"Complaint {id} not found"
        }
    }
# ... etc
```

### Deliverables
✅ All 6 tools implemented  
✅ Error handling in place  
✅ Response formatting consistent  
✅ Integration tests for each tool

---

## Phase 5: Server Setup & Integration (Days 13-14)

### Objectives
- Create main server entry point
- Integrate all tools with FastMCP
- Implement signal handlers
- Add database initialization

### Tasks

#### 1. **Server Entry Point** (`server.py`)

**Implementation:**
```python
import signal
import sys
import logging
from fastmcp import FastMCP
from src.config import load_config
from src.database import init_database, seed_database
from src.utils.logger import setup_logging

# Initialize
config = load_config()
logger = setup_logging(config)

# Create MCP instance
mcp = FastMCP(
    name=config.server_name,
    instructions=config.server_description,
    host=config.host,
    port=config.port
)

# Import and register tools
from src.tools.register import register_complaint
from src.tools.get import get_complaint
from src.tools.search import search_complaints
from src.tools.resolve import resolve_complaint
from src.tools.update import update_complaint
from src.tools.archive import archive_complaint

# Signal handler for graceful shutdown
def signal_handler(signum, frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize database
    init_database()
    
    # Seed if needed
    if config.auto_seed:
        seed_database()
    
    # Start server
    logger.info(f"Starting {config.server_name}...")
    logger.info(f"Server available at http://{config.host}:{config.port}{config.mount_path}")
    
    try:
        mcp.run(transport="streamable-http", mount_path=config.mount_path)
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        logger.info("Server shutdown complete")
```

#### 2. **Database Initialization**

**In `database.py`:**
- Create database directory if not exists
- Create all tables
- Check if seeding needed
- Execute seeding if conditions met

#### 3. **Startup Flow**
1. Load configuration
2. Setup logging
3. Initialize FastMCP instance
4. Register signal handlers
5. Initialize database
6. Seed database (if needed)
7. Register tools
8. Start HTTP transport
9. Log server ready

### Deliverables
✅ Server.py implemented  
✅ All tools registered  
✅ Signal handlers working  
✅ Database auto-initialization  
✅ Seeding on first run  
✅ Server starts successfully

---

## Phase 6: Testing & Documentation (Days 15-16)

### Objectives
- Test all tools individually
- Test search combinations
- Validate error handling
- Complete documentation

### Tasks

#### 1. **Testing Checklist**

**Unit Tests:**
- [ ] Validators work correctly
- [ ] Models serialize/deserialize
- [ ] Config loads properly
- [ ] Seeder generates valid data

**Integration Tests:**
- [ ] Register complaint creates record
- [ ] Get complaint retrieves correct data
- [ ] Search with single filter works
- [ ] Search with multiple filters (OR logic) works
- [ ] Search excludes archived by default
- [ ] Resolve updates status and timestamp
- [ ] Resolve is idempotent
- [ ] Update modifies only specified fields
- [ ] Update rejects archived complaints
- [ ] Archive sets flag correctly
- [ ] Archive is idempotent

**End-to-End Tests:**
- [ ] Server starts without errors
- [ ] All tools accessible via HTTP
- [ ] Database persists after restart
- [ ] Seeding occurs only once
- [ ] Graceful shutdown works

#### 2. **Test Script Creation**

Create `tests/test_tools.py`:
```python
import pytest
from src.tools.register import register_complaint
# ... test each tool
```

Create `tests/manual_test_scenarios.rest`:
```http
### Register Complaint
POST http://localhost:8000/mcp
Content-Type: application/json

{
  "tool": "register_complaint",
  "params": {
    "title": "Product damaged",
    "description": "Received broken items in shipment",
    "customer_name": "John Doe",
    "order_number": "ORD-10001",
    "priority": "HIGH"
  }
}
```

#### 3. **Documentation Completion**

**README.md:**
- Project description
- Features list
- Installation guide
- Quick start
- Usage examples
- API documentation
- Contributing link
- License

**Sample Usage Examples:**
```markdown
## Usage Examples

### Register a Complaint
"Register a complaint for customer John Doe, order ORD-10001, about damaged product"

### Search Complaints
"Find all complaints from John Doe"
"Show me all open complaints"
"Search complaints for order ORD-10015 or with HIGH priority"
```

### Deliverables
✅ All unit tests passing  
✅ All integration tests passing  
✅ Manual testing complete  
✅ README.md finished  
✅ Usage examples documented

---

## Phase 7: Polish & Deployment (Days 17-18)

### Objectives
- Code review and refactoring
- Performance optimization
- Create deployment guide
- Tag release

### Tasks

#### 1. **Code Review**
- Review all modules for consistency
- Check error handling coverage
- Validate logging is comprehensive
- Ensure code follows Python standards (PEP 8)
- Add docstrings where missing
- Remove debug code

#### 2. **Performance Optimization**
- Verify database indexes are in place
- Test query performance
- Check connection pooling
- Optimize seeding process

#### 3. **Deployment Guide**

Create `docs/DEPLOYMENT.md`:
```markdown
# Deployment Guide

## Production Setup
1. Clone repository
2. Create virtual environment
3. Install production dependencies
4. Configure .env for production
5. Set DATABASE_ECHO=false
6. Configure logging to file
7. Start server

## Systemd Service (Linux)
[Service configuration]

## Docker Deployment
[Docker instructions]
```

#### 4. **Release Preparation**
- Update CHANGELOG.md with v1.0.0 details
- Verify all documentation is accurate
- Test on clean environment
- Create release notes

#### 5. **Git Operations**
```bash
git add .
git commit -m "Initial release v1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

### Deliverables
✅ Code reviewed and refactored  
✅ Performance optimized  
✅ Deployment guide created  
✅ v1.0.0 tagged and released  
✅ All success criteria met

---

## Success Criteria Checklist

Before considering development complete, verify:

- [ ] All six MCP tools function correctly
- [ ] Database persists data across server restarts
- [ ] Auto-seeding works with 20 sample records
- [ ] Search supports OR logic with multiple filters
- [ ] Soft-delete archival prevents data loss
- [ ] Configuration via .env works correctly
- [ ] All documentation files are complete and accurate
- [ ] Server runs on streamable HTTP transport
- [ ] Validation rules properly enforce data integrity
- [ ] Error handling provides clear, actionable messages

---

## Quick Start Command Reference

### Setup
```bash
# Create project directory
mkdir -p v16-e2e/mcp-servers/complaint-management-mcp
cd v16-e2e/mcp-servers/complaint-management-mcp

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
copy .env.example .env
```

### Development
```bash
# Run server
python server.py

# Run tests
pytest tests/

# Check code style
flake8 src/
```

### Testing Endpoints
```http
# Server should be running at:
http://localhost:8000/mcp

# Test with curl or Postman
# See tests/manual_test_scenarios.rest for examples
```

---

## Team Responsibilities

| Team Member | Primary Focus | Support Areas |
|-------------|---------------|---------------|
| **Ramkumar** | Core developer, architecture, final review | All areas |
| **Chandini** | Tools implementation, testing | Database, schemas |
| **Priya** | Database, models, seeding | Validators, utilities |
| **Ashok** | Documentation, deployment | Configuration, logging |

---

## Progress Tracking

Use this checklist to track overall progress:

### Phase Status
- [ ] Phase 1: Project Setup (2 days)
- [ ] Phase 2: Core Infrastructure (3 days)
- [ ] Phase 3: Utilities (2 days)
- [ ] Phase 4: MCP Tools (5 days)
- [ ] Phase 5: Server Setup (2 days)
- [ ] Phase 6: Testing & Docs (2 days)
- [ ] Phase 7: Polish & Deploy (2 days)

### Milestone Dates
- **Kickoff:** [Date]
- **Phase 1-3 Complete:** [Date] (Target: Day 7)
- **Phase 4 Complete:** [Date] (Target: Day 12)
- **Beta Ready:** [Date] (Target: Day 14)
- **Release v1.0.0:** [Date] (Target: Day 18)

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dependency conflicts | Medium | Use virtual env, pin versions |
| Database corruption | High | Regular backups, transactions |
| Performance issues | Medium | Early testing with seed data |
| Incomplete testing | High | Dedicated testing phase |
| Documentation lag | Medium | Write docs alongside code |

---

## Next Steps

1. **Review this plan** with the team
2. **Set milestone dates** based on availability
3. **Assign task ownership** among team members
4. **Begin Phase 1** - Project setup
5. **Hold daily standups** (15 min) to track progress
6. **Update CHANGELOG.md** after each phase

---

**Document Status:** Ready for Review ✅  
**Prepared By:** GitHub Copilot  
**Date:** February 19, 2026  
**Approved By:** [Pending - Ramkumar]

---

**Ready to start development!** 🚀
