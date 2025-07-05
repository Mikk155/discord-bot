from project import *

class marry_sara( Plugin ):

    @property
    def GetDescription(self):
        return "Count how many times mikk confessed his love to the goddess sara";

    async def OnMessage(self, message):

        if message.author.id == bot.user.id:
            return True;

        if message.author.id == 744768007892500481:

            content = message.content.lower();

            if 'neko marry' in content:

                sare: discord.User = bot.get_guild( 744769532513615922 ).get_member( 746914044828450856 );

                if sare and sare in message.mentions:

                    cache = g_Cache.Get();

                    number = cache.get( "times", 52 );

                    number += 1;

                    await bot.get_channel( message.channel.id ).send( f"Mikk has confesed his love to Sare {number} times.", mention_author=False );

                    cache[ "times" ] = number;

        return True;
