"""SQLite database connection, schema bootstrap, and sequence helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from magic_v22_mcp.config import get_settings

_SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS _meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date    TEXT    NOT NULL,
    customer_name TEXT    NOT NULL,
    order_number  TEXT    NOT NULL UNIQUE,
    product_sku   TEXT    NOT NULL,
    units         INTEGER NOT NULL CHECK(units > 0),
    order_amount  INTEGER NOT NULL CHECK(order_amount >= 0),
    remarks       TEXT    NOT NULL DEFAULT '',
    status        TEXT    NOT NULL DEFAULT 'PENDING'
);

CREATE TABLE IF NOT EXISTS complaints (
    complaint_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_date        TEXT    NOT NULL,
    order_id              INTEGER NOT NULL REFERENCES orders(order_id),
    registered_by         TEXT    NOT NULL,
    complaint_description TEXT    NOT NULL,
    priority              TEXT    NOT NULL,
    status                TEXT    NOT NULL DEFAULT 'OPEN',
    resolved_by           TEXT,
    resolution_remarks    TEXT
);
"""

_ORD_SEQUENCE_KEY = "ord_next_seq"
_ORD_START = 10001


def _db_path() -> Path:
    p = Path(get_settings().db_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def get_conn() -> sqlite3.Connection:
    """Return a new SQLite connection with row factory and FK enforcement."""
    conn = sqlite3.connect(str(_db_path()), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create tables and initialize the order-number sequence if needed."""
    with get_conn() as conn:
        conn.executescript(_SCHEMA_SQL)
        existing = conn.execute(
            "SELECT value FROM _meta WHERE key=?", (_ORD_SEQUENCE_KEY,)
        ).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO _meta(key, value) VALUES(?, ?)",
                (_ORD_SEQUENCE_KEY, str(_ORD_START)),
            )
            conn.commit()


def next_order_number() -> str:
    """Atomically read-and-increment the ORD sequence; return e.g. 'ORD10001'."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT value FROM _meta WHERE key=?", (_ORD_SEQUENCE_KEY,)
        ).fetchone()
        seq = int(row["value"])
        conn.execute(
            "UPDATE _meta SET value=? WHERE key=?",
            (str(seq + 1), _ORD_SEQUENCE_KEY),
        )
        conn.commit()
    return f"ORD{seq:05d}"
