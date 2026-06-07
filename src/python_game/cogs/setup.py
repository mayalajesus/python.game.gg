from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from python_game.content_repository import ContentRepository, TrailContent
from python_game.database import GameDatabase
from python_game.discord_helpers import ensure_access_role, ensure_rank_roles, require_guild
from python_game.views import MissionFeedView, PortalView, StartJourneyView


SETUP_MARKER = "python.game.gg • setup"
LEGACY_SETUP_MARKERS = {
    SETUP_MARKER,
    "python.game.gg â€¢ setup",
}
LEGACY_SETUP_TEXT = (
    "Próximo portal",
    "Proximo portal",
    "Siga para",
    "O portão da Guilda se abriu",
    "O portao da Guilda se abriu",
    "Como a campanha funciona",
    "Acenda sua primeira missão",
    "Acenda sua primeira missao",
)


class SetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot, contents: ContentRepository, database: GameDatabase) -> None:
        self.bot = bot
        self.contents = contents
        self.database = database

    @app_commands.command(name="setup_servidor", description="Cria a jornada guiada da Guilda python.game.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_servidor(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        await ensure_rank_roles(guild)
        apprentice_role = await ensure_access_role(guild)
        everyone = guild.default_role
        bot_member = guild.me

        start_read_only = self._overwrites(
            everyone,
            discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False,
                add_reactions=False,
                create_public_threads=False,
                create_private_threads=False,
                use_application_commands=False,
            ),
            bot_member,
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
                use_application_commands=True,
            ),
        )
        start_action = self._overwrites(
            everyone,
            discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False,
                add_reactions=False,
                create_public_threads=False,
                create_private_threads=False,
                use_application_commands=True,
            ),
            bot_member,
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
                use_application_commands=True,
            ),
        )
        category_locked = self._role_overwrites(
            everyone=everyone,
            role=apprentice_role,
            member_overwrite=discord.PermissionOverwrite(view_channel=True, read_message_history=True),
            bot_member=bot_member,
        )
        read_only = self._role_overwrites(
            everyone=everyone,
            role=apprentice_role,
            member_overwrite=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False,
                add_reactions=False,
                create_public_threads=False,
                create_private_threads=False,
                use_application_commands=True,
            ),
            bot_member=bot_member,
        )
        community_write = self._role_overwrites(
            everyone=everyone,
            role=apprentice_role,
            member_overwrite=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
                add_reactions=True,
                attach_files=True,
                create_public_threads=False,
                create_private_threads=False,
                use_application_commands=True,
            ),
            bot_member=bot_member,
        )
        deliveries_write = self._role_overwrites(
            everyone=everyone,
            role=apprentice_role,
            member_overwrite=discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
                add_reactions=False,
                attach_files=True,
                create_public_threads=False,
                create_private_threads=False,
                use_application_commands=True,
            ),
            bot_member=bot_member,
        )

        start_category = await self._get_or_create_category(guild, "🏰 START", overwrites=start_read_only, position=0)
        game_category = await self._get_or_create_category(
            guild,
            "🌎 PYTHON.GAME",
            overwrites=category_locked,
            aliases=("🐍 PYTHON.GAME",),
            position=1,
        )
        community_category = await self._get_or_create_category(
            guild,
            "🏕️ COMUNIDADE",
            overwrites=category_locked,
            aliases=("🎧 SALAS DE ESTUDO",),
            position=2,
        )

        welcome = await self._get_or_create_text(
            guild,
            start_category,
            "01-👋-bem-vindo",
            start_read_only,
            aliases=("👋-boas-vindas", "👋-bem-vindo", "boas-vindas", "bem-vindo"),
            position=0,
        )
        how_it_works = await self._get_or_create_text(
            guild,
            start_category,
            "02-🎯-como-funciona",
            start_read_only,
            aliases=("02-🧭-como-funciona", "🧭-como-funciona", "🎯-como-funciona", "como-funciona"),
            position=1,
        )
        start = await self._get_or_create_text(
            guild,
            start_category,
            "03-✅-iniciar-jornada",
            start_action,
            aliases=("✅-iniciar-jornada", "iniciar-jornada"),
            position=2,
        )

        journey_map = await self._get_or_create_text(
            guild,
            game_category,
            "🗺️-mapa-da-jornada",
            read_only,
            aliases=("mapa-da-jornada", "🗺️-mapa"),
            position=0,
        )
        trail = await self._get_or_create_text(
            guild,
            game_category,
            "🧩-trilha-python",
            read_only,
            aliases=("🐍-trilha-python", "trilha-python"),
            position=1,
        )
        deliveries = await self._get_or_create_text(
            guild,
            game_category,
            "📦-entregas",
            deliveries_write,
            aliases=("entregas",),
            position=2,
        )
        ranking = await self._get_or_create_text(
            guild,
            game_category,
            "🏆-ranking",
            read_only,
            aliases=("ranking",),
            position=3,
        )
        achievements = await self._get_or_create_text(
            guild,
            game_category,
            "📜-conquistas",
            read_only,
            aliases=("conquistas",),
            position=4,
        )

        chat = await self._get_or_create_text(
            guild,
            community_category,
            "💬-chat-da-guilda",
            community_write,
            aliases=("chat-da-guilda",),
            position=0,
        )
        focus = await self._get_or_create_voice(
            guild,
            community_category,
            "🕯️ sala-de-foco",
            overwrites=self._voice_overwrites(everyone, apprentice_role, can_speak=False, bot_member=bot_member),
            aliases=("🔇 quarto-silencioso", "quarto-silencioso", "sala-de-foco"),
            position=1,
        )
        cafe = await self._get_or_create_voice(
            guild,
            community_category,
            "☕ area-do-cafe",
            overwrites=self._voice_overwrites(everyone, apprentice_role, can_speak=True, bot_member=bot_member),
            aliases=("area-do-cafe",),
            position=2,
        )

        first_content = self.contents.get_content(self.contents.first_content_id())

        await self._replace_setup_embed(
            welcome,
            self._welcome_embed(how_it_works),
            view=PortalView(label="Continuar", emoji="🧭", url=how_it_works.jump_url),
        )
        await self._replace_setup_embed(
            how_it_works,
            self._how_it_works_embed(start),
            view=PortalView(label="Iniciar Jornada", emoji="🚀", url=start.jump_url),
        )
        await self._replace_setup_embed(
            start,
            self._start_embed(),
            view=StartJourneyView(self.contents, self.database),
        )
        await self._replace_setup_embed(journey_map, self._journey_map_embed())
        await self._replace_setup_embed(
            trail,
            self._mission_feed_embed(first_content),
            view=MissionFeedView(self.database, self.contents),
        )
        await self._replace_setup_embed(deliveries, self._deliveries_embed(), pin=True)
        await self._replace_setup_embed(ranking, self._ranking_embed())
        await self._replace_setup_embed(achievements, self._achievements_embed())
        await self._replace_setup_embed(chat, self._tavern_embed(), pin=True)

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
                "A jornada guiada está pronta.\n\n"
                f"Entrada: {welcome.mention} → {how_it_works.mention} → {start.mention}\n"
                f"Mapa e missões: {journey_map.mention}, {trail.mention}, {deliveries.mention}\n"
                f"Comunidade: {chat.mention}, {focus.name}, {cafe.name}\n\n"
                "Quem chega vê apenas o START. Ao clicar em **Tornar-se Aprendiz**, recebe o cargo e libera o resto da Guilda."
            ),
            ephemeral=True,
        )

    async def _get_or_create_category(
        self,
        guild: discord.Guild,
        name: str,
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] | None = None,
        aliases: tuple[str, ...] = (),
        position: int | None = None,
    ) -> discord.CategoryChannel:
        existing = self._find_category(guild, (name, *aliases))
        if existing:
            edit_options: dict[str, object] = {"name": name}
            if overwrites:
                edit_options["overwrites"] = dict(overwrites)
            if position is not None:
                edit_options["position"] = position
            await existing.edit(**edit_options)
            return existing
        return await guild.create_category(name=name, overwrites=dict(overwrites or {}), position=position)

    async def _get_or_create_text(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
        name: str,
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] | None = None,
        aliases: tuple[str, ...] = (),
        position: int | None = None,
    ) -> discord.TextChannel:
        existing = self._find_text_channel(guild, (name, *aliases))
        if existing:
            edit_options: dict[str, object] = {"name": name, "category": category}
            if overwrites:
                edit_options["overwrites"] = dict(overwrites)
            if position is not None:
                edit_options["position"] = position
            await existing.edit(**edit_options)
            return existing
        return await guild.create_text_channel(
            name=name,
            category=category,
            overwrites=dict(overwrites or {}),
            position=position,
        )

    async def _get_or_create_voice(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
        name: str,
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] | None = None,
        aliases: tuple[str, ...] = (),
        position: int | None = None,
    ) -> discord.VoiceChannel:
        existing = self._find_voice_channel(guild, (name, *aliases))
        if existing:
            edit_options: dict[str, object] = {"name": name, "category": category}
            if overwrites:
                edit_options["overwrites"] = dict(overwrites)
            if position is not None:
                edit_options["position"] = position
            await existing.edit(**edit_options)
            return existing
        return await guild.create_voice_channel(
            name=name,
            category=category,
            overwrites=dict(overwrites or {}),
            position=position,
        )

    async def _replace_setup_embed(
        self,
        channel: discord.TextChannel,
        embed: discord.Embed,
        *,
        view: discord.ui.View | None = None,
        pin: bool = False,
    ) -> discord.Message:
        permissions = channel.permissions_for(channel.guild.me) if channel.guild.me else None
        if permissions and permissions.manage_messages:
            try:
                await channel.purge(
                    limit=30,
                    check=self._is_setup_message,
                )
            except discord.HTTPException:
                pass

        embed.set_footer(text=SETUP_MARKER)
        message = await channel.send(embed=embed, view=view)
        if pin and permissions and permissions.manage_messages:
            try:
                await message.pin(reason="python.game setup")
            except discord.HTTPException:
                pass
        return message

    @staticmethod
    def _is_setup_message(message: discord.Message) -> bool:
        if message.guild is None or message.author != message.guild.me or not message.embeds:
            return False
        embed = message.embeds[0]
        footer = embed.footer.text or ""
        title = embed.title or ""
        description = embed.description or ""
        field_text = "\n".join(f"{field.name}\n{field.value}" for field in embed.fields)
        searchable = f"{title}\n{description}\n{field_text}"
        return footer in LEGACY_SETUP_MARKERS or any(fragment in searchable for fragment in LEGACY_SETUP_TEXT)

    @staticmethod
    def _welcome_embed(next_channel: discord.TextChannel) -> discord.Embed:
        embed = discord.Embed(
            title="🏰 ▣ Bem-vindo à Python.Game",
            description=(
                "Você acaba de entrar em uma Guilda onde cada desafio gera experiência, "
                "cada projeto fortalece suas habilidades e cada conquista marca sua evolução.\n\n"
                "**Sua jornada começa agora.**\n\n"
                "Use o botão abaixo para abrir o próximo portal."
            ),
            color=0x44D07B,
        )
        return embed

    @staticmethod
    def _how_it_works_embed(next_channel: discord.TextChannel) -> discord.Embed:
        embed = discord.Embed(
            title="🎯 ▣ Como funciona",
            description=(
                "Sua jornada é simples:\n\n"
                "⚔️ Complete missões\n"
                "📈 Ganhe XP\n"
                "🏆 Desbloqueie conquistas\n"
                "📂 Construa projetos\n"
                "🚀 Evolua seu portfólio\n\n"
                "Tudo o que você aprender será usado em desafios reais.\n\n"
                "**Nenhum exercício existe apenas para preencher tempo.**"
            ),
            color=0x4EA5FF,
        )
        return embed

    @staticmethod
    def _start_embed() -> discord.Embed:
        embed = discord.Embed(
            title="✅ ▣ Sua primeira missão",
            description=(
                "Clique abaixo para iniciar sua jornada.\n\n"
                "Ao iniciar você receberá:\n\n"
                "🎒 Cargo de Aprendiz\n"
                "📜 Acesso à Trilha Python\n"
                "⭐ XP inicial"
            ),
            color=0xF2C94C,
        )
        embed.add_field(name="Portal", value="⚔️ **Tornar-se Aprendiz**", inline=False)
        return embed

    @staticmethod
    def _journey_map_embed() -> discord.Embed:
        embed = discord.Embed(
            title="🗺️ ▣ Mapa da Jornada",
            description=(
                "```text\n"
                "🏰 Início\n"
                "   ↓\n"
                "🌱 Fundamentos\n"
                "   ↓\n"
                "⚔️ Condicionais\n"
                "   ↓\n"
                "🔄 Loops\n"
                "   ↓\n"
                "🧙 Funções\n"
                "   ↓\n"
                "📂 Arquivos\n"
                "   ↓\n"
                "🏛️ Orientação a Objetos\n"
                "   ↓\n"
                "🌐 APIs\n"
                "   ↓\n"
                "📊 Dados\n"
                "   ↓\n"
                "👑 Engenheiro de Dados\n"
                "```"
            ),
            color=0xA779FF,
        )
        embed.add_field(name="Como ler o mapa", value="Você avança por entregas aprovadas, não por tempo assistido.", inline=False)
        return embed

    @staticmethod
    def _mission_feed_embed(content: TrailContent) -> discord.Embed:
        mission_number = max(0, content.order)
        embed = discord.Embed(
            title=f"📜 MISSÃO {mission_number:02d}",
            description=(
                f"**Nome:**\n{content.title}\n\n"
                f"**Objetivo:**\n{content.objective}\n\n"
                f"**Recompensa:**\n+{content.raw.get('xp_sugerido', 100)} XP"
            ),
            color=0x4EA5FF,
        )
        embed.add_field(name="Selo da missão", value=f"`{content.id}`", inline=True)
        embed.add_field(name="Entrega", value="Use o botão quando estiver pronto para ver o modelo.", inline=False)
        return embed

    @staticmethod
    def _deliveries_embed() -> discord.Embed:
        embed = discord.Embed(
            title="📦 ▣ Entregas",
            description=(
                "Use este canal para registrar entregas em público. Depois use `/entregar` para correção, XP e progressão.\n\n"
                "**1. Registro social:**\n"
                "```text\n"
                "Missão: ambiente_desenvolvimento\n"
                "Github: sem repositorio\n"
                "Observações: instalei o ambiente e validei as ferramentas.\n"
                "```\n"
                "**2. Correção:** envie `/entregar` com o mesmo `desafio_id`, suas evidências no campo `codigo` "
                "e um checklist no campo `explicacao`."
            ),
            color=0xF2C94C,
        )
        return embed

    @staticmethod
    def _ranking_embed() -> discord.Embed:
        embed = discord.Embed(
            title="🏆 ▣ Ranking da Guilda",
            description=(
                "O placar será atualizado pelo bot conforme os Aprendizes concluem missões.\n\n"
                "🥇 Aguardando o primeiro nome\n"
                "🥈 Aguardando o próximo avanço\n"
                "🥉 Aguardando uma nova conquista"
            ),
            color=0xF2C94C,
        )
        return embed

    @staticmethod
    def _achievements_embed() -> discord.Embed:
        embed = discord.Embed(
            title="📜 ▣ Conquistas da Guilda",
            description=(
                "Quando alguém desbloquear uma conquista, o anúncio aparece aqui.\n\n"
                "🏆 Conquista Desbloqueada\n"
                "Usuário: @Aprendiz\n"
                "Conquista: Primeira Função\n"
                "Descrição: criou sua primeira função Python."
            ),
            color=0xA779FF,
        )
        return embed

    @staticmethod
    def _tavern_embed() -> discord.Embed:
        embed = discord.Embed(
            title="🍺 ▣ Taverna da Guilda",
            description=(
                "Converse.\n"
                "Compartilhe progresso.\n"
                "Conheça outros aventureiros.\n"
                "Faça networking.\n\n"
                "**Nada de dúvidas técnicas aqui.**"
            ),
            color=0x44D07B,
        )
        return embed

    @staticmethod
    def _find_category(guild: discord.Guild, names: tuple[str, ...]) -> discord.CategoryChannel | None:
        for name in names:
            channel = discord.utils.get(guild.categories, name=name)
            if channel:
                return channel
        return None

    @staticmethod
    def _find_text_channel(guild: discord.Guild, names: tuple[str, ...]) -> discord.TextChannel | None:
        for name in names:
            channel = discord.utils.get(guild.text_channels, name=name)
            if channel:
                return channel
        return None

    @staticmethod
    def _find_voice_channel(guild: discord.Guild, names: tuple[str, ...]) -> discord.VoiceChannel | None:
        for name in names:
            channel = discord.utils.get(guild.voice_channels, name=name)
            if channel:
                return channel
        return None

    @staticmethod
    def _overwrites(
        everyone_role: discord.Role,
        everyone_overwrite: discord.PermissionOverwrite,
        bot_member: discord.Member | None,
        bot_overwrite: discord.PermissionOverwrite | None,
    ) -> dict[discord.abc.Snowflake, discord.PermissionOverwrite]:
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] = {everyone_role: everyone_overwrite}
        if bot_member and bot_overwrite:
            overwrites[bot_member] = bot_overwrite
        return overwrites

    @staticmethod
    def _role_overwrites(
        *,
        everyone: discord.Role,
        role: discord.Role,
        member_overwrite: discord.PermissionOverwrite,
        bot_member: discord.Member | None,
    ) -> dict[discord.abc.Snowflake, discord.PermissionOverwrite]:
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            role: member_overwrite,
        }
        if bot_member:
            overwrites[bot_member] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
                use_application_commands=True,
                connect=True,
                speak=True,
            )
        return overwrites

    @staticmethod
    def _voice_overwrites(
        everyone: discord.Role,
        role: discord.Role,
        *,
        can_speak: bool,
        bot_member: discord.Member | None,
    ) -> dict[discord.abc.Snowflake, discord.PermissionOverwrite]:
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            role: discord.PermissionOverwrite(view_channel=True, connect=True, speak=can_speak),
        }
        if bot_member:
            overwrites[bot_member] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)
        return overwrites
