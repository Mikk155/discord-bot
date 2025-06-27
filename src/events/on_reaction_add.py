from src.main import *;

@bot.event
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):

    await g_PluginManager.CallFunction( "OnReaction", reaction, 1, user, GuildID=reaction.guild.id );
