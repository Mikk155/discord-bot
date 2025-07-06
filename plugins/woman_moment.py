'''
MIT License

Copyright (c) 2025 Mikk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
'''

from project import *

import re;

class woman_moment( Plugin ):

    @property
    def GetName(self):
        return "Woman moment";

    @property
    def GetDescription(self):
        return "Keep track of how many times bunnt was foolish";

    async def OnCommand(self, message, command, args):

        if command != 'womanmoment' and command != 'wm':
            return True;

        await self.WomanMoment( message.guild );

        return False;

    async def OnMessage( self, message ):

        if message.author.id == bot.user.id:
            return True;

        if 'woman moment' in message.content.lower():

            await self.WomanMoment( message.guild );

        return True;

    async def WomanMoment( self, guild: discord.Guild ) -> None:

        bunnt: discord.User = guild.get_member( 740196277844967458 );

        if bunnt:

            cache = g_Cache.Get();

            number = cache.get( "moment", 0 );

            number = ( number + 1 );

            nombre_actual = bunnt.display_name;

            moment = re.sub( r'\d+', str(number), nombre_actual )

            if not str(number) in moment:

                moment = '{} {}'.format( moment, number );

            await bunnt.edit( nick=moment )

            cache[ "moment" ] = number;
