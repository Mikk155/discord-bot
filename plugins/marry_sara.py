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

class marry_sara( Plugin ):

    @property
    def GetDescription(self):
        return "Count how many times mikk confessed his love to the his goddess sara";

    async def OnMessage( self, message: discord.Message ) -> Hook:

        if message.author.id != 744768007892500481:
            return Hook.Continue;

        content: str = message.content.lower();

        if 'neko marry' in content:

            sare: discord.User = bot.get_guild( 744769532513615922 ).get_member( 746914044828450856 );

            if sare and sare in message.mentions:

                cache: Dictionary = g_Cache.Plugin;

                if cache.IsEmpty:
                    cache[ "times" ] = 95;

                cache[ "times" ] += 1;

                await bot.get_channel( message.channel.id ).send( "Mikk has confesed his love to Sare {} times.".format( cache[ "times" ] ), mention_author=False );

        return Hook.Continue;
