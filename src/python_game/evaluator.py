from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any

from python_game.content_repository import TrailContent


@dataclass(frozen=True)
class Evaluation:
    accepted: bool
    score: int
    feedback: str
    strengths: tuple[str, ...]
    improvements: tuple[str, ...]


CONCEPT_HINTS: dict[str, tuple[str, ...]] = {
    "terminal": ("mkdir", "cd", "dir", "ls", "pwd"),
    "print": ("print(",),
    "comentarios": ("#", '"""', "'''"),
    "variaveis": ("=",),
    "str": ('"', "'"),
    "int": ("int(",),
    "float": ("float(",),
    "type": ("type(",),
    "input": ("input(",),
    "casting": ("int(", "float(", "str("),
    "bool": ("True", "False", "==", "!=", ">=", "<="),
    "and": (" and ",),
    "or": (" or ",),
    "not": (" not ",),
    "if": ("if ",),
    "else": ("else:",),
    "elif": ("elif ",),
    "while": ("while ",),
    "for": ("for ",),
    "range": ("range(",),
    "listas": ("[", ".append(", ".remove("),
    "tuplas": ("(", ","),
    "dicionarios": ("{", ":"),
    "def": ("def ",),
    "return": ("return ",),
    "try": ("try:",),
    "except": ("except",),
    "import": ("import ", "from "),
    "csv": ("csv",),
    "json": ("json",),
    "requests": ("requests",),
    "classe": ("class ",),
    "pytest": ("assert ", "pytest"),
    "sql": ("SELECT", "sqlite", "sql"),
    "pandas": ("pandas", "DataFrame", "pd."),
    "etl": ("extract", "transform", "load"),
}


def evaluate_submission(content: TrailContent, code: str, explanation: str) -> Evaluation:
    strengths: list[str] = []
    improvements: list[str] = []
    score = 35

    expects_python = _expects_python_code(content.raw.get("conceitos", []))
    syntax_ok = _syntax_is_valid(code) if expects_python else bool(code.strip())
    if syntax_ok:
        score += 20
        if expects_python:
            strengths.append("O codigo possui sintaxe Python valida.")
        else:
            strengths.append("A solucao tecnica possui conteudo suficiente para a missao.")
    else:
        improvements.append("Revise a sintaxe ou inclua uma solucao tecnica verificavel.")

    if len(code.splitlines()) >= 3:
        score += 10
        strengths.append("A solucao tem corpo suficiente para ser analisada.")
    else:
        improvements.append("A solucao parece curta demais para uma missao pratica.")

    concept_score, missing = _concept_score(content.raw.get("conceitos", []), code)
    score += concept_score
    if concept_score >= 15:
        strengths.append("A solucao usa sinais dos conceitos pedidos na trilha.")
    if missing:
        improvements.append("Reforce estes conceitos no codigo: " + ", ".join(missing[:4]) + ".")

    if len(explanation) >= 40:
        score += 10
        strengths.append("A explicacao ajuda a entender sua estrategia.")
    else:
        improvements.append("Explique com mais clareza o que o codigo faz e por que funciona.")

    if expects_python:
        if _has_readable_names(code):
            score += 10
            strengths.append("Os nomes usados no codigo parecem legiveis.")
        else:
            improvements.append("Use nomes em snake_case que descrevam melhor os dados.")
    else:
        score += 10
        strengths.append("A entrega esta alinhada a uma missao tecnica nao-Python.")

    score = max(0, min(score, 100))
    accepted = syntax_ok and score >= 70

    if accepted:
        feedback = "Missao aprovada. A Guilda registrou seu progresso."
    else:
        feedback = "Missao ainda nao aprovada. Ajuste os pontos abaixo e reenvie."

    return Evaluation(
        accepted=accepted,
        score=score,
        feedback=feedback,
        strengths=tuple(strengths),
        improvements=tuple(improvements or ("Continue refinando a organizacao da solucao.",)),
    )


def _syntax_is_valid(code: str) -> bool:
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True


def _expects_python_code(concepts: list[Any]) -> bool:
    non_python_markers = {
        "terminal",
        "instalacao",
        "vscode",
        "path",
        "git",
        "github",
        "sql",
        "docker",
        "dockerfile",
        "env",
        "cli",
        "agendamento",
        "orquestracao",
    }
    normalized = {str(concept).lower() for concept in concepts}
    if normalized & non_python_markers:
        return False
    return True


def _concept_score(concepts: list[Any], code: str) -> tuple[int, list[str]]:
    normalized_code = code.lower()
    matched = 0
    missing: list[str] = []
    relevant = 0

    for raw_concept in concepts:
        concept = str(raw_concept).lower()
        hints = CONCEPT_HINTS.get(concept)
        if not hints:
            continue
        relevant += 1
        if any(hint.lower() in normalized_code for hint in hints):
            matched += 1
        else:
            missing.append(concept)

    if relevant == 0:
        return 15, []
    return int(20 * (matched / relevant)), missing


def _has_readable_names(code: str) -> bool:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False

    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    custom_names = [name for name in names if not name.startswith("_") and name not in {"print", "input"}]
    if not custom_names:
        return True
    return any("_" in name or len(name) >= 4 for name in custom_names)
