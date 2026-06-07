from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands, tasks

from python_game.content_repository import ContentRepository, TrailContent, format_recommendations, has_recommendation_links
from python_game.database import GameDatabase
from python_game.delivery_validation import validate_delivery_format
from python_game.discord_helpers import require_guild, require_member, sync_member_rank
from python_game.embeds import feedback_embed, mission_embed
from python_game.evaluator import evaluate_submission
from python_game.ranks import rank_for_xp
from python_game.views import MissionFeedView


class TrailCog(commands.Cog):
    def __init__(self, bot: commands.Bot, contents: ContentRepository, database: GameDatabase) -> None:
        self.bot = bot
        self.contents = contents
        self.database = database
        self.refresh_rankings.start()

    def cog_unload(self) -> None:
        self.refresh_rankings.cancel()

    @tasks.loop(hours=24)
    async def refresh_rankings(self) -> None:
        for guild in self.bot.guilds:
            await self._publish_ranking_board(guild)

    @refresh_rankings.before_loop
    async def before_refresh_rankings(self) -> None:
        await self.bot.wait_until_ready()

    @app_commands.command(name="trilha", description="Lista os conteudos cadastrados na trilha.")
    async def trilha(self, interaction: discord.Interaction) -> None:
        contents = self.contents.list_contents()
        lines = ["🐍 **Mapa da Campanha Python**"]
        for item in contents[:15]:
            lines.append(f"- `{item['id']}` - {item['titulo']}")
        if len(contents) > 15:
            lines.append(f"...e mais {len(contents) - 15} capitulos aguardando no mapa.")
        lines.append("")
        lines.append("Use `/missao id:<id>` para acender um capitulo no seu mapa.")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @app_commands.command(name="conteudo", description="Mostra recomendacoes cadastradas para um conteudo.")
    async def conteudo(self, interaction: discord.Interaction, id: str | None = None) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        player = self.database.get_player(member.id, guild.id)
        content_id = id or (player.active_content_id if player else None) or self.contents.first_content_id()
        try:
            content = self.contents.get_content(content_id)
        except KeyError:
            await interaction.response.send_message(
                f"A biblioteca nao encontrou esse selo de missao: `{content_id}`.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(format_recommendations(content), ephemeral=True)

    @app_commands.command(name="missao", description="Mostra ou ativa uma missao da trilha.")
    async def missao(self, interaction: discord.Interaction, id: str | None = None) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        player = self.database.get_player(member.id, guild.id)
        if player is None:
            await interaction.response.send_message(
                "Antes de abrir o mapa, grave seu nome no Registro da Guilda com `/iniciar`.",
                ephemeral=True,
            )
            return

        content_id = id or player.active_content_id or self.contents.first_content_id()
        try:
            content = self.contents.get_content(content_id)
        except KeyError:
            await interaction.response.send_message(f"Nenhum capitulo encontrado com o selo `{content_id}`.", ephemeral=True)
            return

        self.database.set_active_content(member.id, guild.id, content.id)
        await interaction.response.send_message(
            "🗺️ O mapa foi atualizado. Este e o seu capitulo ativo.",
            embed=mission_embed(content, has_recommendation_links(content)),
            ephemeral=True,
        )

    @app_commands.command(name="entregar", description="Envia uma solucao para avaliacao e XP.")
    async def entregar(
        self,
        interaction: discord.Interaction,
        desafio_id: str,
        codigo: str,
        explicacao: str,
        repositorio: str | None = None,
    ) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        player = self.database.get_player(member.id, guild.id)
        if player is None:
            await interaction.response.send_message(
                "A Guilda ainda nao reconhece seu nome. Use `/iniciar` antes de entregar missoes.",
                ephemeral=True,
            )
            return

        try:
            content = self.contents.get_content(desafio_id)
        except KeyError:
            await interaction.response.send_message(f"O selo `{desafio_id}` nao existe no mapa da Guilda.", ephemeral=True)
            return

        evaluation = evaluate_submission(content, codigo, explicacao)
        submission = self.database.record_submission(
            discord_id=member.id,
            guild_id=guild.id,
            content_id=content.id,
            code=codigo,
            explanation=explicacao,
            repository_url=repositorio,
            score=evaluation.score,
            accepted=evaluation.accepted,
            feedback=evaluation.feedback,
        )

        xp_awarded = 0
        new_rank_message = ""
        next_content = None
        if evaluation.accepted and submission.first_completion:
            xp_awarded = int(content.raw.get("xp_sugerido", 100))
            updated = self.database.add_xp(
                discord_id=member.id,
                guild_id=guild.id,
                amount=xp_awarded,
                reason=f"Missao concluida: {content.id}",
                content_id=content.id,
                rank_role=rank_for_xp(player.xp + xp_awarded).role_name,
            )
            synced_rank = await sync_member_rank(member, updated.xp)
            if synced_rank != player.rank_role:
                new_rank_message = f"\n🏅 Novo rank conquistado: **{synced_rank}**"
            next_content_id = self.contents.next_content_id(content.id)
            if next_content_id:
                next_content = self.contents.get_content(next_content_id)
                self.database.set_active_content(member.id, guild.id, next_content_id)

        embed = feedback_embed(
            content.title,
            evaluation.score,
            evaluation.accepted,
            evaluation.strengths,
            evaluation.improvements,
        )
        reward = f"\nRecompensa registrada: **+{xp_awarded} XP**" if xp_awarded else "\nRecompensa registrada: **+0 XP**"
        await interaction.response.send_message(
            evaluation.feedback + reward + new_rank_message,
            embed=embed,
            ephemeral=True,
        )
        if evaluation.accepted and submission.first_completion:
            await self._publish_achievement(guild, member, content.title, xp_awarded)
            await self._publish_ranking_board(guild)
            if next_content:
                await self._publish_mission_feed(guild, next_content)

    @app_commands.command(name="validar_entrega", description="Valida se uma entrega textual esta no formato correto.")
    async def validar_entrega(self, interaction: discord.Interaction, texto: str) -> None:
        result = validate_delivery_format(texto)
        prefix = "✅" if result.is_valid else "⚠️"
        await interaction.response.send_message(f"{prefix} {result.message}", ephemeral=True)

    @app_commands.command(name="ranking", description="Mostra o ranking de XP da Guilda.")
    async def ranking(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        players = self.database.leaderboard(guild.id)
        if not players:
            await interaction.response.send_message(
                "O placar da Guilda ainda esta em branco. Use `/iniciar` para escrever o primeiro nome.",
                ephemeral=True,
            )
            return
        lines = ["🏆 **Placar da Guilda**"]
        for index, player in enumerate(players, start=1):
            lines.append(f"{index}. **{player.hero_name}** - {player.xp} XP - {player.rank_role}")
        await interaction.response.send_message("\n".join(lines), ephemeral=False)

    @app_commands.command(name="registrar_projeto", description="Adiciona um projeto ao seu portfolio interno.")
    async def registrar_projeto(
        self,
        interaction: discord.Interaction,
        titulo: str,
        repositorio: str,
        descricao: str,
        desafio_id: str | None = None,
    ) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        player = self.database.get_player(member.id, guild.id)
        if player is None:
            await interaction.response.send_message(
                "Antes de montar sua vitrine, entre na campanha com `/iniciar`.",
                ephemeral=True,
            )
            return
        content_id = desafio_id or player.active_content_id or self.contents.first_content_id()
        self.database.add_project(
            discord_id=member.id,
            guild_id=guild.id,
            content_id=content_id,
            title=titulo,
            repository_url=repositorio,
            description=descricao,
        )
        updated = self.database.add_xp(
            discord_id=member.id,
            guild_id=guild.id,
            amount=50,
            reason=f"Projeto registrado: {titulo}",
            content_id=content_id,
            rank_role=rank_for_xp(player.xp + 50).role_name,
        )
        await sync_member_rank(member, updated.xp)
        await interaction.response.send_message(
            f"📦 **{titulo}** entrou na sua vitrine da Guilda.\nRecompensa registrada: **+50 XP**",
            ephemeral=True,
        )

        await self._publish_achievement(guild, member, f"Projeto publicado: {titulo}", 50)
        await self._publish_ranking_board(guild)

    @app_commands.command(name="portfolio", description="Mostra seus projetos registrados.")
    async def portfolio(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        projects = self.database.portfolio(member.id, guild.id)
        if not projects:
            await interaction.response.send_message(
                "Sua vitrine ainda esta vazia. Registre um projeto quando sua primeira entrega virar portfolio.",
                ephemeral=True,
            )
            return
        lines = [f"📦 **Vitrine de {member.display_name}**"]
        for project in projects[:10]:
            lines.append(f"- **{project['title']}** (`{project['content_id']}`): {project['repository_url']}")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    async def _publish_achievement(
        self,
        guild: discord.Guild,
        member: discord.Member,
        achievement_name: str,
        xp_awarded: int,
    ) -> None:
        channel = self._configured_text_channel(guild, "announcements")
        if channel is None:
            return

        embed = discord.Embed(
            title="🏆 Conquista Desbloqueada",
            description=(
                f"**Usuário:**\n{member.mention}\n\n"
                f"**Conquista:**\n{achievement_name}\n\n"
                f"**Descrição:**\nConcluiu uma etapa da campanha e fortaleceu o próprio portfólio.\n\n"
                f"**Recompensa:**\n+{xp_awarded} XP"
            ),
            color=0xF2C94C,
        )
        embed.set_footer(text="python.game.gg • conquista")
        await channel.send(embed=embed)

    async def _publish_ranking_board(self, guild: discord.Guild) -> None:
        channel = self._configured_text_channel(guild, "ranking")
        if channel is None:
            return

        players = self.database.leaderboard(guild.id)
        lines = ["**Ranking da Guilda**"]
        if players:
            medals = ("🥇", "🥈", "🥉")
            for index, player in enumerate(players[:10], start=1):
                prefix = medals[index - 1] if index <= len(medals) else f"{index}."
                lines.append(f"{prefix} **{player.hero_name}** — {player.xp} XP")
        else:
            lines.extend(
                [
                    "🥇 Aguardando o primeiro nome",
                    "🥈 Aguardando o próximo avanço",
                    "🥉 Aguardando uma nova conquista",
                ]
            )

        permissions = channel.permissions_for(guild.me) if guild.me else None
        if permissions and permissions.manage_messages:
            try:
                await channel.purge(
                    limit=50,
                    check=lambda message: (
                        message.author == guild.me
                        and bool(message.embeds)
                        and message.embeds[0].footer.text in {"python.game.gg • ranking", "python.game.gg • setup"}
                    ),
                )
            except discord.HTTPException:
                pass

        embed = discord.Embed(title="🏆 ▣ Ranking da Guilda", description="\n".join(lines), color=0xF2C94C)
        embed.set_footer(text="python.game.gg • ranking")
        await channel.send(embed=embed)

    async def _publish_mission_feed(self, guild: discord.Guild, content: TrailContent) -> None:
        channel = self._configured_text_channel(guild, "trail")
        if channel is None:
            return

        marker = f"python.game.gg • mission:{content.id}"
        async for message in channel.history(limit=75):
            if message.author == guild.me and message.embeds and message.embeds[0].footer.text == marker:
                return

        embed = self._mission_feed_embed(content)
        embed.set_footer(text=marker)
        await channel.send(embed=embed, view=MissionFeedView(self.database))

    def _configured_text_channel(self, guild: discord.Guild, key: str) -> discord.TextChannel | None:
        settings = self.database.guild_settings(guild.id)
        channel_id = settings.get(key)
        channel = guild.get_channel(channel_id) if channel_id else None
        return channel if isinstance(channel, discord.TextChannel) else None

    @staticmethod
    def _mission_feed_embed(content: TrailContent) -> discord.Embed:
        mission_number = max(1, content.order + 1)
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return
        if self._is_delivery_channel(message) and self._looks_like_delivery_card(message.content):
            await message.reply(
                "📦 Entrega recebida no modelo da Guilda. Para correção técnica, XP e progressão automática, use também `/entregar`.",
                mention_author=False,
            )
            return
        if not message.content.strip().lower().startswith("/entregar"):
            return
        result = validate_delivery_format(message.content)
        if not result.is_valid:
            await message.reply(f"⚠️ {result.message}", mention_author=False)
            return
        await message.reply(
            "✅ O selo de formato esta correto. Para registrar XP e receber feedback completo, use o comando slash `/entregar`.",
            mention_author=False,
        )

    def _is_delivery_channel(self, message: discord.Message) -> bool:
        if message.guild is None:
            return False
        settings = self.database.guild_settings(message.guild.id)
        return settings.get("deliveries") == message.channel.id

    @staticmethod
    def _looks_like_delivery_card(content: str) -> bool:
        normalized = content.lower()
        return (
            ("missão:" in normalized or "missao:" in normalized)
            and "github:" in normalized
            and ("observações:" in normalized or "observacoes:" in normalized)
        )
