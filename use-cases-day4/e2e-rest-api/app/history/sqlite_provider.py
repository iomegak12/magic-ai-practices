"""SQLite-backed conversation history provider."""

import sqlite3
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_framework import HistoryProvider, Message


class SQLiteHistoryProvider(HistoryProvider):
    """Persists conversation messages to a local SQLite database."""

    def __init__(self, db_path: str | Path) -> None:
        super().__init__("sqlite-history")
        self.db_path = str(db_path)
        self._init_db()

    def _init_db(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()

    async def get_messages(
        self,
        session_id: str | None,
        *,
        state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[Message]:
        key = session_id or "default"
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id",
                (key,),
            ).fetchall()
        return [Message(role=role, contents=[content]) for role, content in rows]

    async def save_messages(
        self,
        session_id: str | None,
        messages: Sequence[Message],
        *,
        state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        key = session_id or "default"
        now = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            for msg in messages:
                content = msg.text or ""
                conn.execute(
                    "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                    (key, msg.role, content, now),
                )
            conn.commit()
