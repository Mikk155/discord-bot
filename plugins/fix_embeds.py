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

import asyncio;

class fix_embeds( Plugin ):

    def OnPluginActivate(self):

        g_Sentences.push_back( "fix_embeds" );

    @property
    def GetName(self):
        return "Fix embeds";

    @property
    def GetDescription(self):
        return "Create a fixed embed when a link to X or instagram is sent";

    SupportedEmbeds = (
        # https://github.com/Wikidepia/InstaFix
        ( "www.instagram.com", "www.ddinstagram.com" ),
        # https://github.com/FixTweet/FxTwitter
        ( "https://x.com/", "https://fxtwitter.com/" )
    );

    async def OnMessageURL( self, message: discord.Message, urls: tuple[str] ) -> Hook:

        if message.author.id == bot.user.id:
            return Hook.Continue;

        channel: discord.TextChannel = message.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
            return Hook.Continue;

        Links: list[tuple[str, str]] = [ l for l in self.SupportedEmbeds if any( a for a in urls if l[0] in a ) ];

        if len(Links) == 0:
            return Hook.Continue;

        formatted: str = message.content;

        for Link in Links:
            formatted = formatted.replace( Link[0], Link[1] );

        webhook: discord.Webhook = await bot.webhook( message.channel );

        msg: discord.WebhookMessage = await webhook.send( content=formatted, username=message.author.display_name, \
            avatar_url=message.author.avatar.url if message.author.avatar else None, wait=True );

        reply: discord.Message = await message.reply(
            embed=discord.Embed(
                color = HexColor.LIGHT_BLUE,
                description = g_Sentences.get( "fix_embeds_react_to_keep", message.guild )
            ),
            allowed_mentions=False,
            silent=True,
            mention_author=False
        );

        await reply.add_reaction( '✅' );

        async with message.channel.typing():
            await asyncio.sleep( 10 );

        try: # return None: NO. WE HAVE TO RAISE EXCEPTION :sob:
            reply = await message.channel.fetch_message( reply.id );
        except: reply = None;

        if reply is not None:

            if await bot.UserReacted( message.author, reply, emoji='✅' ):

                try: # return None: NO. WE HAVE TO RAISE EXCEPTION :sob:
                    message = await message.channel.fetch_message( message.id );
                    await message.delete();
                except: pass; # i assuem the ID is fine in this context after asyncio sleep

            else:

                try: # return None: NO. WE HAVE TO RAISE EXCEPTION :sob:
                    msg = await message.channel.fetch_message( msg.id );
                except: msg = None;

                if msg is not None:

                    await msg.delete();

            await reply.delete();

        return Hook.Continue;
