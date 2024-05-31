import os
import logging
from pathlib import Path
import hikari
import lightbulb
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hikari.events.base_events import EventT
from pytz import utc
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)

bot = lightbulb.BotApp(
    prefix="!",
    token=os.getenv("DISCORD_TOKEN"),
    intents=hikari.Intents.ALL,
    help_slash_command=True)

bot.d._dynamic = Path("./data/dynamic")
bot.d._static = bot.d._dynamic.parent / "static"
bot.d.scheduler = AsyncIOScheduler()
bot.d.scheduler.configure(timezone=utc)

bot.load_extensions_from("./extensions")


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.scheduler.start()
    bot.d.session = ClientSession(trust_env=True)
    log.info("AIOHTTP session started")


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.d.db.close()
    await bot.d.session.close()
    log.info("AIOHTTP session closed")
    bot.d.scheduler.shutdown()


@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[EventT]) -> None:
    raise event.exception



def run() -> None:
    if os.name != "nt":
        print("asd")
        import uvloop
        uvloop.install()

    bot.run()