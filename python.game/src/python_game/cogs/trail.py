from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from python_game.content_repository import ContentRepository, format_recommendations
from python_game.delivery_validation import validate_delivery_format


class TrailCog(commands.Cog):
    def __init__(self, bot: commands.Bot, contents: ContentRepository) -> None:
        self.bot = bot
        self.contents = contents

    @app_commands.command(name="trilha", description="Lista os conteudos cadastrados na trilha.")
    async def trilha(self, interaction: discord.Interaction) -> None:
        contents = self.contents.list_contents()[:12]
        lines = ["🐍 Primeiros conteudos da trilha:"]
        lines.extend(f"- `{item['id']}` - {item['titulo']}" for item in contents)
        lines.append("")
        lines.append("Use `/conteudo id:<id_do_conteudo>` para ver recomendacoes.")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @app_commands.command(name="conteudo", description="Mostra recomendacoes cadastradas para um conteudo.")
    async def conteudo(self, interaction: discord.Interaction, id: str) -> None:
        try:
            content = self.contents.get_content(id)
        except KeyError:
            await interaction.response.send_message(
                f"Conteudo nao encontrado: `{id}`.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(format_recommendations(content), ephemeral=True)

    @app_commands.command(name="validar_entrega", description="Valida se uma entrega textual esta no formato correto.")
    async def validar_entrega(self, interaction: discord.Interaction, texto: str) -> None:
        result = validate_delivery_format(texto)
        prefix = "✅" if result.is_valid else "⚠️"
        await interaction.response.send_message(f"{prefix} {result.message}", ephemeral=True)

