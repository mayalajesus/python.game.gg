from __future__ import annotations

import discord

from python_game.ranks import RANKS, rank_for_xp


async def ensure_rank_roles(guild: discord.Guild) -> dict[str, discord.Role]:
    roles: dict[str, discord.Role] = {}
    for rank in RANKS:
        role = discord.utils.get(guild.roles, name=rank.role_name)
        if role is None:
            role = await guild.create_role(name=rank.role_name, reason="python.game rank setup")
        roles[rank.role_name] = role
    return roles


async def sync_member_rank(member: discord.Member, xp: int) -> str:
    guild = member.guild
    roles = await ensure_rank_roles(guild)
    target_rank = rank_for_xp(xp)
    rank_roles = set(roles.values())
    roles_to_remove = [role for role in member.roles if role in rank_roles and role.name != target_rank.role_name]
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove, reason="python.game rank sync")
    target_role = roles[target_rank.role_name]
    if target_role not in member.roles:
        await member.add_roles(target_role, reason="python.game rank sync")
    return target_rank.role_name


def require_guild(interaction: discord.Interaction) -> discord.Guild:
    if interaction.guild is None:
        raise RuntimeError("Este comando so funciona dentro de um servidor.")
    return interaction.guild


def require_member(interaction: discord.Interaction) -> discord.Member:
    if not isinstance(interaction.user, discord.Member):
        raise RuntimeError("Nao foi possivel identificar o membro no servidor.")
    return interaction.user

