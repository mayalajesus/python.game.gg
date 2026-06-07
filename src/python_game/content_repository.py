from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TrailContent:
    id: str
    title: str
    module: str
    week: int
    order: int
    objective: str
    recommendations: dict[str, list[str]]
    raw: dict[str, Any]


class ContentRepository:
    def __init__(self, index_path: Path) -> None:
        self.index_path = index_path
        self.base_dir = index_path.parent
        self._index = self._load_index()

    def list_contents(self) -> list[dict[str, Any]]:
        return list(self._index["conteudos"])

    def first_content_id(self) -> str:
        return self.list_contents()[0]["id"]

    def has_content(self, content_id: str | None) -> bool:
        if not content_id:
            return False
        return any(content["id"] == content_id for content in self._index["conteudos"])

    def safe_content_id(self, content_id: str | None) -> str:
        return content_id if self.has_content(content_id) else self.first_content_id()

    def next_content_id(self, current_content_id: str) -> str | None:
        contents = self.list_contents()
        for index, item in enumerate(contents):
            if item["id"] == current_content_id:
                if index + 1 >= len(contents):
                    return None
                return contents[index + 1]["id"]
        return None

    def get_content(self, content_id: str) -> TrailContent:
        item = next(
            (content for content in self._index["conteudos"] if content["id"] == content_id),
            None,
        )
        if item is None:
            raise KeyError(f"Conteudo nao encontrado: {content_id}")

        content_path = self.base_dir / item["arquivo"]
        data = self._read_json(content_path)

        return TrailContent(
            id=data["id"],
            title=data["titulo"],
            module=data["modulo"],
            week=int(data["semana"]),
            order=int(data["ordem"]),
            objective=data["objetivo"],
            recommendations=data.get("recomendacoes", {}),
            raw=data,
        )

    def _load_index(self) -> dict[str, Any]:
        if not self.index_path.exists():
            raise FileNotFoundError(f"Indice de conteudos nao encontrado: {self.index_path}")
        return self._read_json(self.index_path)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)


def format_recommendations(content: TrailContent) -> str:
    lines = [
        f"📚 Biblioteca da missao: {content.title}",
        f"🎯 Objetivo de campo: {content.objective}",
        "",
    ]

    labels = {
        "pdfs": "📄 PDFs",
        "videos": "🎥 Videos",
        "artigos": "📰 Artigos",
        "sites_oficiais": "🏛️ Sites oficiais",
        "documentacao": "📚 Documentacao",
        "cursos": "🎓 Cursos",
        "repositorios": "💻 Repositorios",
        "ferramentas": "🧰 Ferramentas",
        "outros": "✨ Outros",
    }

    has_links = False
    for key, label in labels.items():
        links = content.recommendations.get(key, [])
        if not links:
            continue
        has_links = True
        lines.append(label)
        lines.extend(f"- {link}" for link in links)
        lines.append("")

    return "\n".join(lines).strip()


def compact_recommendations(content: TrailContent, limit: int = 5) -> tuple[str, ...]:
    labels = {
        "ferramentas": "🧰 Ferramenta",
        "documentacao": "📚 Documentacao",
        "sites_oficiais": "🏛️ Site oficial",
        "videos": "🎥 Video",
        "artigos": "📰 Artigo",
        "pdfs": "📄 PDF",
        "cursos": "🎓 Curso",
        "repositorios": "💻 Repositorio",
        "outros": "✨ Apoio",
    }
    lines: list[str] = []
    for key, label in labels.items():
        for item in content.recommendations.get(key, []):
            lines.append(f"{label}: {item}")
            if len(lines) >= limit:
                return tuple(lines)
    return tuple(lines)


def primary_recommendation(content: TrailContent) -> str | None:
    recommendations = compact_recommendations(content, limit=1)
    return recommendations[0] if recommendations else None


def has_recommendation_links(content: TrailContent) -> bool:
    return any(bool(links) for links in content.recommendations.values())
