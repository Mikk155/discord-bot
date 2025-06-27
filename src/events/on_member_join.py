from src.main import *;

@bot.event
async def on_member_join( member : discord.Member ):

    await g_PluginManager.CallFunction( "OnMemberJoin", member, GuildID=member.guild.id );
