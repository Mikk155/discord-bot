from plugins.main import *

hooks = [
    Hooks.on_member_join,
    Hooks.on_ready
];

RegisterHooks( plugin_name='thecult_shared_role', hook_list=hooks );

async def set_role( member: discord.Member ):

    if member:

        rol = discord.utils.get( bot.get_guild( config[ "mikkserver" ][ "ID" ] ).roles, name="The Cult Member" )

        if not rol in member.roles:

            await member.add_roles( rol )

            await bot.get_channel( config[ "mikkserver" ][ "USERS" ] ).send( f'{member.mention} is now a cult member <:elegant:1216204366349078631>\n' )

async def on_ready():

    for miembro in bot.get_guild( config[ "thecult" ][ "ID" ] ).members:

        member = bot.get_guild( config[ "mikkserver" ][ "ID" ] ).get_member( miembro.id )

        if member:

            await set_role( member )

async def on_member_join( member : discord.Member ):

    tcm = bot.get_guild( config[ "thecult" ][ "ID" ] ).get_member( member.id )

    lpm = bot.get_guild( config[ "mikkserver" ][ "ID" ] ).get_member( member.id )

    if tcm and lpm:

        await set_role( lpm )
