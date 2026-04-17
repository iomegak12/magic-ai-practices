## Plan: Customer Complaints Library + Agent Notebook

Build a modular SQLAlchemy+SQLite library (`customers_complaints/`) at the workspace root with customer, complaint, and profile preference management. Expose features as `@tool`-decorated functions. Create a notebook at `use-cases/maf-tools-mtt-ccp.ipynb` demonstrating tools (auto-approved) + a context provider that extracts customer identity from conversation to inject profile tier into agent instructions.

---

### Phase 1: Library — `customers_complaints/`

**Files to create:**

| File | Purpose |
|---|---|
| `customers_complaints/__init__.py` | Re-export all public tools + `init_db` for clean imports |
| `customers_complaints/database.py` | Engine, session factory, Base; reads `DATABASE_PATH` from `.env` via `python-dotenv` |
| `customers_complaints/models.py` | 3 ORM models: `Customer`, `Complaint`, `CustomerProfilePreference` |
| `customers_complaints/customer_tools.py` | `get_customer_by_id`, `search_customers` — decorated with `@tool` |
| `customers_complaints/complaint_tools.py` | `get_complaints_by_customer`, `get_complaints_by_status`, `register_complaint` — `@tool` decorated |
| `customers_complaints/profile_preferences.py` | `get_customer_profile` — helper/tool to look up customer tier |
| `customers_complaints/seed.py` | Seeds 15 Indian customers + ~65-70 IT complaints + 15 profile records |
| `customers_complaints/README.md` | Library documentation |

**Models (in `models.py`):**

- **Customer** — `customer_id` (PK, auto-gen `CUST10001`+), `customer_name`, `address`, `email`, `phone`, `active_status` (default `"active"`), `remarks`
- **Complaint** — `complaint_id` (PK, auto-gen `COMP10001`+), `complaint_date` (datetime), `customer_id` (FK→Customer), `complaint_description`, `priority` (Critical/High/Medium/Low), `status` (Open/In Progress/Resolved/Closed/Reopened)
- **CustomerProfilePreference** — `id` (PK), `customer_id` (FK→Customer, unique 1:1), `customer_type` (platinum/gold/silver/general)

**Key design details:**
- `database.py` uses `load_dotenv()` to read `DATABASE_PATH` from `.env`; engine points to `sqlite:///{DATABASE_PATH}/customers_complaints.db`
- Auto-generated IDs: query max existing ID, increment (or start at 10001)
- `register_complaint` checks the customer's profile type — if **platinum** and no priority explicitly given → default to **High**
- `search_customers` uses SQLAlchemy `ilike` for partial, case-insensitive matching on name/address/email
- All tools follow the existing pattern: `@tool(approval_mode="never_require")` + `Annotated[type, Field(description="...")]`

**Seed data (`seed.py`):**
- 15 Indian customers (realistic names, cities like Mumbai, Delhi, Bangalore, Chennai, etc.)
- Each customer has 4-5 IT complaints (laptop issues, VPN problems, software crashes, access requests, etc.)
- Profile types: **Shweta = platinum**, rest distributed across gold/silver/general
- Runnable as `python -m customers_complaints.seed`

---

### Phase 2: Notebook — `use-cases/maf-tools-mtt-ccp.ipynb`

**Cell flow:**

1. **Imports + path setup** — `sys.path` insert, import all tools from `customers_complaints`, import framework classes
2. **DB init + seed check** — call `init_db()`, optionally run seed if DB is empty
3. **Context Provider** — `CustomerProfileProvider(BaseContextProvider)`:
   - `after_run()`: scans tool output / `context.input_messages` for customer_id references, stores it
   - `before_run()`: if customer is identified, looks up profile type -> injects into `context.instructions` (e.g., *"Current customer is Shweta (platinum tier). For platinum customers, default complaint priority is HIGH."*)
4. **Agent setup** — `AzureOpenAIResponsesClient` + `client.as_agent(name="ComplaintsAgent", instructions=..., tools=[5 tools], context_providers=[profile_provider])`
5. **Session creation** — `session = agent.create_session()`
6. **Test A**: `"Search for customer named Shweta"` → invokes `search_customers` → returns Shweta's record
7. **Test B**: `"Register an IT complaint for her — laptop not connecting to corporate VPN"` → invokes `register_complaint` → auto-sets priority to **High** (platinum)
8. **Test C**: `"Show me the complaint details for this customer"` → invokes `get_complaints_by_customer`

---

### Phase 3: Supporting Files

- **`.env`** at workspace root — add `DATABASE_PATH=./data` (keeping any existing env vars intact)
- The `.env` already doesn't exist, so we'll create it with both the database path and placeholder notes for the Azure env vars

---

### Relevant Files (reference patterns)
- `maf-101/crm_system_tools/customer_tools.py` — reference for `@tool` decorator pattern + parameter annotations
- `maf-101/4-agent-multi-turn-conversations.ipynb` — reference for `BaseContextProvider` / `before_run` / `after_run` pattern
- `pyproject.toml` — SQLAlchemy already listed as dependency

---

### Verification
1. Run `python -m customers_complaints.seed` — confirm DB at `./data/customers_complaints.db` with 15 customers, ~65-70 complaints, 15 profile records
2. Run each tool function independently in a Python REPL to verify correct output
3. Run the notebook end-to-end — search Shweta → register complaint (verify **High** priority auto-set) → retrieve complaints
4. Rename/change `DATABASE_PATH` in `.env` to verify it's respected
5. Check all `.py` files for lint/type errors

---

### Decisions
- Priority: Critical / High / Medium / Low
- Status: Open / In Progress / Resolved / Closed / Reopened
- Profile preferences lives inside `customers_complaints/` as `profile_preferences.py` (not a separate library)
- Shweta is platinum to demo the auto-HIGH priority feature
- Context provider extracts customer identity from conversation (tool outputs), not pre-set
- `.env` with `DATABASE_PATH` for DB location configuration
