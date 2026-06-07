from __future__ import annotations

import discord

from python_game.content_repository import ContentRepository, TrailContent, has_recommendation_links, primary_recommendation
from python_game.database import GameDatabase
from python_game.embeds import mission_embed
from python_game.game_service import start_player_journey


class PortalView(discord.ui.View):
    def __init__(self, *, label: str, emoji: str, url: str) -> None:
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label=label, emoji=emoji, style=discord.ButtonStyle.link, url=url))


class StartJourneyView(discord.ui.View):
    def __init__(self, contents: ContentRepository, database: GameDatabase) -> None:
        super().__init__(timeout=None)
        self.contents = contents
        self.database = database

    @discord.ui.button(
        label="Tornar-se Aprendiz",
        emoji="⚔️",
        style=discord.ButtonStyle.success,
        custom_id="python_game:start_journey",
    )
    async def start_journey(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("Este portal só abre dentro da Guilda.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        result = await start_player_journey(
            member=interaction.user,
            contents=self.contents,
            database=self.database,
        )

        trail_channel = self._configured_text_channel(interaction.guild, "trail", "🧩-trilha-python")
        trail_hint = trail_channel.mention if trail_channel else "#🧩-trilha-python"
        dm_delivered = await self._send_welcome_dm(interaction.user, trail_hint, result.content)
        if result.is_new_player:
            await self._announce_new_apprentice(interaction.guild, interaction.user, result.player.hero_name)

        intro = "Seu registro foi aceso no Livro da Guilda." if result.is_new_player else "Seu registro já estava aceso."
        xp_line = f"⭐ XP inicial recebido: **+{result.xp_awarded} XP**" if result.xp_awarded else "⭐ XP inicial já registrado."
        dm_line = "📬 Enviei o chamado inicial por DM." if dm_delivered else "📬 Sua DM está fechada, mas a missão já foi liberada aqui."

        await interaction.followup.send(
            (
                f"🏰 **{result.player.hero_name}, você agora é Aprendiz da Python.Game.**\n\n"
                f"{intro}\n"
                f"🎒 Cargo liberado: **Aprendiz**\n"
                f"{xp_line}\n"
                f"📜 Primeira missão: {trail_hint}\n"
                f"{dm_line}"
            ),
            embed=mission_embed(result.content, has_recommendation_links(result.content)),
            ephemeral=True,
        )

    async def _send_welcome_dm(self, member: discord.Member, trail_hint: str, content: TrailContent) -> bool:
        recommendation = primary_recommendation(content)
        material_line = f"\n\nPrimeiro recurso:\n{recommendation}" if recommendation else ""
        try:
            await member.send(
                "🏰 **Bem-vindo à Guilda.**\n\n"
                f"Sua primeira missão já está disponível em:\n{trail_hint}\n\n"
                f"Missão ativa: **{content.title}**{material_line}\n\n"
                "Boa sorte, aventureiro."
            )
        except discord.HTTPException:
            return False
        return True

    async def _announce_new_apprentice(self, guild: discord.Guild, member: discord.Member, hero_name: str) -> None:
        channel = self._configured_text_channel(guild, "announcements", "📜-conquistas")
        if channel is None:
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

    def _configured_text_channel(self, guild: discord.Guild, key: str, fallback_name: str) -> discord.TextChannel | None:
        settings = self.database.guild_settings(guild.id)
        channel_id = settings.get(key)
        channel = guild.get_channel(channel_id) if channel_id else None
        if isinstance(channel, discord.TextChannel):
            return channel
        fallback = discord.utils.get(guild.text_channels, name=fallback_name)
        return fallback if isinstance(fallback, discord.TextChannel) else None


class MissionFeedView(discord.ui.View):
    def __init__(self, database: GameDatabase, contents: ContentRepository | None = None) -> None:
        super().__init__(timeout=None)
        self.database = database
        self.contents = contents

    @discord.ui.button(
        label="Concluir Missão",
        emoji="✅",
        style=discord.ButtonStyle.primary,
        custom_id="python_game:mission_delivery_help",
    )
    async def delivery_help(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("Use este botão dentro da Guilda.", ephemeral=True)
            return

        settings = self.database.guild_settings(interaction.guild.id)
        channel_id = settings.get("deliveries")
        channel = interaction.guild.get_channel(channel_id) if channel_id else None
        delivery_hint = channel.mention if isinstance(channel, discord.TextChannel) else "#📦-entregas"
        challenge_id = "ambiente_desenvolvimento"
        if isinstance(interaction.user, discord.Member):
            player = self.database.get_player(interaction.user.id, interaction.guild.id)
            if player and player.active_content_id:
                challenge_id = (
                    self.contents.safe_content_id(player.active_content_id)
                    if self.contents
                    else player.active_content_id
                )

        await interaction.response.send_message(
            (
                f"📦 Para concluir, registre sua entrega em {delivery_hint} e depois envie para correção.\n\n"
                "**1. Registro social no canal:**\n"
                "```text\n"
                f"Missão: {challenge_id}\n"
                "Github: sem repositorio\n"
                "Observações: instalei o ambiente e validei as ferramentas.\n"
                "```\n"
                "**2. Correção e XP:** use `/entregar` com o mesmo `desafio_id`, suas evidências no campo `codigo` "
                "e um checklist no campo `explicacao`."
            ),
            ephemeral=True,
        )
