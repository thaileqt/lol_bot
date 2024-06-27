

from fastapi import APIRouter
from src.api.models import *
from src.match_data import MatchData as LoLMatchData
from src.bot import bot

router = APIRouter(prefix="/api")

@router.get("/check_queue", response_model=MatchData)
async def check_queue(target_summoner: Summoner):
    return LoLMatchData(target_summoner.name)


@router.get("/list_servers", response_model=list[DiscordServer])
async def list_servers():
    print("Listing servers")
    print(bot.is_alive)
    servers = bot.cache.get_available_guilds_view()
    for g in servers:
        print(g)
        data = await bot.rest.fetch_guild(g)
        print(data)
    return [DiscordServer(id=1,
                          name="Test Server",
                          icon="https://cdn.discordapp.com/icons/123/abc.png",
                          owner_id=123,
                            region="US",
                            member_count=5,
                            created_at="2021-01-01",
                            joined_at="2021-01-01"),
            ]


