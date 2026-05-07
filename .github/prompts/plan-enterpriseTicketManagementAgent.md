## Plan: Enterprise Ticket-Management Agent Notebook

Build a new notebook at [day2-usecase/notebooks/ticket-management-agent-enterprise.ipynb](day2-usecase/notebooks/ticket-management-agent-enterprise.ipynb) that extends the existing ticket-management agent with: a SQLite-backed custom history provider (hybrid: in-memory cache + SQLite flush on save), three class-based **agent-level** middleware (input guardrail, exception handling, logging), and an end-of-notebook session-resume demo to prove SQLite persistence works.

**Steps**

**Phase 1 — Supporting files** *(create before notebook)*
1. Create `day2-usecase/lib/ticket_management/chat_history_models.py` — own SQLAlchemy `Base`, engine pointed at `sqlite:///./db/chat_history.db`, models `ChatMessage` and `BlockedQuery`, plus an `init_chat_history_db()` helper. *(Independent — can run first)*
2. Create `day2-usecase/db/blacklist.txt` — starter list of profanity / racial / crime / offensive words, `#`-comment style. *(Parallel with step 1)*

**Phase 2 — Notebook scaffolding**
3. Cell 1 — Imports, `.env`, `sys.path` (mirrors existing notebook). *Depends on step 1.*
4. Cell 2 — `init_db()` + `init_chat_history_db()`.

**Phase 3 — Custom history provider**
5. Cell 3 — `SqliteHistoryProvider(HistoryProvider)`:
   - `get_messages` returns `state["messages"]` if populated; otherwise loads rows from `chat_messages` for the `session_id`, hydrates into `Message`, caches into `state`.
   - `save_messages` appends to `state["messages"]` AND inserts new rows into SQLite.

**Phase 4 — Middleware (all class-based, agent-level)**
6. Cell 4 — `LoggingAgentMiddleware`: configures Python `logging` once → `logs/agent.log`; logs incoming last-user-message + msg count + run duration + response snippet.
7. Cell 5 — `ExceptionHandlingAgentMiddleware`: wraps `await call_next()` in try/except for `TimeoutError`, `ValueError`, `sqlalchemy.exc.SQLAlchemyError`, then generic `Exception`; on error sets `context.result = AgentResponse(...)` with a friendly message and **returns** (no re-raise).
8. Cell 6 — `InputGuardrailMiddleware`: loads words from `db/blacklist.txt`, compiles a single case-insensitive whole-word regex `\b(...)\b`. On match: logs the attempt + inserts a `blocked_queries` row + sets `context.result` with a polite refusal that names the matched word as the reason + raises `MiddlewareTermination`.

**Phase 5 — Agent assembly**
9. Cell 7 — `FoundryChatClient` + `client.as_agent(...)` reusing all six ticket tools, with `context_providers=[SqliteHistoryProvider()]` and `middleware=[InputGuardrailMiddleware(...), ExceptionHandlingAgentMiddleware(), LoggingAgentMiddleware()]` (guardrail outermost, logging innermost).
10. Cell 8 — `session = agent.create_session()`; print `session.id`.

**Phase 6 — Scenarios**
11. Cells 9–13 — Reuse existing scenarios 1–4 unchanged (Jessie raises → confirm → Aarav resolves → Aarav closes → list open).
12. Cell 14 — **Scenario 5: guardrail demo** — query containing a blacklisted word; expect polite refusal stating the reason.
13. Cell 15 — **Scenario 6: exception demo** — force a tool failure (e.g., resolve a non-existent ticket ID); expect friendly error message, no crash.
14. Cell 16 — Verification: direct DB read of Jessie's tickets (existing pattern).

**Phase 7 — Session-persistence demo (end of notebook)**
15. Cell 17 — `serialized = session.to_dict()`; print briefly.
16. Cell 18 — `SELECT COUNT(*) FROM chat_messages WHERE session_id = ?` to prove SQLite rows exist.
17. Cell 19 — `resumed = AgentSession.from_dict(serialized)`; build a **fresh** agent (same client + provider + middleware); run a follow-up like *"Remind me the ticket ID we registered for Jessie?"* with `session=resumed`. Successful recall proves SQLite-backed continuity.

**Relevant files**
- [day2-usecase/notebooks/ticket-management-agent.ipynb](day2-usecase/notebooks/ticket-management-agent.ipynb) — template for cells 1, 2, 7, 9–13, 16.
- [day2-usecase/lib/ticket_management/database.py](day2-usecase/lib/ticket_management/database.py) — pattern to mirror in `chat_history_models.py` (engine + sessionmaker + `get_session` ctx manager + `init_db`).
- [day2-usecase/lib/ticket_management/tools.py](day2-usecase/lib/ticket_management/tools.py) — six tool functions imported as-is.
- [maf-202/202-1-custom_message_store.ipynb](maf-202/202-1-custom_message_store.ipynb) — reference for `HistoryProvider` interface, `state["messages"]` pattern, and `to_dict`/`from_dict` round-trip.

**Verification**
1. Notebook runs top-to-bottom without unhandled exceptions.
2. Scenarios 1–4 produce the same behaviour as the existing notebook.
3. Scenario 5 returns a refusal naming the matched word; no ticket row created; one new row in `blocked_queries`.
4. Scenario 6 returns a friendly error string; `logs/agent.log` contains the captured exception entry.
5. `chat_messages` table contains rows for the active `session_id` after cell 17.
6. After cell 19, the resumed agent recalls the ticket ID correctly.

**Decisions**
- All three middleware are class-based and agent-level (function/chat scope is out of scope).
- Hybrid history: cache in `state["messages"]`, flush to SQLite on save, fall back to SQLite load on cold start.
- Separate DB file `db/chat_history.db` with its own SQLAlchemy `Base` (no coupling to tickets DB).
- Exception middleware degrades gracefully (returns instead of raising); guardrail terminates hard.
- Blacklist starter file authored by assistant; whole-word case-insensitive regex matching.
- `FoundryChatClient` retained.
- Session-resume demo lives only at the end.

**Out of scope**
- Function/chat-level middleware, streaming, tool approval, MCP, schema migrations, auth/encryption.
