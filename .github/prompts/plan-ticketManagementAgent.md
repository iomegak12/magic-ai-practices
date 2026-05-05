## Plan: IT Ticket Management Library + MAF Agent Notebook

Build a modular `ticket_management` library (SQLAlchemy + SQLite) under `day2-usecase/lib/`, seed it with 15 demo tickets, and demonstrate it from `day2-usecase/notebooks/ticket-management-agent.ipynb` using a single Microsoft Agent Framework agent that drives 3 multi-turn scenarios (Jessie creates → IT Admin resolves → IT Admin closes) over a single session.

### Decisions (confirmed)
- **Priorities**: Low, Medium, High, Critical
- **Statuses**: Open, In Progress, On Hold, Resolved, Closed, Cancelled
- **Layout**: modularized package under `day2-usecase/lib/ticket_management/`
- **Agent**: ONE `ITSupportAgent`, single session across all 3 scenarios
- **Tool approval**: `never_require`
- **Tools exposed**: `register_ticket`, `get_tickets_by_registered_by`, `get_tickets_by_resolved_by`, `search_tickets`, `resolve_ticket`, `close_ticket`
- **IDs**: sequential `DTKT10001+`, computed via MAX(id)+1 inside the insert transaction
- **Env**: `.env` with `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`, `DATABASE_URL=sqlite:///./db/tickets.db` (loaded via `python-dotenv`)
- **Seed names**: Mixed US / Australia / India (Jessie Thompson, Liam O'Connor, Aarav Sharma, Priya Iyer, Emma Wilson, Noah Smith, …)

### Target layout
```
day2-usecase/
├── .env / .env.example / .gitignore / LICENSE / README.md
├── db/.gitkeep
├── lib/ticket_management/
│   ├── __init__.py, enums.py, models.py, database.py,
│   ├── id_generator.py, repository.py, tools.py, seed.py
└── notebooks/ticket-management-agent.ipynb
```

### Phases & steps

**Phase 1 — Library (sequential)**
1. `enums.py` — `Priority`, `Status`
2. `models.py` — SQLAlchemy `Ticket` (incl. nullable `resolved_*` fields, `to_dict()`)
3. `database.py` — `engine`, `Base`, `SessionLocal`, `init_db()`, `get_session()` ctx mgr (reads `DATABASE_URL` via dotenv)
4. `id_generator.py` — `next_ticket_id(session)` parses suffix after `DTKT`, increments
5. `repository.py` — pure functions (no decorators) for register/search/get-by/resolve/close, returning JSON-serialisable dicts; case-insensitive partial matching for description & person fields

**Phase 2 — Tools** (*depends on Phase 1*)
6. `tools.py` — thin `@tool(approval_mode="never_require")` wrappers with `Annotated[..., Field(description=...)]` parameters and clear docstrings; each opens its own short-lived session

**Phase 3 — Seed** (*depends on Phase 1*, *parallel with Phase 2*)
7. `seed.py` — calls `init_db()`, inserts 15 mixed tickets (variety of priorities, statuses, registered_by, some already resolved with remarks)

**Phase 4 — Project files** (*parallel*)
8. `.env`, `.env.example`, `.gitignore`, MIT `LICENSE` (2026, Ramkumar), `README.md`

**Phase 5 — Notebook** (*depends on Phases 1–3*)
9. Cell A: imports + `load_dotenv()` + add `lib/` to `sys.path` + `init_db()`
10. Cell B: build `FoundryChatClient` + `client.as_agent(name="ITSupportAgent", instructions=…, tools=[…6 tools])`
11. Cell C: `session = agent.create_session()`
12. Cell D — **Scenario 1 (Jessie)**: VPN issue → expects `register_ticket` call
13. Cell E — Optional confirmation turn (Jessie asks for ticket ID/status)
14. Cell F — **Scenario 2 (IT Admin resolves)**: Aarav Sharma resolves with VPN cert remarks → expects `resolve_ticket`
15. Cell G — **Scenario 3 (IT Admin closes)**: closes Jessie's resolved ticket → expects `close_ticket`
16. Cell H — Verification: direct repository read prints final ticket as `Closed`

### Reference patterns reused
- `@tool` + `Annotated`/`Field` schema from [maf-101/2-agent-tools.ipynb](maf-101/2-agent-tools.ipynb)
- `FoundryChatClient` + `agent.create_session()` + repeated `agent.run(..., session=session)` from [maf-101/4-agent-multi-turn-conversations.ipynb](maf-101/4-agent-multi-turn-conversations.ipynb)
- Modular SQLAlchemy precedent in [customers_complaints/database.py](customers_complaints/database.py), [customers_complaints/models.py](customers_complaints/models.py), [customers_complaints/seed.py](customers_complaints/seed.py)

### Verification
1. `python day2-usecase/lib/ticket_management/seed.py` — `db/tickets.db` created, 15 rows, IDs `DTKT10001..DTKT10015`.
2. Smoke test: `search_tickets(status="Open")` returns rows; `search_tickets(description="VPN")` matches case-insensitively.
3. Notebook runs top-to-bottom against a live Foundry endpoint; each scenario triggers the correct tool; final cell shows Jessie's ticket as `Closed` with `resolved_by`/`resolution_remarks`/`resolved_date` populated.
4. Re-running the notebook adds a fresh `DTKT10016+` ticket without corrupting seed data.

### Scope — excluded
- Auth beyond existing Azure CLI credential
- REST/web UI, Alembic migrations, pytest suite
- Approval workflow / HITL gating
- Async SQLAlchemy

### Further considerations (please confirm before I implement)
1. **Close-ticket rule** — Allow closing only `Resolved`? Or also `Open`/`On Hold`/`Cancelled`?
   *Recommendation:* allow `Resolved`, `Cancelled`, `Open` (admin discretion); reject already-`Closed`.
2. **`registered_date` source** — server-side `datetime.utcnow()` ISO, or caller-supplied?
   *Recommendation:* server-side UTC, uniform across rows.
3. **README depth** — concise 1-page quickstart, or full API reference?
   *Recommendation:* concise quickstart with API summary table.
