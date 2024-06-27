import logging
import lightbulb
from src.process_data import process_rank_data
from src.match_data import MatchData
import hikari
import os

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("Check")


@plugin.command()
@lightbulb.command("ping", "check_ping")
@lightbulb.implements(lightbulb.PrefixCommand)
async def check_ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")


@plugin.command()
@lightbulb.option("name", "The characters to get the information on.", type=str)
@lightbulb.command("checkrank", "Check rank of a user", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_rank(ctx: lightbulb.Context) -> None:
    summonerName = ctx.options.name
    data = process_rank_data(summonerName)
    await ctx.respond(data)


# @plugin.command()
# @lightbulb.option("name", "The characters to get the information on.", type=str)
# @lightbulb.command("checkqueue", "Check rank of all players in queue", auto_defer=True)
# @lightbulb.implements(lightbulb.SlashCommand)
# async def check_queue(ctx: lightbulb.Context) -> None:
#     summonerName = ctx.options.name
#     data = process_match_data(summonerName)
#     await ctx.respond(data)


@plugin.command()
@lightbulb.option("name", "The characters to get the information on.", type=str)
@lightbulb.command("checkqueue", "Check rank of all players in queue", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_queue_img(ctx: lightbulb.Context) -> None:
    card = MatchData(ctx.options.name)
    card_path = "card.png"
    if not os.path.exists(card_path):
        await ctx.respond("Player or Match not found!")
    else:
        with open(card_path, "rb") as image:
            f = image.read()
            b = bytearray(f)

        await ctx.respond(attachment=hikari.files.Bytes(b, 'card.png'))
        os.remove(card_path)
    # remove the image after sending





def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)

if __name__ == "__main__":
    print(process_rank_data("Ola#4498"))