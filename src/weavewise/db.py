from __future__ import annotations

import datetime as dt
from typing import Any

_memory: dict[str, dict[str, Any]] = {}


def create_session(session_id: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    now = dt.datetime.now(dt.UTC)
    doc: dict[str, Any] = {
        "session_id": session_id,
        "created_at": now,
        "updated_at": now,
    }
    if extra:
        doc.update(extra)
    _memory[session_id] = {**doc}
    return doc


def update_session(session_id: str, fields: dict[str, Any]) -> None:
    if session_id not in _memory:
        raise KeyError(session_id)
    now = dt.datetime.now(dt.UTC)
    payload = {**fields, "updated_at": now}
    _memory[session_id].update(payload)


def get_session(session_id: str) -> dict[str, Any] | None:
    mem = _memory.get(session_id)
    return dict(mem) if mem is not None else None


def list_sessions_recent(limit: int = 20) -> list[dict[str, Any]]:
    rows = sorted(_memory.values(), key=lambda d: d["updated_at"], reverse=True)
    return list(rows[:limit])
