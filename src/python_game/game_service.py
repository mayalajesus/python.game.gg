from __future__ import annotations

from dataclasses import dataclass

import discord

from python_game.content_repository import ContentRepository, TrailContent
from python_game.database import GameDatabase, Player
from python_game.discord_helpers import grant_access_role, sync_member_rank
from python_game.ranks import RANKS, rank_for_xp


INITIAL_XP = 10


@dataclass(frozen=True)
class JourneyStart:
    player: Player
    content: TrailContent
    is_new_player: bool
    xp_awarded: int


async def start_player_journey(
    *,
    member: discord.Member,
    contents: ContentRepository,
    database: GameDatabase,
    hero_name: str | None = None,
) -> JourneyStart:
    selected_name = (hero_name or member.display_name).strip()[:40]
    first_content_id = contents.first_content_id()
    existing = database.get_player(member.id, member.guild.id)

    player = database.upsert_player(
        discord_id=member.id,
        guild_id=member.guild.id,
        display_name=member.display_name,
        hero_name=selected_name,
        rank_role=RANKS[0].role_name,
        active_content_id=first_content_id,
    )

    await grant_access_role(member)

    xp_awarded = 0
    if existing is None:
        xp_awarded = INITIAL_XP
        player = database.add_xp(
            discord_id=member.id,
            guild_id=member.guild.id,
            amount=INITIAL_XP,
            reason="Entrada na Guilda",
            content_id=first_content_id,
            rank_role=rank_for_xp(INITIAL_XP).role_name,
        )

    rank_role = await sync_member_rank(member, player.xp)
    if rank_role != player.rank_role:
        player = database.add_xp(
            discord_id=member.id,
            guild_id=member.guild.id,
            amount=0,
            reason="rank sync",
            rank_role=rank_role,
        )

    content = contents.get_content(player.active_content_id or first_content_id)
    return JourneyStart(player=player, content=content, is_new_player=existing is None, xp_awarded=xp_awarded)
