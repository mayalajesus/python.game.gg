from __future__ import annotations

import re
from dataclasses import dataclass


DELIVERY_PATTERN = re.compile(
    r"^/entregar\s+desafio_id:\s*(?P<challenge_id>[\w.-]+)\s+"
    r"Codigo:\s*```python\s*(?P<code>.*?)\s*```\s+"
    r"Explicacao:\s*(?P<explanation>.+)$",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class DeliveryValidationResult:
    is_valid: bool
    challenge_id: str | None = None
    code: str | None = None
    explanation: str | None = None
    message: str = ""


def validate_delivery_format(text: str) -> DeliveryValidationResult:
    match = DELIVERY_PATTERN.match(text.strip())
    if match is None:
        return DeliveryValidationResult(
            is_valid=False,
            message=(
                "Entrega fora do formato. Reenvie usando `/entregar desafio_id: ...`, "
                "um bloco `Codigo:` com ```python e uma `Explicacao:`."
            ),
        )

    code = match.group("code").strip()
    explanation = match.group("explanation").strip()

    if not code:
        return DeliveryValidationResult(is_valid=False, message="O bloco de codigo esta vazio.")
    if len(explanation) < 10:
        return DeliveryValidationResult(
            is_valid=False,
            message="A explicacao esta curta demais. Explique brevemente como a solucao funciona.",
        )

    return DeliveryValidationResult(
        is_valid=True,
        challenge_id=match.group("challenge_id").strip(),
        code=code,
        explanation=explanation,
        message="Formato validado. A entrega pode seguir para correcao.",
    )

