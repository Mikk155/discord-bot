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

    async def OnLink( self, message, urls ):

        if message.author.id == bot.user.id:
            return True;

        Links = [ l for l in self.SupportedEmbeds if any( a for a in urls if l[0] in a ) ];

        if len(Links) == 0:
            return True;

        formatted = message.content;

        for Link in Links:
            formatted = formatted.replace( Link[0], Link[1] );

        webhook: discord.Webhook = await bot.webhook( message.channel );

        msg: discord.WebhookMessage = await webhook.send( content=formatted, username=message.author.display_name, \
            avatar_url=message.author.avatar.url if message.author.avatar else None, wait=True );

        reply = await message.reply(
            embed=discord.Embed(
                color = HexColor.LIGHT_BLUE,
                description = g_Sentences.get( "fix_embeds_react_to_keep", message.guild )
            ),
            allowed_mentions=False,
            silent=True,
            mention_author=False
        );

        await reply.add_reaction( '✅' );

        await asyncio.sleep(10);

        reply = None;
        try: # return None: NO. WE HAVE TO RAISE EXCEPTION :sob:
            reply = await message.channel.fetch_message( reply.id );
        except: pass;

        if reply is not None:

            if await bot.UserReacted( message.author, reply, emoji='✅' ):

                try: # return None: NO. WE HAVE TO RAISE EXCEPTION :sob:
                    message = await message.channel.fetch_message( message.id );
                    await message.delete();
                except: pass; # i assuem the ID is fine in this context after asyncio sleep

            else:

                msg = None;
                try: # return None: NO. WE HAVE TO RAISE EXCEPTION :sob:
                    msg = await message.channel.fetch_message( msg.id );
                except: pass;

                if msg is not None:

                    await msg.delete();

            await reply.delete();

        return True;
