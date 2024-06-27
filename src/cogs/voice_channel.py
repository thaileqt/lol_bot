import hikari
import lightbulb
from lightbulb import Plugin


CHANNEL_NAME = "Create Voice Channel"
voice_channel_plugin = Plugin("Voice Channel")



@voice_channel_plugin.listener(hikari.StartedEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    bot = voice_channel_plugin.bot
    async for guild in bot.rest.fetch_my_guilds():
        channels = await bot.rest.fetch_guild_channels(guild.id)
        voice_channels = next((channel for channel in channels if channel.name == CHANNEL_NAME
                               and isinstance(channel, hikari.GuildVoiceChannel)), None)
        if not voice_channels:
            await bot.rest.create_guild_voice_channel(guild.id, CHANNEL_NAME)
            print(f"Created voice channel in {guild.name}")

# on guild join
@voice_channel_plugin.listener(hikari.GuildAvailableEvent)
async def on_guild_available(event: hikari.GuildAvailableEvent) -> None:
    bot = voice_channel_plugin.bot
    channels = await bot.rest.fetch_guild_channels(event.guild_id)
    voice_channels = next((channel for channel in channels if channel.name == CHANNEL_NAME
                           and isinstance(channel, hikari.GuildVoiceChannel)), None)
    if not voice_channels:
        await bot.rest.create_guild_voice_channel(event.guild_id, CHANNEL_NAME)
        print(f"Created voice channel in {event.guild_id}")

@voice_channel_plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    if event.state.channel_id is None:
        return # user left the voice channel

    channel = await voice_channel_plugin.bot.rest.fetch_channel(event.state.channel_id)
    if channel.name == CHANNEL_NAME:
        guild_id = event.state.guild_id
        member = await voice_channel_plugin.bot.rest.fetch_member(guild_id, event.state.user_id)
        new_channel = await voice_channel_plugin.bot.rest.create_guild_voice_channel(guild_id, f"{member.username}'s Channel")
        await voice_channel_plugin.bot.rest.edit_member(guild_id, member.id, voice_channel=new_channel)
        print(f"Created voice channel for {member.username}")


def load(bot: lightbulb.BotApp) -> None:
    pass
    # bot.add_plugin(voice_channel_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    pass
    # bot.remove_plugin(voice_channel_plugin)