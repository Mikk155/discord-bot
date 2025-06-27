from src.main import *;

@bot.event
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):

    await g_PluginManager.CallFunction( "OnReaction", reaction, 0, user, GuildID=reaction.guild.id );
