from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rank:
    role_name: str
    title: str
    min_xp: int
    emoji: str
    flavor: str


RANKS: tuple[Rank, ...] = (
    Rank("🥚 Novato", "Novato", 0, "🥚", "Acabou de entrar na Guilda e esta preparando o equipamento."),
    Rank("⚔️ Aventureiro", "Aventureiro", 300, "⚔️", "Ja venceu as primeiras missoes e entende a base da jornada."),
    Rank("🛡️ Caçador de Bugs", "Cacador de Bugs", 900, "🛡️", "Comeca a depurar erros e pensar como programador."),
    Rank("🔮 Mago das Funções", "Mago das Funcoes", 1600, "🔮", "Transforma codigo repetido em feiticos reutilizaveis."),
    Rank("📚 Guardião dos Dados", "Guardiao dos Dados", 2600, "📚", "Domina arquivos, registros e dados estruturados."),
    Rank("🏰 Arquiteto de Classes", "Arquiteto de Classes", 3800, "🏰", "Organiza sistemas com objetos, testes e boas praticas."),
    Rank("🌐 Invocador de APIs", "Invocador de APIs", 5200, "🌐", "Abre portais externos e coleta dados do mundo real."),
    Rank("📊 Analista Arcano", "Analista Arcano", 6800, "📊", "Transforma dados em relatorios, metricas e historias."),
    Rank("⚙️ Engenheiro da Guilda", "Engenheiro da Guilda", 8400, "⚙️", "Constrói pipelines, bancos e automacoes consistentes."),
    Rank("👑 Mestre dos Dados", "Mestre dos Dados", 10500, "👑", "Concluiu a jornada e possui portfolio de Engenharia de Dados."),
)


def rank_for_xp(xp: int) -> Rank:
    current = RANKS[0]
    for rank in RANKS:
        if xp >= rank.min_xp:
            current = rank
    return current


def next_rank_for_xp(xp: int) -> Rank | None:
    for rank in RANKS:
        if xp < rank.min_xp:
            return rank
    return None

