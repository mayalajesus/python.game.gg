from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from python_game.content_repository import ContentRepository, has_recommendation_links
from python_game.database import GameDatabase
from python_game.discord_helpers import require_guild, require_member, sync_member_rank
from python_game.embeds import mission_embed, profile_embed
from python_game.ranks import RANKS


class OnboardingCog(commands.Cog):
    def __init__(self, bot: commands.Bot, contents: ContentRepository, database: GameDatabase) -> None:
        self.bot = bot
        self.contents = contents
        self.database = database

    @app_commands.command(name="iniciar", description="Inicia sua jornada na Guilda python.game.")
    async def iniciar(self, interaction: discord.Interaction, nome: str | None = None) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        hero_name = (nome or member.display_name).strip()[:40]
        first_content_id = self.contents.first_content_id()

        player = self.database.upsert_player(
            discord_id=member.id,
            guild_id=guild.id,
            display_name=member.display_name,
            hero_name=hero_name,
            rank_role=RANKS[0].role_name,
            active_content_id=first_content_id,
        )
        rank_role = await sync_member_rank(member, player.xp)
        if rank_role != player.rank_role:
            player = self.database.add_xp(
                discord_id=member.id,
                guild_id=guild.id,
                amount=0,
                reason="rank sync",
                rank_role=rank_role,
            )

        content = self.contents.get_content(player.active_content_id or first_content_id)
        await interaction.response.send_message(
            (
                f"🥚 **{player.hero_name}, seu nome foi gravado no Registro da Guilda.**\n\n"
                "A primeira marca do seu mapa acendeu. A partir daqui, cada entrega conta: "
                "pergunte, ajude, mostre progresso e avance com a comunidade."
            ),
            embed=mission_embed(content, has_recommendation_links(content)),
            ephemeral=True,
        )

    @app_commands.command(name="formato", description="Mostra o modelo correto de entrega.")
    async def formato(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            (
                "📜 **Formato oficial de entrega**\n\n"
                "O avaliador da Guilda so abre a correcao quando a missao chega neste formato:\n\n"
                "````text\n"
                "/entregar desafio_id: fundamentos_01\n\n"
                "Codigo:\n"
                "```python\n"
                "seu codigo aqui\n"
                "```\n\n"
                "Explicacao:\n"
                "Explique em poucas linhas como sua solucao funciona.\n"
                "````\n\n"
                "Clareza tambem faz parte da missao."
            ),
            ephemeral=True,
        )

    @app_commands.command(name="perfil", description="Mostra seu perfil, XP, rank e progresso.")
    async def perfil(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        player = self.database.get_player(member.id, guild.id)
        if player is None:
            await interaction.response.send_message(
                "Seu nome ainda nao apareceu no Registro da Guilda. Use `/iniciar` para abrir sua campanha.",
                ephemeral=True,
            )
            return
        stats = self.database.stats(member.id, guild.id)
        await interaction.response.send_message(
            embed=profile_embed(player, stats["completed"], stats["attempts"], stats["projects"]),
            ephemeral=True,
        )

    @app_commands.command(name="guia", description="Mostra os comandos principais da Guilda.")
    async def guia(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            (
                "🎮 **Painel da Guilda**\n\n"
                "`/setup_servidor` ergue a estrutura da campanha.\n"
                "`/iniciar` grava seu nome no Registro da Guilda.\n"
                "`/missao` mostra ou troca o capitulo ativo.\n"
                "`/conteudo` abre a biblioteca da missao.\n"
                "`/entregar` envia sua solucao para avaliacao.\n"
                "`/perfil` mostra sua cronica: XP, rank e progresso.\n"
                "`/ranking` revela o placar da Guilda.\n"
                "`/registrar_projeto` coloca uma entrega na sua vitrine.\n"
            ),
            ephemeral=True,
        )
