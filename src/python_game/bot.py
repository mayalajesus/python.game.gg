from __future__ import annotations

import asyncio
import logging

import discord
from discord.ext import commands

from python_game.cogs.onboarding import OnboardingCog
from python_game.cogs.setup import SetupCog
from python_game.cogs.trail import TrailCog
from python_game.content_repository import ContentRepository
from python_game.database import GameDatabase
from python_game.settings import load_settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("python_game")


class PythonGameBot(commands.Bot):
    def __init__(self) -> None:
        settings = load_settings()
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=settings.command_prefix, intents=intents)

        self.settings = settings
        self.contents = ContentRepository(settings.content_index_path)
        self.database = GameDatabase(settings.database_path)

    async def setup_hook(self) -> None:
        await self.add_cog(SetupCog(self, self.database))
        await self.add_cog(OnboardingCog(self, self.contents, self.database))
        await self.add_cog(TrailCog(self, self.contents, self.database))

        if self.settings.discord_guild_id:
            guild = discord.Object(id=int(self.settings.discord_guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info("Slash commands sincronizados para a guild %s", self.settings.discord_guild_id)
            return

        await self.tree.sync()

    async def on_ready(self) -> None:
        logger.info("Bot conectado como %s", self.user)


async def main() -> None:
    bot = PythonGameBot()
    if not bot.settings.discord_bot_token:
        raise RuntimeError("DISCORD_BOT_TOKEN nao configurado. Preencha a .env antes de iniciar o bot.")

    async with bot:
        await bot.start(bot.settings.discord_bot_token)


if __name__ == "__main__":
    asyncio.run(main())
