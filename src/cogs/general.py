import lightbulb


general_plugin = lightbulb.Plugin("General")

@general_plugin.command()
@lightbulb.command("ping", "Check the bot's latency")
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! {ctx.bot.heartbeat_latency * 1000:.0f}ms")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(general_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(general_plugin)