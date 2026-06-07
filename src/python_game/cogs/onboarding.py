from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from python_game.content_repository import ContentRepository, has_recommendation_links
from python_game.database import GameDatabase
from python_game.discord_helpers import require_guild, require_member
from python_game.embeds import mission_embed, profile_embed
from python_game.game_service import start_player_journey


class OnboardingCog(commands.Cog):
    def __init__(self, bot: commands.Bot, contents: ContentRepository, database: GameDatabase) -> None:
        self.bot = bot
        self.contents = contents
        self.database = database

    @app_commands.command(name="iniciar", description="Inicia sua jornada na Guilda python.game.")
    async def iniciar(self, interaction: discord.Interaction, nome: str | None = None) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        result = await start_player_journey(
            member=member,
            contents=self.contents,
            database=self.database,
            hero_name=nome,
        )

        settings = self.database.guild_settings(guild.id)
        trail_channel = guild.get_channel(settings["trail"]) if settings["trail"] else None
        trail_hint = trail_channel.mention if isinstance(trail_channel, discord.TextChannel) else "#🧩-trilha-python"
        intro = "Seu registro foi aceso no Livro da Guilda." if result.is_new_player else "Seu registro já estava aceso."
        xp_line = f"⭐ XP inicial recebido: **+{result.xp_awarded} XP**" if result.xp_awarded else "⭐ XP inicial já registrado."

        await interaction.response.send_message(
            (
                f"🏰 **{result.player.hero_name}, você agora é Aprendiz da Python.Game.**\n\n"
                f"{intro}\n"
                "🎒 Cargo liberado: **Aprendiz**\n"
                f"{xp_line}\n"
                f"📜 Primeira missão: {trail_hint}"
            ),
            embed=mission_embed(result.content, has_recommendation_links(result.content)),
            ephemeral=True,
        )
        if result.is_new_player:
            await self._announce_new_apprentice(guild, member, result.player.hero_name)

    @app_commands.command(name="formato", description="Mostra o modelo correto de entrega.")
    async def formato(self, interaction: discord.Interaction) -> None:
        desafio_id = self.contents.first_content_id()
        await interaction.response.send_message(
            (
                "📜 **Formato oficial de entrega**\n\n"
                "**1. Registro social em `📦-entregas`:**\n"
                "```text\n"
                f"Missão: {desafio_id}\n"
                "Github: sem repositorio\n"
                "Observações: instalei o ambiente e validei as ferramentas.\n"
                "```\n\n"
                "**2. Correção e XP:** use `/entregar` e preencha:\n"
                f"`desafio_id`: `{desafio_id}`\n"
                "`codigo`: evidências, comandos usados ou código da missão\n"
                "`explicacao`: checklist do que foi feito e como você validou\n\n"
                "Clareza também faz parte da missão."
            ),
            ephemeral=True,
        )

    async def _announce_new_apprentice(self, guild: discord.Guild, member: discord.Member, hero_name: str) -> None:
        settings = self.database.guild_settings(guild.id)
        channel_id = settings.get("announcements")
        channel = guild.get_channel(channel_id) if channel_id else None
        if not isinstance(channel, discord.TextChannel):
            return

        embed = discord.Embed(
            title="🎒 Novo Aprendiz na Guilda",
            description=(
                f"{member.mention} entrou na campanha como **{hero_name}**.\n\n"
                "O mapa acendeu, a primeira missão foi liberada e a Guilda ganhou mais uma pessoa construindo em público."
            ),
            color=0x44D07B,
        )
        embed.set_footer(text="python.game.gg • onboarding")
        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            pass

    @app_commands.command(name="perfil", description="Mostra seu perfil, XP, rank e progresso.")
    async def perfil(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        player = self.database.get_player(member.id, guild.id)
        if player is None:
            await interaction.response.send_message(
                "Seu nome ainda não apareceu no Registro da Guilda. Use `/iniciar` para abrir sua campanha.",
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
                "`/missao` mostra ou troca o capítulo ativo.\n"
                "`/conteudo` abre a biblioteca da missão.\n"
                "`/entregar` envia sua solução para avaliação.\n"
                "`/perfil` mostra sua crônica: XP, rank e progresso.\n"
                "`/ranking` revela o placar da Guilda.\n"
                "`/registrar_projeto` coloca uma entrega na sua vitrine.\n"
            ),
            ephemeral=True,
        )
