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
    Rank("🥚 Novato", "Novato", 0, "🥚", "Acendeu a primeira marca no mapa e entrou no ritmo da Guilda."),
    Rank("⚔️ Aventureiro", "Aventureiro", 300, "⚔️", "Ja transformou estudo em entrega e comecou a criar historico."),
    Rank("🛡️ Caçador de Bugs", "Cacador de Bugs", 900, "🛡️", "Aprende a ler erros, ajustar rotas e proteger o proprio codigo."),
    Rank("🔮 Mago das Funções", "Mago das Funcoes", 1600, "🔮", "Transforma repeticao em funcoes e ganha velocidade na jornada."),
    Rank("📚 Guardião dos Dados", "Guardiao dos Dados", 2600, "📚", "Organiza registros, arquivos e dados como parte viva do sistema."),
    Rank("🏰 Arquiteto de Classes", "Arquiteto de Classes", 3800, "🏰", "Da forma a sistemas maiores com objetos, testes e clareza."),
    Rank("🌐 Invocador de APIs", "Invocador de APIs", 5200, "🌐", "Conecta a Guilda a fontes externas e coleta dados do mundo real."),
    Rank("📊 Analista Arcano", "Analista Arcano", 6800, "📊", "Transforma tabelas em leitura, metricas e decisoes."),
    Rank("⚙️ Engenheiro da Guilda", "Engenheiro da Guilda", 8400, "⚙️", "Constrói pipelines, bancos e automacoes que sustentam a campanha."),
    Rank("👑 Mestre dos Dados", "Mestre dos Dados", 10500, "👑", "Fecha a jornada com portfolio, autonomia e dominio em dados."),
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
