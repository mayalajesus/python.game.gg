from __future__ import annotations

from pathlib import Path

from python_game.content_repository import ContentRepository
from python_game.delivery_validation import validate_delivery_format


ROOT = Path(__file__).resolve().parents[1]


def test_loads_content_index() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")

    contents = repository.list_contents()

    assert len(contents) >= 30
    assert contents[0]["id"] == "onboarding_entrada_guilda"


def test_loads_single_content() -> None:
    repository = ContentRepository(ROOT / "conteudos" / "index-conteudos.json")

    content = repository.get_content("variaveis_baus_memoria")

    assert content.title == "Variaveis - Baus de Memoria"
    assert "variaveis" in content.raw["conceitos"]


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
