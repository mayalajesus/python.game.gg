from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from python_game.database import GameDatabase
from python_game.discord_helpers import ensure_rank_roles, require_guild


class SetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot, database: GameDatabase) -> None:
        self.bot = bot
        self.database = database

    @app_commands.command(name="setup_servidor", description="Cria a estrutura minimalista da Guilda python.game.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_servidor(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        roles = await ensure_rank_roles(guild)
        novato_role = roles["🥚 Novato"]
        everyone = guild.default_role

        start_category = await self._get_or_create_category(guild, "🎮 START")
        game_category = await self._get_or_create_category(
            guild,
            "🐍 PYTHON.GAME",
            overwrites={
                everyone: discord.PermissionOverwrite(view_channel=False),
                novato_role: discord.PermissionOverwrite(view_channel=True),
            },
        )
        study_category = await self._get_or_create_category(
            guild,
            "🎧 SALAS DE ESTUDO",
            overwrites={
                everyone: discord.PermissionOverwrite(view_channel=False),
                novato_role: discord.PermissionOverwrite(view_channel=True),
            },
        )

        welcome = await self._get_or_create_text(guild, start_category, "👋-boas-vindas")
        how_it_works = await self._get_or_create_text(guild, start_category, "🧭-como-funciona")
        start = await self._get_or_create_text(guild, start_category, "✅-iniciar-jornada")
        chat = await self._get_or_create_text(guild, game_category, "💬-chat-da-guilda")
        trail = await self._get_or_create_text(guild, game_category, "🐍-trilha-python")
        deliveries = await self._get_or_create_text(guild, game_category, "📦-entregas")
        ranking = await self._get_or_create_text(guild, game_category, "🏆-ranking")
        achievements = await self._get_or_create_text(guild, game_category, "📜-conquistas")

        silent = await self._get_or_create_voice(
            guild,
            study_category,
            "🔇 quarto-silencioso",
            overwrites={
                everyone: discord.PermissionOverwrite(view_channel=False),
                novato_role: discord.PermissionOverwrite(view_channel=True, connect=True, speak=False),
            },
        )
        cafe = await self._get_or_create_voice(
            guild,
            study_category,
            "☕ area-do-cafe",
            overwrites={
                everyone: discord.PermissionOverwrite(view_channel=False),
                novato_role: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True),
            },
        )

        await welcome.send(
            "🎮 **Bem-vindo ao python.game**\n\n"
            "Voce entrou na Guilda dos Aprendizes. Aqui voce evolui por missoes, XP, ranks e projetos reais."
        )
        await how_it_works.send(
            "🧭 **Como funciona**\n\n"
            "1. Use `/iniciar`\n"
            "2. Receba uma missao\n"
            "3. Estude pelo objetivo da missao\n"
            "4. Entregue seu codigo\n"
            "5. Ganhe XP e desbloqueie ranks\n\n"
            "Links de estudo sao bonus. A jornada funciona mesmo antes deles serem cadastrados."
        )
        await start.send("✅ Use `/iniciar nome:<seu_nome_de_aventureiro>` para abrir o mapa da Guilda.")

        self.database.save_guild_setup(
            guild.id,
            {
                "announcements": achievements.id,
                "trail": trail.id,
                "deliveries": deliveries.id,
                "ranking": ranking.id,
            },
        )

        await interaction.followup.send(
            (
                "Setup concluido.\n\n"
                f"Canais criados: {welcome.mention}, {how_it_works.mention}, {start.mention}, "
                f"{chat.mention}, {trail.mention}, {deliveries.mention}, {ranking.mention}, {achievements.mention}\n"
                f"Voz: {silent.name}, {cafe.name}"
            ),
            ephemeral=True,
        )

    async def _get_or_create_category(
        self,
        guild: discord.Guild,
        name: str,
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] | None = None,
    ) -> discord.CategoryChannel:
        existing = discord.utils.get(guild.categories, name=name)
        if existing:
            if overwrites:
                await existing.edit(overwrites=overwrites)
            return existing
        return await guild.create_category(name=name, overwrites=overwrites)

    async def _get_or_create_text(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
        name: str,
    ) -> discord.TextChannel:
        existing = discord.utils.get(guild.text_channels, name=name)
        if existing:
            return existing
        return await guild.create_text_channel(name=name, category=category)

    async def _get_or_create_voice(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
        name: str,
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] | None = None,
    ) -> discord.VoiceChannel:
        existing = discord.utils.get(guild.voice_channels, name=name)
        if existing:
            if overwrites:
                await existing.edit(overwrites=overwrites)
            return existing
        return await guild.create_voice_channel(name=name, category=category, overwrites=overwrites)

