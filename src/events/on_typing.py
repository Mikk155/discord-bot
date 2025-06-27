from src.main import *;

from datetime import datetime;

@bot.event
async def on_typing( channel: discord.TextChannel | discord.GroupChannel | discord.DMChannel, user: discord.Member | discord.User, when: datetime ):

    await g_PluginManager.CallFunction( "OnTyping", channel, user, when, GuildID=channel.guild.id );
