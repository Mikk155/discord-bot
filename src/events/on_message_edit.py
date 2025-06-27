from src.main import *;

@bot.event
async def on_message_edit( before: discord.Message, after: discord.Message ):

    await g_PluginManager.CallFunction( "OnMessageEdited", before, after, GuildID=message.guild.id );
