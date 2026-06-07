from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def utcnow() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Player:
    discord_id: int
    guild_id: int
    display_name: str
    hero_name: str
    xp: int
    level: int
    rank_role: str
    active_content_id: str | None
    onboarded_at: str


@dataclass(frozen=True)
class SubmissionResult:
    accepted: bool
    first_completion: bool
    xp_awarded: int


class ManagedConnection(sqlite3.Connection):
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        result = super().__exit__(exc_type, exc_value, traceback)
        self.close()
        return result


class GameDatabase:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, factory=ManagedConnection)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS players (
                    discord_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    display_name TEXT NOT NULL,
                    hero_name TEXT NOT NULL,
                    xp INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1,
                    rank_role TEXT NOT NULL,
                    active_content_id TEXT,
                    onboarded_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (discord_id, guild_id)
                );

                CREATE TABLE IF NOT EXISTS xp_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    content_id TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS content_progress (
                    discord_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    content_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    best_score INTEGER NOT NULL DEFAULT 0,
                    completed_at TEXT,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (discord_id, guild_id, content_id)
                );

                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    content_id TEXT NOT NULL,
                    code TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    repository_url TEXT,
                    score INTEGER NOT NULL,
                    accepted INTEGER NOT NULL,
                    feedback TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    content_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    repository_url TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id INTEGER PRIMARY KEY,
                    setup_completed_at TEXT,
                    announcements_channel_id INTEGER,
                    trail_channel_id INTEGER,
                    deliveries_channel_id INTEGER,
                    ranking_channel_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS moderation_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    discord_id INTEGER NOT NULL,
                    moderator_id INTEGER,
                    action TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    message_excerpt TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )

    def upsert_player(
        self,
        *,
        discord_id: int,
        guild_id: int,
        display_name: str,
        hero_name: str,
        rank_role: str,
        active_content_id: str | None,
    ) -> Player:
        now = utcnow()
        with self.connect() as connection:
            existing = self.get_player(discord_id, guild_id)
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO players (
                        discord_id, guild_id, display_name, hero_name, xp, level, rank_role,
                        active_content_id, onboarded_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, 0, 1, ?, ?, ?, ?)
                    """,
                    (
                        discord_id,
                        guild_id,
                        display_name,
                        hero_name,
                        rank_role,
                        active_content_id,
                        now,
                        now,
                    ),
                )
            else:
                connection.execute(
                    """
                    UPDATE players
                    SET display_name = ?, hero_name = ?, active_content_id = COALESCE(active_content_id, ?),
                        updated_at = ?
                    WHERE discord_id = ? AND guild_id = ?
                    """,
                    (display_name, hero_name, active_content_id, now, discord_id, guild_id),
                )
        return self.get_player_or_raise(discord_id, guild_id)

    def get_player(self, discord_id: int, guild_id: int) -> Player | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM players WHERE discord_id = ? AND guild_id = ?",
                (discord_id, guild_id),
            ).fetchone()
        if row is None:
            return None
        return self._player_from_row(row)

    def get_player_or_raise(self, discord_id: int, guild_id: int) -> Player:
        player = self.get_player(discord_id, guild_id)
        if player is None:
            raise KeyError(f"Player nao encontrado: {discord_id}/{guild_id}")
        return player

    def set_active_content(self, discord_id: int, guild_id: int, content_id: str) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE players
                SET active_content_id = ?, updated_at = ?
                WHERE discord_id = ? AND guild_id = ?
                """,
                (content_id, utcnow(), discord_id, guild_id),
            )

    def add_xp(
        self,
        *,
        discord_id: int,
        guild_id: int,
        amount: int,
        reason: str,
        content_id: str | None = None,
        rank_role: str | None = None,
    ) -> Player:
        now = utcnow()
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO xp_events (discord_id, guild_id, amount, reason, content_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (discord_id, guild_id, amount, reason, content_id, now),
            )
            player = connection.execute(
                "SELECT xp FROM players WHERE discord_id = ? AND guild_id = ?",
                (discord_id, guild_id),
            ).fetchone()
            if player is None:
                raise KeyError(f"Player nao encontrado: {discord_id}/{guild_id}")
            new_xp = int(player["xp"]) + amount
            new_level = max(1, new_xp // 300 + 1)
            connection.execute(
                """
                UPDATE players
                SET xp = ?, level = ?, rank_role = COALESCE(?, rank_role), updated_at = ?
                WHERE discord_id = ? AND guild_id = ?
                """,
                (new_xp, new_level, rank_role, now, discord_id, guild_id),
            )
        return self.get_player_or_raise(discord_id, guild_id)

    def record_submission(
        self,
        *,
        discord_id: int,
        guild_id: int,
        content_id: str,
        code: str,
        explanation: str,
        repository_url: str | None,
        score: int,
        accepted: bool,
        feedback: str,
    ) -> SubmissionResult:
        now = utcnow()
        with self.connect() as connection:
            progress = connection.execute(
                """
                SELECT status, attempts, best_score, completed_at
                FROM content_progress
                WHERE discord_id = ? AND guild_id = ? AND content_id = ?
                """,
                (discord_id, guild_id, content_id),
            ).fetchone()
            first_completion = accepted and (progress is None or progress["status"] != "completed")
            attempts = 1 if progress is None else int(progress["attempts"]) + 1
            best_score = max(score, 0 if progress is None else int(progress["best_score"]))
            status = "completed" if accepted or (progress and progress["status"] == "completed") else "needs_revision"
            completed_at = now if first_completion else (progress["completed_at"] if progress and "completed_at" in progress.keys() else None)

            connection.execute(
                """
                INSERT INTO submissions (
                    discord_id, guild_id, content_id, code, explanation, repository_url,
                    score, accepted, feedback, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    discord_id,
                    guild_id,
                    content_id,
                    code,
                    explanation,
                    repository_url,
                    score,
                    int(accepted),
                    feedback,
                    now,
                ),
            )
            connection.execute(
                """
                INSERT INTO content_progress (
                    discord_id, guild_id, content_id, status, attempts, best_score, completed_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(discord_id, guild_id, content_id)
                DO UPDATE SET status = excluded.status, attempts = excluded.attempts,
                    best_score = excluded.best_score,
                    completed_at = COALESCE(content_progress.completed_at, excluded.completed_at),
                    updated_at = excluded.updated_at
                """,
                (discord_id, guild_id, content_id, status, attempts, best_score, completed_at, now),
            )
        return SubmissionResult(accepted=accepted, first_completion=first_completion, xp_awarded=0)

    def add_project(
        self,
        *,
        discord_id: int,
        guild_id: int,
        content_id: str,
        title: str,
        repository_url: str,
        description: str,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO projects (discord_id, guild_id, content_id, title, repository_url, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (discord_id, guild_id, content_id, title, repository_url, description, utcnow()),
            )

    def leaderboard(self, guild_id: int, limit: int = 10) -> list[Player]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM players
                WHERE guild_id = ?
                ORDER BY xp DESC, updated_at ASC
                LIMIT ?
                """,
                (guild_id, limit),
            ).fetchall()
        return [self._player_from_row(row) for row in rows]

    def portfolio(self, discord_id: int, guild_id: int) -> list[sqlite3.Row]:
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT * FROM projects
                WHERE discord_id = ? AND guild_id = ?
                ORDER BY created_at DESC
                """,
                (discord_id, guild_id),
            ).fetchall()

    def stats(self, discord_id: int, guild_id: int) -> dict[str, Any]:
        with self.connect() as connection:
            completed = connection.execute(
                """
                SELECT COUNT(*) AS total FROM content_progress
                WHERE discord_id = ? AND guild_id = ? AND status = 'completed'
                """,
                (discord_id, guild_id),
            ).fetchone()["total"]
            attempts = connection.execute(
                """
                SELECT COUNT(*) AS total FROM submissions
                WHERE discord_id = ? AND guild_id = ?
                """,
                (discord_id, guild_id),
            ).fetchone()["total"]
            projects = connection.execute(
                """
                SELECT COUNT(*) AS total FROM projects
                WHERE discord_id = ? AND guild_id = ?
                """,
                (discord_id, guild_id),
            ).fetchone()["total"]
        return {"completed": completed, "attempts": attempts, "projects": projects}

    def save_guild_setup(self, guild_id: int, channels: dict[str, int]) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO guild_settings (
                    guild_id, setup_completed_at, announcements_channel_id, trail_channel_id,
                    deliveries_channel_id, ranking_channel_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(guild_id)
                DO UPDATE SET setup_completed_at = excluded.setup_completed_at,
                    announcements_channel_id = excluded.announcements_channel_id,
                    trail_channel_id = excluded.trail_channel_id,
                    deliveries_channel_id = excluded.deliveries_channel_id,
                    ranking_channel_id = excluded.ranking_channel_id
                """,
                (
                    guild_id,
                    utcnow(),
                    channels.get("announcements"),
                    channels.get("trail"),
                    channels.get("deliveries"),
                    channels.get("ranking"),
                ),
            )

    def add_moderation_event(
        self,
        *,
        guild_id: int,
        discord_id: int,
        action: str,
        reason: str,
        moderator_id: int | None = None,
        message_excerpt: str | None = None,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO moderation_events (
                    guild_id, discord_id, moderator_id, action, reason, message_excerpt, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    guild_id,
                    discord_id,
                    moderator_id,
                    action,
                    reason,
                    (message_excerpt or "")[:240],
                    utcnow(),
                ),
            )

    def moderation_events_for_user(self, guild_id: int, discord_id: int, limit: int = 10) -> list[sqlite3.Row]:
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT * FROM moderation_events
                WHERE guild_id = ? AND discord_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (guild_id, discord_id, limit),
            ).fetchall()

    def moderation_event_count(self, guild_id: int, discord_id: int, action: str | None = None) -> int:
        with self.connect() as connection:
            if action:
                row = connection.execute(
                    """
                    SELECT COUNT(*) AS total FROM moderation_events
                    WHERE guild_id = ? AND discord_id = ? AND action = ?
                    """,
                    (guild_id, discord_id, action),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT COUNT(*) AS total FROM moderation_events
                    WHERE guild_id = ? AND discord_id = ?
                    """,
                    (guild_id, discord_id),
                ).fetchone()
        return int(row["total"])

    @staticmethod
    def _player_from_row(row: sqlite3.Row) -> Player:
        return Player(
            discord_id=int(row["discord_id"]),
            guild_id=int(row["guild_id"]),
            display_name=row["display_name"],
            hero_name=row["hero_name"],
            xp=int(row["xp"]),
            level=int(row["level"]),
            rank_role=row["rank_role"],
            active_content_id=row["active_content_id"],
            onboarded_at=row["onboarded_at"],
        )
