from src.main import *;

@bot.event
async def on_message_delete( message: discord.Message ):

    # -TODO Get audith log and pass on the deleter
    deleter = message.author;

    await g_PluginManager.CallFunction( "OnMessageDelete", message, deleter, GuildID=message.guild.id );
