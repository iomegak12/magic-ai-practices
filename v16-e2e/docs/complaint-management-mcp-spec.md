# Complaint Management MCP Server - Specification Document

**Version:** 1.0.0  
**Date:** February 18, 2026  
**Project Type:** Model Context Protocol (MCP) Server  
**Core Developer:** Ramkumar  
**Team Members:** Chandini, Priya, Ashok

---

## 1. Project Overview

### 1.1 Purpose
Develop an MCP server to track and manage customer complaints related to specific orders. The server will provide comprehensive complaint management capabilities through MCP tools, enabling AI assistants and clients to interact with the complaint system seamlessly.

### 1.2 Objectives
- Provide a robust complaint management system with CRUD operations
- Enable advanced search and filtering capabilities
- Maintain complaint history with soft-delete archival
- Expose functionality through MCP protocol over HTTP
- Persist data in SQLite database using SQLAlchemy ORM
- Auto-seed sample data for testing and demonstration

---

## 2. Technical Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.12 |
| **MCP Framework** | FastMCP | 2.10.6 |
| **Transport Protocol** | Streamable HTTP | - |
| **ORM** | SQLAlchemy | Latest |
| **Database** | SQLite | 3.x |
| **Configuration** | python-dotenv | Latest |
| **Data Validation** | Pydantic | Latest |

---

## 3. Data Model

### 3.1 Complaint Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `complaint_id` | Integer | Primary Key, Auto-increment | Unique identifier |
| `title` | String(200) | NOT NULL | Complaint title |
| `description` | Text | NOT NULL | Detailed complaint description |
| `customer_name` | String(100) | NOT NULL | Name of the customer |
| `order_number` | String(50) | NOT NULL, Format: ORD-XXXXX | Associated order number |
| `created_at` | DateTime | NOT NULL, Default: UTC Now | Timestamp when complaint was created |
| `updated_at` | DateTime | NOT NULL, Auto-update | Timestamp when complaint was last updated |
| `priority` | Enum | NOT NULL, Default: MEDIUM | Complaint priority level |
| `status` | Enum | NOT NULL, Default: OPEN | Current complaint status |
| `remarks` | Text | Nullable | Additional notes or remarks |
| `is_archived` | Boolean | NOT NULL, Default: False | Soft-delete flag |
| `resolution_date` | DateTime | Nullable | Timestamp when complaint was resolved |

### 3.2 Enumeration Values

#### Priority Enum
```
- LOW
- MEDIUM (default)
- HIGH
- CRITICAL
```

#### Status Enum
```
- OPEN (default)
- IN_PROGRESS
- RESOLVED
- CLOSED
```

### 3.3 Database Schema (SQLAlchemy Model)

**Table Name:** `complaints`

**Indexes:**
- Primary Key on `complaint_id`
- Index on `customer_name` (for search optimization)
- Index on `order_number` (for search optimization)
- Index on `status` (for filtering)
- Index on `is_archived` (for filtering active complaints)

---

## 4. MCP Tools Specification

### 4.1 Tool: `register_complaint`

**Description:** Register a new customer complaint

**Parameters:**
- `title` (string, required): Complaint title (max 200 chars)
- `description` (string, required): Detailed description
- `customer_name` (string, required): Customer name (max 100 chars)
- `order_number` (string, required): Order number (format: ORD-XXXXX)
- `priority` (string, optional): Priority level (LOW|MEDIUM|HIGH|CRITICAL), default: MEDIUM
- `remarks` (string, optional): Additional remarks

**Returns:**
```json
{
  "success": true,
  "message": "Complaint registered successfully",
  "complaint_id": 1,
  "data": {
    "complaint_id": 1,
    "title": "...",
    "status": "OPEN",
    "created_at": "2026-02-18T10:30:00Z"
  }
}
```

**Validation Rules:**
- Title: Required, 5-200 characters
- Description: Required, minimum 10 characters
- Customer name: Required, 2-100 characters
- Order number: Required, must match pattern `ORD-\d{5,}`
- Priority: Must be valid enum value

---

### 4.2 Tool: `get_complaint`

**Description:** Retrieve detailed information about a specific complaint

**Parameters:**
- `complaint_id` (integer, required): The complaint ID to retrieve

**Returns:**
```json
{
  "success": true,
  "data": {
    "complaint_id": 1,
    "title": "Product defect",
    "description": "...",
    "customer_name": "John Doe",
    "order_number": "ORD-10001",
    "priority": "HIGH",
    "status": "OPEN",
    "remarks": "...",
    "created_at": "2026-02-18T10:30:00Z",
    "updated_at": "2026-02-18T10:30:00Z",
    "resolution_date": null,
    "is_archived": false
  }
}
```

**Error Handling:**
- Returns error if complaint_id not found
- Returns error if complaint is archived (unless explicitly requested)

---

### 4.3 Tool: `search_complaints`

**Description:** Search complaints using multiple filter criteria (OR logic)

**Parameters:**
- `customer_name` (string, optional): Filter by customer name (partial match)
- `order_number` (string, optional): Filter by order number (partial match)
- `title` (string, optional): Filter by title (partial match)
- `status` (string, optional): Filter by status (exact match)
- `include_archived` (boolean, optional): Include archived complaints, default: false

**Search Logic:**
- Multiple filters applied with OR logic
- Partial matching for text fields (case-insensitive)
- Exact matching for status
- Always excludes archived unless `include_archived=true`

**Returns:**
```json
{
  "success": true,
  "count": 5,
  "filters_applied": ["customer_name", "status"],
  "data": [
    {
      "complaint_id": 1,
      "title": "...",
      "customer_name": "...",
      "order_number": "...",
      "status": "...",
      "priority": "...",
      "created_at": "..."
    },
    // ... more results
  ]
}
```

---

### 4.4 Tool: `resolve_complaint`

**Description:** Mark a complaint as resolved and update status

**Parameters:**
- `complaint_id` (integer, required): The complaint ID to resolve
- `remarks` (string, optional): Resolution remarks/notes

**Business Logic:**
- Changes status to "RESOLVED"
- Sets `resolution_date` to current UTC timestamp
- Appends remarks if provided
- Updates `updated_at` timestamp

**Returns:**
```json
{
  "success": true,
  "message": "Complaint resolved successfully",
  "data": {
    "complaint_id": 1,
    "status": "RESOLVED",
    "resolution_date": "2026-02-18T15:45:00Z",
    "updated_at": "2026-02-18T15:45:00Z"
  }
}
```

**Validation:**
- Complaint must exist
- Cannot resolve already archived complaints
- Cannot resolve already resolved complaints (idempotent check)

---

### 4.5 Tool: `update_complaint`

**Description:** Update complaint details (title, description, remarks only)

**Parameters:**
- `complaint_id` (integer, required): The complaint ID to update
- `title` (string, optional): New title
- `description` (string, optional): New description
- `remarks` (string, optional): New/additional remarks

**Business Logic:**
- Only updates provided fields
- Cannot update status (use resolve_complaint instead)
- Cannot update priority after creation
- Cannot update archived complaints
- Updates `updated_at` timestamp

**Returns:**
```json
{
  "success": true,
  "message": "Complaint updated successfully",
  "updated_fields": ["title", "remarks"],
  "data": {
    "complaint_id": 1,
    "title": "Updated title",
    "remarks": "Updated remarks",
    "updated_at": "2026-02-18T16:00:00Z"
  }
}
```

**Validation:**
- At least one field must be provided
- Same validation rules as register_complaint

---

### 4.6 Tool: `archive_complaint`

**Description:** Archive a complaint (soft-delete)

**Parameters:**
- `complaint_id` (integer, required): The complaint ID to archive

**Business Logic:**
- Sets `is_archived` to True
- Does not delete from database (soft-delete)
- Updates `updated_at` timestamp
- Archived complaints excluded from normal searches

**Returns:**
```json
{
  "success": true,
  "message": "Complaint archived successfully",
  "data": {
    "complaint_id": 1,
    "is_archived": true,
    "archived_at": "2026-02-18T17:00:00Z"
  }
}
```

**Validation:**
- Complaint must exist
- Cannot archive already archived complaint (idempotent)

---

## 5. Configuration Management

### 5.1 Environment Variables (.env)

```ini
# Server Configuration
MCP_SERVER_NAME=complaint-management-server
MCP_SERVER_DESCRIPTION=MCP Server for managing customer complaints and orders
MCP_SERVER_VERSION=1.0.0
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_MOUNT_PATH=/mcp

# Database Configuration
DATABASE_PATH=db/complaints.db
DATABASE_ECHO=false

# Seeding Configuration
AUTO_SEED_DATABASE=true
SEED_RECORD_COUNT=20

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Application Settings
TIMEZONE=UTC
```

### 5.2 Configuration Loading Strategy
- Use `python-dotenv` to load environment variables
- Provide default values for all settings
- Validate configuration on startup
- Log configuration (mask sensitive values)

---

## 6. Database Seeding Strategy

### 6.1 Seeding Logic

**Trigger Conditions:**
- `AUTO_SEED_DATABASE=true` in .env
- Database table is empty (count = 0)

**Seeding Process:**
1. Check if `complaints` table exists
2. Count existing records
3. If count == 0 and AUTO_SEED_DATABASE is true:
   - Generate `SEED_RECORD_COUNT` sample complaints
   - Use realistic sample data (customer names, order numbers)
   - Randomize priorities and statuses
   - Set varied timestamps (past 30 days)
   - Insert all records in a transaction

### 6.2 Sample Data Characteristics

**Customer Names:** Mix of common names (15-20 unique customers)
**Order Numbers:** ORD-10001 to ORD-10050 (varied)
**Titles:** Realistic complaint scenarios
- "Product arrived damaged"
- "Wrong item shipped"
- "Missing parts in package"
- "Late delivery"
- "Quality issues with product"
- etc.

**Status Distribution:**
- 40% OPEN
- 30% IN_PROGRESS
- 20% RESOLVED
- 10% CLOSED

**Priority Distribution:**
- 30% LOW
- 40% MEDIUM
- 20% HIGH
- 10% CRITICAL

**Archived:** 10% of records (2 out of 20)

---

## 7. Project Structure

```
complaint-management-mcp/
│
├── .env                          # Environment configuration
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # Project documentation
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
├── requirements.txt              # Python dependencies
├── server.py                     # Main MCP server entry point
│
├── db/                           # Database directory
│   └── complaints.db             # SQLite database (gitignored)
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── models.py                 # SQLAlchemy models
│   ├── database.py               # Database connection & session
│   ├── enums.py                  # Enum definitions
│   ├── tools/                    # MCP tools
│   │   ├── __init__.py
│   │   ├── register.py           # Register complaint tool
│   │   ├── get.py                # Get complaint tool
│   │   ├── search.py             # Search complaints tool
│   │   ├── resolve.py            # Resolve complaint tool
│   │   ├── update.py             # Update complaint tool
│   │   └── archive.py            # Archive complaint tool
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py
│   │   ├── validators.py         # Input validation
│   │   ├── seed_data.py          # Database seeding
│   │   └── logger.py             # Logging configuration
│   └── schemas.py                # Pydantic schemas
│
├── tests/                        # Test directory (future)
│   ├── __init__.py
│   └── test_tools.py
│
└── docs/                         # Documentation
    ├── API.md                    # API documentation
    └── USAGE_EXAMPLES.md         # Sample prompts & resources
```

---

## 8. Sample Prompts and Resources

### 8.1 Location
All sample prompts and usage examples will be documented in `README.md` under "Usage Examples" section.

### 8.2 Sample Prompt Categories

#### A. Registering Complaints
```
"Register a new complaint for customer John Doe, order ORD-10001, 
about a damaged product with high priority"

"Create a complaint: Customer Sarah Smith received wrong item for order ORD-10025"
```

#### B. Retrieving Complaint Details
```
"Show me details of complaint ID 5"

"Get full information about complaint number 12"
```

#### C. Searching Complaints
```
"Find all complaints from customer John Doe"

"Search for complaints related to order ORD-10001"

"Show me all open complaints"

"Find complaints with status RESOLVED or order number ORD-10015"
```

#### D. Resolving Complaints
```
"Resolve complaint ID 3 with remark 'Refund processed'"

"Mark complaint 7 as resolved"
```

#### E. Updating Complaints
```
"Update complaint 5 title to 'Product quality issue - Resolved'"

"Add remarks to complaint 10: 'Customer contacted via email'"
```

#### F. Archiving Complaints
```
"Archive complaint ID 8"

"Remove complaint 15 from active list"
```

### 8.3 MCP Resource Definitions

The server will expose the following MCP resources:

#### Resource: `complaint://active`
- **URI:** `complaint://active`
- **Description:** List of all active (non-archived) complaints
- **MIME Type:** `application/json`

#### Resource: `complaint://{complaint_id}`
- **URI:** `complaint://123`
- **Description:** Detailed view of specific complaint
- **MIME Type:** `application/json`

#### Resource: `complaint://stats`
- **URI:** `complaint://stats`
- **Description:** Complaint statistics and summary
- **MIME Type:** `application/json`
- **Content:** Count by status, priority distribution, etc.

---

## 9. Error Handling Strategy

### 9.1 Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "COMPLAINT_NOT_FOUND",
    "message": "Complaint with ID 999 not found",
    "details": {}
  }
}
```

### 9.2 Error Codes

| Code | Description |
|------|-------------|
| `COMPLAINT_NOT_FOUND` | Complaint ID does not exist |
| `VALIDATION_ERROR` | Input validation failed |
| `INVALID_STATUS` | Invalid status value |
| `INVALID_PRIORITY` | Invalid priority value |
| `ALREADY_ARCHIVED` | Complaint already archived |
| `ALREADY_RESOLVED` | Complaint already resolved |
| `DATABASE_ERROR` | Database operation failed |
| `INVALID_ORDER_NUMBER` | Order number format invalid |

---

## 10. Validation Rules

### 10.1 Field Validations

| Field | Rules |
|-------|-------|
| `title` | Required, 5-200 characters, no special chars except - _ , . |
| `description` | Required, minimum 10 characters |
| `customer_name` | Required, 2-100 characters, letters and spaces only |
| `order_number` | Required, format: `ORD-\d{5,}` (e.g., ORD-10001) |
| `priority` | Must be: LOW, MEDIUM, HIGH, or CRITICAL |
| `status` | Must be: OPEN, IN_PROGRESS, RESOLVED, or CLOSED |
| `remarks` | Optional, max 1000 characters |

### 10.2 Business Rules

1. **Cannot modify archived complaints** - All update/resolve operations fail on archived complaints
2. **Status changes restricted** - Status can only change through `resolve_complaint` tool
3. **Priority immutable** - Priority cannot be changed after complaint creation
4. **Idempotent operations** - Resolving/archiving already resolved/archived complaints returns success without changes
5. **Soft-delete only** - No hard deletion of complaints

---

## 11. Logging Strategy

### 11.1 Log Levels
- **INFO:** Server startup, tool invocations, successful operations
- **WARNING:** Validation failures, business rule violations
- **ERROR:** Database errors, system errors
- **DEBUG:** Detailed request/response data (development only)

### 11.2 Log Format
```
2026-02-18 10:30:45 - complaint-mcp - INFO - Complaint registered: ID=1, Customer=John Doe
```

### 11.3 What to Log
- Server startup/shutdown events
- All tool invocations with parameters (sanitized)
- Database operations (queries, inserts, updates)
- Validation errors with details
- System errors with stack traces

---

## 12. Dependencies (requirements.txt)

```txt
fastmcp==2.10.6
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
faker>=20.0.0          # For generating seed data
```

---

## 13. Git Configuration

### 13.1 .gitignore Contents
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Database
db/
*.db
*.sqlite
*.sqlite3

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

---

## 14. License

**Type:** MIT License

**Copyright Holder:** Ramkumar and Team (Chandini, Priya, Ashok)

---

## 15. Documentation Files

### 15.1 README.md Structure
1. Project title and description
2. Features list
3. Technical stack
4. Installation instructions
5. Configuration guide
6. Usage examples with sample prompts
7. MCP tools documentation
8. Testing instructions
9. Contributing guidelines link
10. License information
11. Team and contacts

### 15.2 CONTRIBUTING.md Structure
1. Welcome message
2. Core developer: Ramkumar
3. Team members: Chandini, Priya, Ashok
4. How to contribute
5. Code style guidelines
6. Pull request process
7. Issue reporting guidelines
8. Development setup
9. Testing requirements

### 15.3 CHANGELOG.md Structure
```markdown
# Changelog

## [1.0.0] - 2026-02-18

### Added
- Initial release
- Six MCP tools for complaint management
- SQLite database with SQLAlchemy ORM
- Automatic database seeding
- Soft-delete archival functionality
- Configuration via .env file
- Comprehensive documentation
```

---

## 16. Implementation Roadmap

### Phase 1: Project Setup (Days 1-2)
- [ ] Create project structure
- [ ] Setup virtual environment
- [ ] Create all documentation files (README, CONTRIBUTING, CHANGELOG)
- [ ] Add .gitignore and LICENSE
- [ ] Create .env.example

### Phase 2: Core Infrastructure (Days 3-5)
- [ ] Implement configuration management (config.py)
- [ ] Define enums (enums.py)
- [ ] Create SQLAlchemy models (models.py)
- [ ] Setup database connection and session management (database.py)
- [ ] Implement Pydantic schemas (schemas.py)

### Phase 3: Utilities (Days 6-7)
- [ ] Implement validators (validators.py)
- [ ] Create seed data generator (seed_data.py)
- [ ] Setup logging configuration (logger.py)

### Phase 4: MCP Tools Implementation (Days 8-12)
- [ ] Implement register_complaint tool
- [ ] Implement get_complaint tool
- [ ] Implement search_complaints tool
- [ ] Implement resolve_complaint tool
- [ ] Implement update_complaint tool
- [ ] Implement archive_complaint tool

### Phase 5: Server Setup (Days 13-14)
- [ ] Create main server.py entry point
- [ ] Integrate all tools with FastMCP
- [ ] Implement signal handlers for graceful shutdown
- [ ] Add startup logging and configuration validation
- [ ] Implement database initialization and seeding

### Phase 6: Testing & Documentation (Days 15-16)
- [ ] Test all tools individually
- [ ] Test search with various filter combinations
- [ ] Test database seeding logic
- [ ] Validate error handling
- [ ] Complete README with usage examples
- [ ] Document sample prompts and resources

### Phase 7: Polish & Deployment (Days 17-18)
- [ ] Code review and refactoring
- [ ] Performance optimization
- [ ] Final documentation review
- [ ] Create deployment guide
- [ ] Tag v1.0.0 release

---

## 17. Success Criteria

1. ✅ All six MCP tools function correctly
2. ✅ Database persists data across server restarts
3. ✅ Auto-seeding works with 20 sample records
4. ✅ Search supports OR logic with multiple filters
5. ✅ Soft-delete archival prevents data loss
6. ✅ Configuration via .env works correctly
7. ✅ All documentation files are complete and accurate
8. ✅ Server runs on streamable HTTP transport
9. ✅ Validation rules properly enforce data integrity
10. ✅ Error handling provides clear, actionable messages

---

## 18. Future Enhancements (Out of Scope for v1.0)

- Pagination for search results
- Hard-delete functionality
- Complaint assignment to support agents
- Email notifications
- Complaint categories/tags
- File attachments
- Complaint history tracking
- Analytics and reporting dashboard
- Authentication and authorization
- Multi-tenant support

---

## Document Approval

**Prepared by:** GitHub Copilot  
**Reviewed by:** [Pending - Ramkumar]  
**Approved by:** [Pending]  
**Date:** February 18, 2026

---

**End of Specification Document**
