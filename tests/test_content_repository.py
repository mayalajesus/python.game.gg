from __future__ import annotations

from pathlib import Path

from python_game.content_repository import ContentRepository, format_recommendations
from python_game.database import GameDatabase
from python_game.delivery_validation import validate_delivery_format
from python_game.evaluator import evaluate_submission


ROOT = Path(__file__).resolve().parents[1]


def test_loads_content_index() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")

    contents = repository.list_contents()

    assert len(contents) >= 30
    assert contents[0]["id"] == "ambiente_desenvolvimento"


def test_loads_single_content() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")

    content = repository.get_content("variaveis_baus_memoria")

    assert content.title == "Variaveis - Baus de Memoria"
    assert "variaveis" in content.raw["conceitos"]


def test_empty_recommendations_do_not_announce_missing_materials() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")
    content = repository.get_content("variaveis_baus_memoria")

    message = format_recommendations(content)

    assert "Ainda nao existem" not in message
    assert "Nenhum link" not in message


def test_content_files_do_not_expose_extra_manual_fields() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")
    forbidden_fields = {
        "bot",
        "observacoes_internas",
    }
    forbidden_nested_fields = {
        "validacao": {"criterios_manuais"},
        "status": {"revisado", "links_adicionados"},
    }

    for item in repository.list_contents():
        content = repository.get_content(item["id"])

        assert forbidden_fields.isdisjoint(content.raw.keys())
        for parent, fields in forbidden_nested_fields.items():
            assert fields.isdisjoint(content.raw.get(parent, {}).keys())


def test_validates_expected_delivery_format() -> None:
    result = validate_delivery_format(
        """/entregar desafio_id: fundamentos_01

Codigo:
```python
print("ola guilda")
```

Explicacao:
Este codigo imprime uma mensagem inicial no terminal.
"""
    )

    assert result.is_valid is True
    assert result.challenge_id == "fundamentos_01"


def test_rejects_delivery_without_required_format() -> None:
    result = validate_delivery_format("segue meu codigo: print('oi')")

    assert result.is_valid is False


def test_evaluator_accepts_valid_intro_solution() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")
    content = repository.get_content("print_primeiro_script")

    result = evaluate_submission(
        content,
        'print("Bem-vindo a Guilda")\nprint("Missao iniciada")\nprint("Fim")',
        "O codigo imprime tres mensagens no terminal para criar um banner simples.",
    )

    assert result.accepted is True
    assert result.score >= 70


def test_database_records_player_submission_and_ranking(tmp_path: Path) -> None:
    database = GameDatabase(tmp_path / "game.sqlite3")
    player = database.upsert_player(
        discord_id=1,
        guild_id=10,
        display_name="Mayala",
        hero_name="Maga dos Dados",
        rank_role="🥚 Novato",
        active_content_id="print_primeiro_script",
    )

    assert player.xp == 0

    submission = database.record_submission(
        discord_id=1,
        guild_id=10,
        content_id="print_primeiro_script",
        code='print("ola")',
        explanation="Imprime uma mensagem simples.",
        repository_url=None,
        score=85,
        accepted=True,
        feedback="Aprovada",
    )
    updated = database.add_xp(
        discord_id=1,
        guild_id=10,
        amount=100,
        reason="Missao concluida",
        content_id="print_primeiro_script",
        rank_role="🥚 Novato",
    )

    assert submission.first_completion is True
    assert updated.xp == 100
    assert database.leaderboard(10)[0].hero_name == "Maga dos Dados"


def test_database_records_moderation_events(tmp_path: Path) -> None:
    database = GameDatabase(tmp_path / "game.sqlite3")

    database.add_moderation_event(
        guild_id=10,
        discord_id=1,
        action="spam",
        reason="Muitas mensagens em poucos segundos.",
        message_excerpt="mensagem repetida",
    )

    events = database.moderation_events_for_user(10, 1)

    assert database.moderation_event_count(10, 1) == 1
    assert events[0]["action"] == "spam"
    assert events[0]["reason"] == "Muitas mensagens em poucos segundos."
