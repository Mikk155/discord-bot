from src.main import *
from src.PluginManager import Plugin;

class ping_counter( Plugin ):

    def GetName(self):
        return "Ping counter";

    def GetDescription(self):
        return "Keep track of users mentioning";

    async def OnMention(self, message, mentions):

        for user in mentions:

            if user:

                cache = g_Cache.get();

                mention = fmt.DiscordUserMention( user );

                counts = cache.get( mention, [ 0, user.global_name ] );

                counts[1] = user.global_name;

                counts[0] = counts[0] + 1;

                cache[ mention ] = counts;

        return True;

    async def OnCommand(self, message, command, args):

        if command != 'pings':
            return True;

        target: discord.Member = message.author; # -TODO Utility to get members by name like Nekotina

        if len(args) > 0:
            print(args)
            target = await bot.FindMemberByName( args[0], message.guild );

        if target is None:

            await message.reply( "Failed to find user {}".format( args[0] ), mention_author=False, silent=True, allowed_mentions=False );

            return False;

        await self.GetPingCount( target, message );

        return False;

    async def GetPingCount( self, target: discord.Member, channel: discord.TextChannel | discord.Message ):

        cache = g_Cache.get();

        mention = fmt.DiscordUserMention( target );

        counts = cache.get( mention, [ 0, target.name ] );

        MessagePrinter = 'The user {} has not been pinged yet. This will be his first ping {}'.format( target.name, mention );

        if counts[0] > 0:

            MessagePrinter = "The user {} has been pinged {} times".format( counts[1], counts[0] );

        if isinstance( channel, discord.Message ):

            await channel.reply( MessagePrinter, mention_author=False, silent=True, allowed_mentions=False );

        else:

            await channel.send( MessagePrinter, mention_author=False, silent=True, allowed_mentions=False );
