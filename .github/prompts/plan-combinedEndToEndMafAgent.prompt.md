# Plan: Combined End-to-End MAF Agent Notebook

A single self-contained notebook at [end-to-end-scenario.ipynb](use-cases-day4/experiments/end-to-end-scenario.ipynb) that combines **all four MAF capabilities** — MCP tools, OpenTelemetry observability, LLM guardrails/exception handling/logging middleware, and SQLite-backed conversation history — into one agent with zero external file dependencies.

---

## Phase 1: Setup & Infrastructure (Cells 1–3)

1. **Intro markdown** — Title, architecture diagram (text), prerequisites (MCP server on 8700, Jaeger on 4317, env vars)
2. **All imports in one cell** — `agent_framework` (Agent, tool, AgentMiddleware, FunctionMiddleware, MCPStreamableHTTPTool, HistoryProvider, Message, AgentSession, etc.), `agent_framework.observability`, `agent_framework.openai`, `opentelemetry.trace`, `azure.identity.aio`, `openai.AzureOpenAI`, `pydantic`, stdlib (`os`, `json`, `time`, `asyncio`, `logging`, `sqlite3`, `functools.partial`, `datetime`, `zoneinfo`)
3. **Env + logging setup** — `load_dotenv()`, read `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`, `AZURE_OPENAI_API_KEY`; configure logging format

## Phase 2: Component Definitions (Cells 4–13)

4–5. **Guardrail prompts** — `INPUT_GUARDRAIL_SYSTEM_PROMPT` and `OUTPUT_GUARDRAIL_SYSTEM_PROMPT` defined inline. Input prompt updated: on-topic = **Customer Service, Azure Documentation, Weather, Time, Location**. Off-topic = cooking, sports, entertainment, etc.

6–7. **Classifier** — `create_guardrail_client()` + `classify_text()` inline (same logic as [classifier.py](use-cases-day4/experiments/use-case-4/classifier.py): `temperature=0.0`, JSON response format, fails open on errors)

8–9. **4 Middleware classes** inline — copied from [middleware.py](use-cases-day4/experiments/use-case-4/middleware.py):
- `LLMInputGuardrailMiddleware` — short-circuits on unsafe input (PII/toxic/injection/off-topic), updated refusal message for new domain
- `ExceptionHandlingMiddleware` — catches downstream errors, returns polished message
- `LLMOutputGuardrailMiddleware` — validates agent output post-execution
- `LoggingFunctionMiddleware` — logs tool name, args, duration per call

10–11. **3 Local tools** with `@tool(approval_mode="never_require")`:
- `get_weather(location)` — random conditions + temperature
- `get_current_time(timezone)` — current time via `datetime` + `zoneinfo`
- `get_location_info(city)` — dummy city info (population, country, coordinates)

12–13. **SQLiteHistoryProvider(HistoryProvider)** — creates `conversation_history.db` in notebook directory. Table: `messages(id, session_id, role, content, timestamp)`. `get_messages()` reads by session_id; `save_messages()` inserts new messages.

## Phase 3: Observability (Cell 14)

14. `configure_otel_providers()` — sets up OTLP exporters pointing to Jaeger (`OTEL_EXPORTER_OTLP_ENDPOINT`)

## Phase 4: Agent Construction (Cells 15–18)

15–16. **Classifier setup** — `guardrail_client` created with API key, `classify_fn = partial(classify_text, guardrail_client, model)`, smoke test

17–18. **Agent assembly** inside a tracing root span (`start_as_current_span("E2E Agent", SpanKind.CLIENT)`):
- `OpenAIChatClient` with `AzureCliCredential`
- 2 MCP tools: `MCPStreamableHTTPTool("Microsoft Learn MCP Tool", "https://learn.microsoft.com/api/mcp")` + `MCPStreamableHTTPTool("Orders and Complaints MCP Tool", "http://localhost:8700/mcp")`
- `SQLiteHistoryProvider` instance
- Agent: `tools=[2 MCP + 3 local]`, `middleware=[input guardrail, exception handler, output guardrail, function logger]`, `context_providers=[history_provider]`
- Instructions cover all 5 domains

## Phase 5: Test Scenarios (Cells 19–32)

| # | Scenario | Mode | What it tests |
|---|----------|------|---------------|
| 1 | Get orders for Priya Sharma | `await` | MCP tool, multi-turn start |
| 2 | Register complaint for one of her orders | `await` | MCP write tool, cross-turn context |
| 3 | Get all complaints by Priya Sharma | `await` | MCP read, verify complaint registered |
| 4 | Weather + time + location for Mumbai | `stream=True` | All 3 local tools, **streaming output** |
| 5 | PII message (SSN + credit card) | `await` | Input guardrail BLOCK |
| 6 | Off-topic (chocolate cake recipe) | `await` | Input guardrail BLOCK |
| 7 | Prompt injection (reveal system prompt) | `await` | Input guardrail BLOCK |

## Phase 6: History Verification (Cells 33–35)

| # | Scenario | What it tests |
|---|----------|---------------|
| 8 | Serialize session → new agent → resume → "What orders did we look up?" | Session persistence + SQLite history |
| 9 | Direct SQL query on `conversation_history.db` | Visual proof of stored messages |

---

## Relevant Files

- [end-to-end-scenario.ipynb](use-cases-day4/experiments/end-to-end-scenario.ipynb) — target (currently empty, will be replaced)
- [middleware.py](use-cases-day4/experiments/use-case-4/middleware.py) — reference for all 4 middleware classes
- [classifier.py](use-cases-day4/experiments/use-case-4/classifier.py) — reference for `create_guardrail_client`, `classify_text`
- [prompts.py](use-cases-day4/experiments/use-case-4/prompts.py) — reference for guardrail system prompts (domain scope will change)
- [mcp-multi-tool-agent.ipynb](use-cases-day4/experiments/mcp-multi-tool-agent.ipynb) — reference for MCP tool + session pattern
- [observability.ipynb](use-cases-day4/experiments/observability.ipynb) — reference for tracing + streaming pattern
- [custom_history_provider.ipynb](use-cases-day4/experiments/custom_history_provider.ipynb) — reference for HistoryProvider + session resumption

## Verification

1. Run Scenarios 1–3 → verify MCP order data and complaint creation
2. Run Scenario 4 → verify streaming chunks from all 3 local tools
3. Run Scenarios 5–7 → verify guardrail blocks with category-specific refusals
4. Check logs → `guardrail` logger shows BLOCKED/PASSED/APPROVED, `function` logger shows tool timing
5. Open Jaeger UI (`localhost:16686`) → search by printed Trace ID → verify nested span tree
6. Run Scenarios 8–9 → verify agent recalls conversation after session resumption; confirm SQLite rows

## Decisions

- **Self-contained**: All code inline — no imports from local `.py` files
- **Replace**: Empty `end-to-end-scenario.ipynb` replaced entirely
- **Domain scope**: On-topic = Customer Service, Azure Docs, Weather, Time, Location
- **SQLite path**: `conversation_history.db` in same directory as notebook
- **Client split**: `OpenAIChatClient` + `AzureCliCredential` for agent; `AzureOpenAI` + API key for classifier
- **Middleware order**: Input guardrail → Exception handler → Output guardrail → Function logger
- **Tracing**: All scenarios under one root span for unified Jaeger visualization
