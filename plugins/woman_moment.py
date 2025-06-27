from src.main import *
from src.PluginManager import Plugin;

import re;

class woman_moment( Plugin ):

    def GetName(self):
        return "Woman moment";

    def GetDescription(self):
        return "Keep track of how many times bunnt was foolish";

    async def OnCommand(self, message, command, args):

        if command != 'womanmoment' and command != 'wm':
            return True;

        await self.WomanMoment( message.guild );

        return False;

    async def OnMessage( self, message ):

        if 'woman moment' in message.content.lower():

            await self.WomanMoment( message.guild );

        return True;

    async def WomanMoment( self, guild: discord.Guild ) -> None:

        bunnt: discord.User = guild.get_member( 740196277844967458 );

        if bunnt:

            cache = g_Cache.get();

            number = cache.get( "moment", 0 );

            number = ( number + 1 );

            nombre_actual = bunnt.display_name;

            moment = re.sub( r'\d+', str(number), nombre_actual )

            if not str(number) in moment:

                moment = '{} {}'.format( moment, number );

            await bunnt.edit( nick=moment )

            cache[ "moment" ] = number;
