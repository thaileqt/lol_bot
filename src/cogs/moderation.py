import hikari
import lightbulb


moderation_plugin = lightbulb.Plugin("Moderation")

@moderation_plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option('user', 'The user to kick', type=hikari.User)
@lightbulb.command("kick", "Kick a user from the server")
@lightbulb.implements(lightbulb.SlashCommand)
async def kick(ctx: lightbulb.Context) -> None:
    user = ctx.options.user
    guild = ctx.get_guild()

    if guild is not None and user is not None:
        await guild.kick(user)
        await ctx.respond(f"Kicked {user.username} from the server.")
    else:
        await ctx.respond("Failed to kick user.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(moderation_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(moderation_plugin)
