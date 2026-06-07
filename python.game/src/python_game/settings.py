from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    discord_token: str
    command_prefix: str
    content_index_path: Path


def load_settings() -> Settings:
    project_dir = Path(__file__).resolve().parents[2]
    workspace_dir = project_dir.parent

    load_dotenv(workspace_dir / ".env")
    load_dotenv(project_dir / ".env", override=False)

    raw_index_path = os.getenv("CONTENT_INDEX_PATH", "../conteudos/index-conteudos.json")
    content_index_path = Path(raw_index_path)
    if not content_index_path.is_absolute():
        content_index_path = project_dir / content_index_path

    return Settings(
        discord_token=os.getenv("DISCORD_TOKEN", ""),
        command_prefix=os.getenv("COMMAND_PREFIX", "!"),
        content_index_path=content_index_path.resolve(),
    )

