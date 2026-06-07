from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from python_game.content_repository import ContentRepository, format_recommendations, has_recommendation_links
from python_game.database import GameDatabase
from python_game.delivery_validation import validate_delivery_format
from python_game.discord_helpers import require_guild, require_member, sync_member_rank
from python_game.embeds import feedback_embed, mission_embed
from python_game.evaluator import evaluate_submission
from python_game.ranks import rank_for_xp


class TrailCog(commands.Cog):
    def __init__(self, bot: commands.Bot, contents: ContentRepository, database: GameDatabase) -> None:
        self.bot = bot
        self.contents = contents
        self.database = database

    @app_commands.command(name="trilha", description="Lista os conteudos cadastrados na trilha.")
    async def trilha(self, interaction: discord.Interaction) -> None:
        contents = self.contents.list_contents()
        lines = ["🐍 **Mapa da trilha python.game**"]
        for item in contents[:15]:
            lines.append(f"- `{item['id']}` - {item['titulo']}")
        if len(contents) > 15:
            lines.append(f"...e mais {len(contents) - 15} conteudos.")
        lines.append("")
        lines.append("Use `/missao id:<id>` para ativar uma missao ou `/conteudo id:<id>` para ver materiais.")
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
                f"Conteudo nao encontrado: `{content_id}`.",
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
            await interaction.response.send_message("Use `/iniciar` antes de abrir missoes.", ephemeral=True)
            return

        content_id = id or player.active_content_id or self.contents.first_content_id()
        try:
            content = self.contents.get_content(content_id)
        except KeyError:
            await interaction.response.send_message(f"Missao nao encontrada: `{content_id}`.", ephemeral=True)
            return

        self.database.set_active_content(member.id, guild.id, content.id)
        await interaction.response.send_message(
            "🗺️ Missao ativa atualizada.",
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
            await interaction.response.send_message("Use `/iniciar` antes de entregar missoes.", ephemeral=True)
            return

        try:
            content = self.contents.get_content(desafio_id)
        except KeyError:
            await interaction.response.send_message(f"Missao nao encontrada: `{desafio_id}`.", ephemeral=True)
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
                new_rank_message = f"\n🏅 Novo rank sincronizado: **{synced_rank}**"
            next_content_id = self.contents.next_content_id(content.id)
            if next_content_id:
                self.database.set_active_content(member.id, guild.id, next_content_id)

        embed = feedback_embed(
            content.title,
            evaluation.score,
            evaluation.accepted,
            evaluation.strengths,
            evaluation.improvements,
        )
        reward = f"\nXP recebido: **+{xp_awarded}**" if xp_awarded else "\nXP recebido: **+0**"
        await interaction.response.send_message(
            evaluation.feedback + reward + new_rank_message,
            embed=embed,
            ephemeral=True,
        )

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
            await interaction.response.send_message("Ainda nao ha aventureiros no ranking. Use `/iniciar`.", ephemeral=True)
            return
        lines = ["🏆 **Ranking da Guilda**"]
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
            await interaction.response.send_message("Use `/iniciar` antes de registrar projetos.", ephemeral=True)
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
            f"📦 Projeto registrado no portfolio: **{titulo}**\nXP recebido: **+50**",
            ephemeral=True,
        )

    @app_commands.command(name="portfolio", description="Mostra seus projetos registrados.")
    async def portfolio(self, interaction: discord.Interaction) -> None:
        guild = require_guild(interaction)
        member = require_member(interaction)
        projects = self.database.portfolio(member.id, guild.id)
        if not projects:
            await interaction.response.send_message("Seu portfolio interno ainda esta vazio.", ephemeral=True)
            return
        lines = [f"📦 **Portfolio de {member.display_name}**"]
        for project in projects[:10]:
            lines.append(f"- **{project['title']}** (`{project['content_id']}`): {project['repository_url']}")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return
        if not message.content.strip().lower().startswith("/entregar"):
            return
        result = validate_delivery_format(message.content)
        if not result.is_valid:
            await message.reply(f"⚠️ {result.message}", mention_author=False)
            return
        await message.reply(
            "✅ Formato validado. Para registrar XP e feedback completo, use o comando slash `/entregar`.",
            mention_author=False,
        )
