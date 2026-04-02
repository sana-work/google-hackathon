"""SQLite-backed persistence for guardrail runs and default configuration."""

from __future__ import annotations

import json
import sqlite3
import time
from copy import deepcopy
from pathlib import Path


def _now_epoch() -> float:
    return time.time()


class RunStore:
    """Persist default config and per-run snapshots in SQLite."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS app_config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    parent_run_id TEXT,
                    status TEXT NOT NULL,
                    stage INTEGER NOT NULL,
                    active_stage INTEGER NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    run_json TEXT NOT NULL
                );
                """
            )

    def _read_json_config(self, key: str, default):
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM app_config WHERE key = ?", (key,)).fetchone()
        if not row:
            return deepcopy(default)
        return json.loads(row["value"])

    def _write_json_config(self, key: str, value) -> None:
        encoded = json.dumps(value)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO app_config (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, encoded),
            )

    def get_default_config(self, defaults: dict) -> dict:
        return self._read_json_config("default_config", defaults)

    def save_default_config(self, config: dict) -> dict:
        self._write_json_config("default_config", config)
        return deepcopy(config)

    def get_current_run_id(self) -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM app_config WHERE key = ?", ("current_run_id",)).fetchone()
        return row["value"] if row else None

    def set_current_run_id(self, run_id: str | None) -> None:
        with self._connect() as conn:
            if run_id is None:
                conn.execute("DELETE FROM app_config WHERE key = ?", ("current_run_id",))
            else:
                conn.execute(
                    """
                    INSERT INTO app_config (key, value)
                    VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                    """,
                    ("current_run_id", run_id),
                )

    def create_run(self, run: dict) -> dict:
        record = deepcopy(run)
        now = _now_epoch()
        if record.get("created_at") is None:
            record["created_at"] = now
        record["updated_at"] = now

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (id, parent_run_id, status, stage, active_stage, created_at, updated_at, run_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["run_id"],
                    record.get("parent_run_id"),
                    record.get("status", "idle"),
                    int(record.get("stage", 0)),
                    int(record.get("active_stage", 0)),
                    float(record["created_at"]),
                    float(record["updated_at"]),
                    json.dumps(record),
                ),
            )
        self.set_current_run_id(record["run_id"])
        return record

    def get_run(self, run_id: str | None) -> dict | None:
        if not run_id:
            return None
        with self._connect() as conn:
            row = conn.execute("SELECT run_json FROM runs WHERE id = ?", (run_id,)).fetchone()
        if not row:
            return None
        return json.loads(row["run_json"])

    def get_current_run(self) -> dict | None:
        return self.get_run(self.get_current_run_id())

    def update_run(self, run_id: str, patch: dict) -> dict:
        current = self.get_run(run_id)
        if current is None:
            raise KeyError(f"Run {run_id} not found")

        current.update(deepcopy(patch))
        current["updated_at"] = _now_epoch()

        with self._connect() as conn:
            conn.execute(
                """
                UPDATE runs
                SET parent_run_id = ?, status = ?, stage = ?, active_stage = ?, updated_at = ?, run_json = ?
                WHERE id = ?
                """,
                (
                    current.get("parent_run_id"),
                    current.get("status", "idle"),
                    int(current.get("stage", 0)),
                    int(current.get("active_stage", 0)),
                    float(current["updated_at"]),
                    json.dumps(current),
                    run_id,
                ),
            )
        return current

    def replace_run(self, run_id: str, run: dict) -> dict:
        record = deepcopy(run)
        record["updated_at"] = _now_epoch()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE runs
                SET parent_run_id = ?, status = ?, stage = ?, active_stage = ?, updated_at = ?, run_json = ?
                WHERE id = ?
                """,
                (
                    record.get("parent_run_id"),
                    record.get("status", "idle"),
                    int(record.get("stage", 0)),
                    int(record.get("active_stage", 0)),
                    float(record["updated_at"]),
                    json.dumps(record),
                    run_id,
                ),
            )
        return record

    def list_runs(self, limit: int = 25) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT run_json FROM runs ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [json.loads(row["run_json"]) for row in rows]
