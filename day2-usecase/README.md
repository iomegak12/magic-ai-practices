# IT Ticket Management — Day 2 Use Case

A modular Python library for IT support ticket management, backed by SQLite + SQLAlchemy ORM, with a Microsoft Agent Framework (MAF) agent notebook demonstrating multi-turn AI conversations.

## Quickstart

### 1. Prerequisites

```bash
pip install sqlalchemy python-dotenv agent-framework azure-identity
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your Azure AI Foundry values:

```
AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<id>
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4o
DATABASE_URL=sqlite:///./db/tickets.db
```

### 3. Seed the database

Run from the `day2-usecase/` folder:

```bash
python -m lib.ticket_management.seed
```

This creates `db/tickets.db` with 15 demo tickets.

### 4. Open the notebook

Open `notebooks/ticket-management-agent.ipynb` and run all cells.

---

## Library API summary

All functions live in `lib/ticket_management/repository.py` and are exposed as agent tools via `lib/ticket_management/tools.py`.

| Function | Description |
|---|---|
| `register_ticket(description, registered_by, priority)` | Creates a new ticket; returns the new ticket dict. |
| `get_tickets_by_registered_by(name)` | Returns all tickets raised by a person (partial, case-insensitive). |
| `get_tickets_by_resolved_by(name)` | Returns all tickets resolved by a person (partial, case-insensitive). |
| `search_tickets(description, status, priority)` | Filters tickets; all params optional; description is partial+case-insensitive. |
| `resolve_ticket(ticket_id, resolved_by, resolution_remarks)` | Marks ticket Resolved; sets resolved_by, remarks, resolved_date. |
| `close_ticket(ticket_id)` | Closes a Resolved, Open, or Cancelled ticket. |

### Priorities
`Low` · `Medium` · `High` · `Critical`

### Statuses
`Open` · `In Progress` · `On Hold` · `Resolved` · `Closed` · `Cancelled`

### Ticket ID format
Auto-generated sequential IDs: `DTKT10001`, `DTKT10002`, …

---

## Project layout

```
day2-usecase/
├── .env                          # local config (git-ignored)
├── .env.example                  # template
├── .gitignore
├── LICENSE
├── README.md
├── db/
│   └── tickets.db                # created at runtime
└── lib/
    └── ticket_management/
        ├── __init__.py
        ├── enums.py
        ├── models.py
        ├── database.py
        ├── id_generator.py
        ├── repository.py
        ├── tools.py
        └── seed.py
notebooks/
    └── ticket-management-agent.ipynb
```

## License

MIT — see [LICENSE](LICENSE).
