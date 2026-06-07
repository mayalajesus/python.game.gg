from __future__ import annotations

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands

from python_game.database import GameDatabase
from python_game.discord_helpers import require_guild


@dataclass(frozen=True)
class ModerationDecision:
    action: str
    reason: str
    delete_message: bool = True
    timeout_minutes: int = 0


class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot, database: GameDatabase) -> None:
        self.bot = bot
        self.database = database
        self.message_windows: dict[tuple[int, int], deque[tuple[datetime, str]]] = defaultdict(deque)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.guild is None or message.author.bot:
            return
        if not isinstance(message.author, discord.Member):
            return
        if message.author.guild_permissions.manage_messages:
            return

        decision = self._inspect_message(message)
        if decision is None:
            return

        await self._apply_decision(message, decision)

    @app_commands.command(name="mod_status", description="Mostra o historico recente de moderacao de um membro.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def mod_status(self, interaction: discord.Interaction, membro: discord.Member) -> None:
        guild = require_guild(interaction)
        events = self.database.moderation_events_for_user(guild.id, membro.id)
        if not events:
            await interaction.response.send_message(
                f"O registro disciplinar de {membro.mention} esta limpo.",
                ephemeral=True,
            )
            return

        lines = [f"🛡️ **Registro disciplinar: {membro.display_name}**"]
        for event in events:
            lines.append(f"- `{event['created_at']}` {event['action']}: {event['reason']}")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @app_commands.command(name="mod_limpar", description="Remove mensagens recentes de um canal.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def mod_limpar(self, interaction: discord.Interaction, quantidade: app_commands.Range[int, 1, 50]) -> None:
        if not isinstance(interaction.channel, discord.TextChannel | discord.Thread):
            await interaction.response.send_message("Este comando so funciona em canais de texto.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True, thinking=True)
        deleted = await interaction.channel.purge(limit=quantidade)
        await interaction.followup.send(f"O canal foi varrido. Mensagens removidas: {len(deleted)}", ephemeral=True)

    def _inspect_message(self, message: discord.Message) -> ModerationDecision | None:
        content = message.content.strip()
        normalized = self._normalize(content)
        now = datetime.now(UTC)
        key = (message.guild.id, message.author.id)
        window = self.message_windows[key]
        window.append((now, normalized))
        while window and now - window[0][0] > timedelta(seconds=20):
            window.popleft()

        recent_8s = [entry for entry in window if now - entry[0] <= timedelta(seconds=8)]
        same_recent = [entry for entry in window if entry[1] == normalized and normalized]

        if len(recent_8s) >= 6:
            return ModerationDecision("spam", "Muitas mensagens em poucos segundos.")
        if len(same_recent) >= 3:
            return ModerationDecision("spam_repetido", "Mensagem repetida muitas vezes.")
        if len(message.mentions) + len(message.role_mentions) >= 6:
            return ModerationDecision("mention_spam", "Excesso de mencoes na mesma mensagem.")
        if self._has_invite_spam(content):
            return ModerationDecision("invite_spam", "Convite externo detectado fora do fluxo da Guilda.")
        if self._has_link_burst(content, window):
            return ModerationDecision("link_spam", "Muitos links enviados em sequencia.")
        return None

    async def _apply_decision(self, message: discord.Message, decision: ModerationDecision) -> None:
        guild = message.guild
        member = message.author
        permissions = message.channel.permissions_for(guild.me) if guild.me else None

        if decision.delete_message and permissions and permissions.manage_messages:
            try:
                await message.delete()
            except discord.HTTPException:
                pass

        total_events = self.database.moderation_event_count(guild.id, member.id)
        timeout_minutes = 0
        if total_events >= 2:
            timeout_minutes = 5
        if total_events >= 5:
            timeout_minutes = 30

        if timeout_minutes and guild.me and guild.me.guild_permissions.moderate_members:
            try:
                await member.timeout(
                    datetime.now(UTC) + timedelta(minutes=timeout_minutes),
                    reason=f"python.game anti-spam: {decision.reason}",
                )
                decision = ModerationDecision(
                    action="timeout",
                    reason=f"{decision.reason} Timeout aplicado por {timeout_minutes} minutos.",
                    delete_message=decision.delete_message,
                    timeout_minutes=timeout_minutes,
                )
            except discord.HTTPException:
                pass

        self.database.add_moderation_event(
            guild_id=guild.id,
            discord_id=member.id,
            action=decision.action,
            reason=decision.reason,
            message_excerpt=message.content,
        )

        try:
            await member.send(
                "🛡️ **Aviso da Guarda da Guilda**\n\n"
                f"Sua mensagem foi sinalizada por: {decision.reason}\n"
                "Mantenha a campanha fluindo: sem flood, repeticao excessiva ou mencoes em massa. "
                "A comunidade cresce melhor quando o canal continua legivel para todos."
            )
        except discord.HTTPException:
            pass

    @staticmethod
    def _normalize(content: str) -> str:
        return re.sub(r"\s+", " ", content.lower()).strip()

    @staticmethod
    def _has_invite_spam(content: str) -> bool:
        return bool(re.search(r"(discord\.gg/|discord\.com/invite/)", content, re.IGNORECASE))

    @staticmethod
    def _has_link_burst(content: str, window: deque[tuple[datetime, str]]) -> bool:
        if not re.search(r"https?://", content, re.IGNORECASE):
            return False
        link_messages = [entry for entry in window if re.search(r"https?://", entry[1], re.IGNORECASE)]
        return len(link_messages) >= 3
