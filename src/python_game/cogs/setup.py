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
        bot_member = guild.me

        public_read = self._overwrites(
            everyone_role=everyone,
            everyone_overwrite=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False,
                add_reactions=False,
                create_public_threads=False,
                create_private_threads=False,
            ),
            bot=discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
            ),
            bot_member=bot_member,
        )
        onboarded_read = self._overwrites(
            everyone_role=everyone,
            everyone_overwrite=discord.PermissionOverwrite(view_channel=False),
            novato=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False,
                add_reactions=False,
                create_public_threads=False,
                create_private_threads=False,
            ),
            bot=discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
            ),
            novato_role=novato_role,
            bot_member=bot_member,
        )
        guild_chat = self._overwrites(
            everyone_role=everyone,
            everyone_overwrite=discord.PermissionOverwrite(view_channel=False),
            novato=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
                add_reactions=True,
                attach_files=False,
                create_public_threads=False,
                create_private_threads=False,
            ),
            bot=discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
            ),
            novato_role=novato_role,
            bot_member=bot_member,
        )
        deliveries_write = self._overwrites(
            everyone_role=everyone,
            everyone_overwrite=discord.PermissionOverwrite(view_channel=False),
            novato=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
                add_reactions=False,
                attach_files=True,
                create_public_threads=False,
                create_private_threads=False,
            ),
            bot=discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
            ),
            novato_role=novato_role,
            bot_member=bot_member,
        )

        start_category = await self._get_or_create_category(guild, "🎮 START", overwrites=public_read)
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

        welcome = await self._get_or_create_text(guild, start_category, "👋-boas-vindas", public_read)
        how_it_works = await self._get_or_create_text(guild, start_category, "🧭-como-funciona", public_read)
        start = await self._get_or_create_text(guild, start_category, "✅-iniciar-jornada", public_read)
        chat = await self._get_or_create_text(guild, game_category, "💬-chat-da-guilda", guild_chat)
        trail = await self._get_or_create_text(guild, game_category, "🐍-trilha-python", onboarded_read)
        deliveries = await self._get_or_create_text(guild, game_category, "📦-entregas", deliveries_write)
        ranking = await self._get_or_create_text(guild, game_category, "🏆-ranking", onboarded_read)
        achievements = await self._get_or_create_text(guild, game_category, "📜-conquistas", onboarded_read)

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

        await self._replace_setup_embed(welcome, self._welcome_embed())
        await self._replace_setup_embed(how_it_works, self._how_it_works_embed())
        await self._replace_setup_embed(start, self._start_embed())

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
                "A fortaleza esta pronta.\n\n"
                f"Canais criados: {welcome.mention}, {how_it_works.mention}, {start.mention}, "
                f"{chat.mention}, {trail.mention}, {deliveries.mention}, {ranking.mention}, {achievements.mention}\n"
                f"Salas de estudo: {silent.name}, {cafe.name}\n\n"
                "Agora chame a Guilda com `/iniciar`."
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
                await existing.edit(overwrites=dict(overwrites))
            return existing
        if overwrites:
            return await guild.create_category(name=name, overwrites=dict(overwrites))
        return await guild.create_category(name=name)

    async def _get_or_create_text(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
        name: str,
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] | None = None,
    ) -> discord.TextChannel:
        existing = discord.utils.get(guild.text_channels, name=name)
        if existing:
            if overwrites:
                await existing.edit(category=category, overwrites=dict(overwrites))
            return existing
        if overwrites:
            return await guild.create_text_channel(name=name, category=category, overwrites=dict(overwrites))
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
                await existing.edit(overwrites=dict(overwrites))
            return existing
        if overwrites:
            return await guild.create_voice_channel(name=name, category=category, overwrites=dict(overwrites))
        return await guild.create_voice_channel(name=name, category=category)

    async def _replace_setup_embed(self, channel: discord.TextChannel, embed: discord.Embed) -> None:
        marker = "python.game.gg • setup"
        permissions = channel.permissions_for(channel.guild.me) if channel.guild.me else None
        if permissions and permissions.manage_messages:
            try:
                await channel.purge(
                    limit=20,
                    check=lambda message: (
                        message.author == channel.guild.me
                        and bool(message.embeds)
                        and message.embeds[0].footer.text == marker
                    ),
                )
            except discord.HTTPException:
                pass
        embed.set_footer(text=marker)
        await channel.send(embed=embed)

    @staticmethod
    def _welcome_embed() -> discord.Embed:
        embed = discord.Embed(
            title="🎮 O portão da Guilda se abriu",
            description=(
                "Bem-vindo ao **python.game**.\n\n"
                "Este servidor é o seu **mapa de campanha**: missões de Python, entregas reais, "
                "XP, ranks, projetos de portfólio e uma comunidade avançando junto.\n\n"
                "Aqui ninguém evolui sozinho. A Guilda pergunta, responde, revisa, celebra progresso "
                "e transforma prática em aventura, um desafio por vez."
            ),
            color=0x44D07B,
        )
        embed.add_field(name="🧱 Comece pequeno", value="Um exercício, uma entrega, um avanço.", inline=True)
        embed.add_field(name="⚔️ Evolua em público", value="Mostre progresso, peça ajuda e ajude outros membros.", inline=True)
        embed.add_field(name="💾 Construa algo real", value="Cada projeto vira parte da sua história profissional.", inline=False)
        return embed

    @staticmethod
    def _how_it_works_embed() -> discord.Embed:
        embed = discord.Embed(
            title="🗺️ Como a campanha funciona",
            description=(
                "**1.** Use `/iniciar` para gravar seu nome no Registro da Guilda.\n"
                "**2.** Receba uma missão e leia o objetivo de campo.\n"
                "**3.** Escreva código, teste, erre, ajuste e aprenda.\n"
                "**4.** Entregue sua solução para receber feedback.\n"
                "**5.** Ganhe XP, suba de rank e fortaleça seu portfólio.\n\n"
                "O ritmo da Guilda é simples: **aparecer, praticar, entregar, ajudar e voltar mais forte**."
            ),
            color=0x4EA5FF,
        )
        embed.add_field(name="🕹️ Progressão", value="XP, ranks, missões e conquistas visíveis.", inline=True)
        embed.add_field(name="📜 Feedback", value="A entrega só conta quando chega no formato certo.", inline=True)
        embed.add_field(name="☕ Comunidade", value="Use o café para conversar e o quarto silencioso para foco.", inline=False)
        return embed

    @staticmethod
    def _start_embed() -> discord.Embed:
        embed = discord.Embed(
            title="✅ Acenda sua primeira missão",
            description=(
                "Se você está pronto para entrar na campanha, use:\n\n"
                "`/iniciar nome:<seu_nome_de_aventureiro>`\n\n"
                "A partir daí, o bot abre seu mapa, registra seu progresso e libera o primeiro capítulo."
            ),
            color=0xF2C94C,
        )
        embed.add_field(name="🥚 Primeiro cargo", value="Novato", inline=True)
        embed.add_field(name="🧭 Primeiro passo", value="Abrir o mapa da jornada", inline=True)
        return embed

    @staticmethod
    def _overwrites(
        *,
        everyone_role: discord.Role,
        everyone_overwrite: discord.PermissionOverwrite,
        bot_member: discord.Member | None,
        novato_role: discord.Role | None = None,
        novato: discord.PermissionOverwrite | None = None,
        bot: discord.PermissionOverwrite | None = None,
    ) -> dict[discord.abc.Snowflake, discord.PermissionOverwrite]:
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] = {
            everyone_role: everyone_overwrite
        }
        if novato_role and novato:
            overwrites[novato_role] = novato
        if bot_member and bot:
            overwrites[bot_member] = bot
        return overwrites
