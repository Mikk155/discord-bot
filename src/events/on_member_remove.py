from src.main import *;

@bot.event
async def on_member_remove( member : discord.Member ):

    await g_PluginManager.CallFunction( "OnMemberLeave", member, GuildID=member.guild.id );
