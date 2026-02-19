"""
Test script to verify Phase 5 implementation.

Tests:
  1. server.py imports cleanly and exposes expected objects
  2. Configuration loads and validates
  3. Startup logic (DB init + auto-seed) runs without errors
  4. All 6 tools are registered on the FastMCP instance
  5. Live server accepts HTTP connections at /mcp (background thread)
"""

import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# 1. Import verification
# ---------------------------------------------------------------------------

def test_server_imports():
    print("Testing server imports...")
    import server as srv
    from src import app as app_mod
    from src import startup as startup_mod

    assert hasattr(srv, "mcp"),    "server.py must expose 'mcp'"
    assert hasattr(srv, "config"), "server.py must expose 'config'"
    assert hasattr(app_mod, "create_app"),               "src/app.py must expose 'create_app'"
    assert hasattr(startup_mod, "run_startup"),          "src/startup.py must expose 'run_startup'"
    assert hasattr(startup_mod, "register_signal_handlers"), \
        "src/startup.py must expose 'register_signal_handlers'"

    print("  mcp         :", type(srv.mcp).__name__)
    print("  config      :", repr(srv.config))
    print("  create_app  : ✓")
    print("  run_startup : ✓")
    print("✓ Server imports passed")
    return srv


# ---------------------------------------------------------------------------
# 2. Config validation
# ---------------------------------------------------------------------------

def test_config(srv):
    print("\nTesting config...")
    cfg = srv.config

    assert cfg.server_name,        "server_name must not be empty"
    assert 1 <= cfg.port <= 65535, f"port out of range: {cfg.port}"
    assert cfg.mount_path.startswith("/"), "mount_path must start with /"

    print(f"  server_name : {cfg.server_name}")
    print(f"  host:port   : {cfg.host}:{cfg.port}")
    print(f"  mount_path  : {cfg.mount_path}")
    print(f"  auto_seed   : {cfg.auto_seed}")
    print("✓ Config passed")


# ---------------------------------------------------------------------------
# 3. Startup logic
# ---------------------------------------------------------------------------

def test_startup(srv):
    print("\nTesting startup logic (run_startup)...")
    from src.database import get_db, init_database
    from src.models import Complaint
    from src.startup import run_startup

    init_database()
    with get_db() as session:
        session.query(Complaint).delete()
        session.commit()

    # Run startup — should seed the DB
    run_startup()

    # Verify seed ran
    with get_db() as session:
        count = session.query(Complaint).count()

    print(f"  Records in DB after startup: {count}")
    assert count == 20, f"Expected 20 seeded records, got {count}"

    # Run again — must be idempotent
    run_startup()
    with get_db() as session:
        count2 = session.query(Complaint).count()
    assert count2 == 20, f"Idempotency failed: expected 20, got {count2}"
    print("  Idempotency: ✓ (second run_startup() did not duplicate records)")
    print("✓ Startup logic passed")


# ---------------------------------------------------------------------------
# 4. Tool registration
# ---------------------------------------------------------------------------

def test_tool_registration(srv):
    print("\nTesting tool registration on FastMCP instance...")

    expected_tools = {
        "register_complaint",
        "get_complaint",
        "search_complaints",
        "resolve_complaint",
        "update_complaint",
        "archive_complaint",
    }

    # FastMCP stores tools in ._tool_manager._tools (dict keyed by tool name)
    registered = set(srv.mcp._tool_manager._tools.keys())
    print(f"  Registered tools: {sorted(registered)}")

    missing = expected_tools - registered
    assert not missing, f"Missing tools on FastMCP instance: {missing}"

    extra = registered - expected_tools
    if extra:
        print(f"  Note: extra tools registered: {extra}")

    print(f"  All {len(expected_tools)} expected tools are registered.")
    print("✓ Tool registration passed")


# ---------------------------------------------------------------------------
# 5. Live server smoke test
# ---------------------------------------------------------------------------

def test_live_server(srv):
    """Start the server in a daemon thread and verify it responds over HTTP."""
    print("\nTesting live server (smoke test)...")

    import os
    # Use a non-clashing test port to avoid conflicts
    TEST_PORT = 18321
    os.environ["MCP_SERVER_PORT"] = str(TEST_PORT)

    # Reset config singleton so it picks up the new port
    import src.config as cfg_mod
    cfg_mod._config = None
    srv.config = cfg_mod.load_config()
    srv.mcp.settings.port = TEST_PORT

    errors: list[str] = []

    def _run():
        try:
            srv.mcp.run(transport="streamable-http", mount_path=srv.config.mount_path)
        except SystemExit:
            pass
        except Exception as exc:
            errors.append(str(exc))

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    # Give uvicorn a moment to bind
    time.sleep(2.5)

    url = f"http://127.0.0.1:{TEST_PORT}{srv.config.mount_path}"
    print(f"  Probing: POST {url}")

    # MCP Streamable-HTTP requires a POST with a JSON-RPC body.
    # We send a minimal initialize request and expect a 200 (or 4xx that proves
    # the server is alive — not a ConnectionRefused).
    payload = (
        b'{"jsonrpc":"2.0","id":1,'
        b'"method":"initialize",'
        b'"params":{"protocolVersion":"2024-11-05",'
        b'"capabilities":{},'
        b'"clientInfo":{"name":"test","version":"0"}}}'
    )
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body = resp.read(500).decode("utf-8", errors="replace")
            print(f"  HTTP {status} — body[:200]: {body[:200]}")
            assert status == 200, f"Expected HTTP 200, got {status}"
    except urllib.error.HTTPError as exc:
        # Any HTTP error (4xx/5xx) still means the server is up
        print(f"  HTTP {exc.code} — server is running (non-200 is acceptable for init probe)")
        assert exc.code < 500, f"Server returned a 5xx error: {exc.code}"
    except urllib.error.URLError as exc:
        assert False, f"Could not connect to server at {url}: {exc.reason}"

    if errors:
        assert False, f"Server thread raised: {errors[0]}"

    print("✓ Live server smoke test passed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Phase 5: Server Setup & Integration - Verification Tests")
    print("=" * 60)

    try:
        srv = test_server_imports()
        test_config(srv)
        test_startup(srv)
        test_tool_registration(srv)
        test_live_server(srv)

        print("\n" + "=" * 60)
        print("✅ Phase 5: Server Setup & Integration - ALL TESTS PASSED")
        print("=" * 60)
        print("\nServer Components Ready:")
        print("  ✓ server.py — clean imports, correct structure")
        print("  ✓ Config — loaded and validated")
        print("  ✓ Startup — DB init + auto-seed (idempotent)")
        print("  ✓ Tool registration — all 6 tools on FastMCP")
        print("  ✓ Live server — Streamable-HTTP responding")
        print("\nReady for Phase 6: Testing & Documentation")

    except AssertionError as exc:
        print(f"\n❌ Assertion failed: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as exc:
        print(f"\n❌ Unexpected error: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
