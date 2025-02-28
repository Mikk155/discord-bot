"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from src.main import *

def on_initialization() -> dict:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.
    '''

    __data__: dict = {};
    __data__["name"] = "The Cult Member Role";
    __data__["description"] = "Add The Cult Member role to users that exists in The Cult discord Server";
    __hooks__: list[Hooks] = [
        Hooks.on_start,
        Hooks.on_member_join,
        Hooks.on_member_remove
    ];
    __data__["hooks"] = __hooks__;

    return __data__;

global THE_CULT;
THE_CULT = 1216162825307820042;

global LIMITLESS_POTENTIAL;
LIMITLESS_POTENTIAL = 744769532513615922;

async def manage_role( member : discord.Member, add: bool = False ):

    rol = discord.utils.get( bot.get_guild( LIMITLESS_POTENTIAL ).roles, name="The Cult Member" );

    if rol:

        if add:

            if not rol in member.roles:

                await member.add_roles( rol );

                await bot.get_channel( 842174687445778483 ).send( f'{member.mention} is now a cult member <:elegant:1216204366349078631>\n' );

        elif rol in member.roles:

            await member.remove_roles( rol );

async def on_start() -> int:

    try:

        guild_tc = bot.get_guild( THE_CULT );
        guild_lp = bot.get_guild( LIMITLESS_POTENTIAL );

        if guild_tc and guild_lp:

            for member_lp in guild_lp.members:

                await manage_role( member_lp, True if guild_tc.get_member( member_lp.id ) else False );

    except Exception as e:

        g_Logger.debug( e );

    return HOOK_CONTINUE();

async def on_member_join( member : discord.Member ) -> int:

    guild = member.guild;

    if member.guild:

        if member.guild.id == LIMITLESS_POTENTIAL:

            guild_tc = bot.get_guild( THE_CULT );

            if guild_tc:

                if guild_tc.get_member( member.id ):
        
                    await manage_role( member, True );

    return HOOK_CONTINUE();

async def on_member_remove( member : discord.Member ) -> int:

    guild = member.guild;

    if member.guild:

        if member.guild.id == THE_CULT:

            guild_lp = bot.get_guild( LIMITLESS_POTENTIAL );

            if guild_lp:

                if guild_lp.get_member( member.id ):

                    await manage_role( member, False );

    return HOOK_CONTINUE();
