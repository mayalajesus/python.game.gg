from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands


class OnboardingCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="iniciar", description="Inicia sua jornada na Guilda python.game.")
    async def iniciar(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            (
                "🥚 Bem-vindo a Guilda, Novato!\n\n"
                "Sua jornada comeca agora. Leia as instrucoes, conclua o onboarding "
                "e use `/trilha` para ver os proximos conteudos."
            ),
            ephemeral=True,
        )

    @app_commands.command(name="formato", description="Mostra o modelo correto de entrega.")
    async def formato(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            (
                "Envie suas entregas neste modelo:\n\n"
                "````text\n"
                "/entregar desafio_id: fundamentos_01\n\n"
                "Codigo:\n"
                "```python\n"
                "seu codigo aqui\n"
                "```\n\n"
                "Explicacao:\n"
                "Explique em poucas linhas como sua solucao funciona.\n"
                "````"
            ),
            ephemeral=True,
        )

