from __future__ import annotations

import discord

from python_game.content_repository import TrailContent
from python_game.database import Player
from python_game.ranks import next_rank_for_xp


PIXEL_GREEN = 0x44D07B
PIXEL_BLUE = 0x4EA5FF
PIXEL_PURPLE = 0xA779FF
PIXEL_GOLD = 0xF2C94C
PIXEL_RED = 0xEF6262


def mission_embed(content: TrailContent, has_materials: bool) -> discord.Embed:
    embed = discord.Embed(
        title=f"🗺️ Missao desbloqueada: {content.title}",
        description=(
            f"**Objetivo:** {content.objective}\n\n"
            "Complete a missao, envie sua solucao e avance no mapa da Guilda."
        ),
        color=PIXEL_BLUE,
    )
    embed.add_field(name="ID da missao", value=f"`{content.id}`", inline=True)
    embed.add_field(name="Semana", value=str(content.week), inline=True)
    embed.add_field(name="XP base", value=str(content.raw.get("xp_sugerido", 100)), inline=True)
    embed.add_field(name="Projeto relacionado", value=content.raw.get("projeto_relacionado", "Missao pratica"), inline=False)
    if has_materials:
        embed.add_field(name="📚 Materiais", value="Ha links cadastrados para apoiar esta missao.", inline=False)
    else:
        embed.add_field(
            name="📚 Materiais",
            value="Nenhum link foi cadastrado ainda. A missao continua liberada pelo objetivo e criterios internos.",
            inline=False,
        )
    embed.set_footer(text="python.game • complete missoes, ganhe XP, construa portfolio")
    return embed


def profile_embed(player: Player, completed: int, attempts: int, projects: int) -> discord.Embed:
    next_rank = next_rank_for_xp(player.xp)
    embed = discord.Embed(
        title=f"🎮 Perfil de {player.hero_name}",
        description=f"Rank atual: **{player.rank_role}**",
        color=PIXEL_PURPLE,
    )
    embed.add_field(name="XP", value=str(player.xp), inline=True)
    embed.add_field(name="Level", value=str(player.level), inline=True)
    embed.add_field(name="Missoes concluidas", value=str(completed), inline=True)
    embed.add_field(name="Tentativas", value=str(attempts), inline=True)
    embed.add_field(name="Projetos no portfolio", value=str(projects), inline=True)
    embed.add_field(name="Missao ativa", value=f"`{player.active_content_id}`" if player.active_content_id else "Nenhuma", inline=False)
    if next_rank:
        remaining = next_rank.min_xp - player.xp
        embed.add_field(name="Proximo rank", value=f"{next_rank.role_name} em {remaining} XP", inline=False)
    else:
        embed.add_field(name="Proximo rank", value="Voce chegou ao topo da Guilda.", inline=False)
    return embed


def feedback_embed(title: str, score: int, accepted: bool, strengths: tuple[str, ...], improvements: tuple[str, ...]) -> discord.Embed:
    embed = discord.Embed(
        title=("✅ " if accepted else "🛠️ ") + title,
        color=PIXEL_GREEN if accepted else PIXEL_RED,
    )
    embed.add_field(name="Score", value=f"{score}/100", inline=True)
    embed.add_field(name="Status", value="Aprovada" if accepted else "Ajustes necessarios", inline=True)
    embed.add_field(name="Pontos fortes", value="\n".join(f"- {item}" for item in strengths[:4]) or "-", inline=False)
    embed.add_field(name="Proximos ajustes", value="\n".join(f"- {item}" for item in improvements[:4]) or "-", inline=False)
    return embed

