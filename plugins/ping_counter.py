from src.main import *
from src.PluginManager import Plugin;

class ping_counter( Plugin ):

    def __init__(self):

        command = app_commands.Command(
            name="pings",
            description="Get the pings of a user",
            callback=self.command_pings,
        );

        command.guild_only = True

        bot.tree.add_command( command )

    @property
    def GetName(self):
        return "Ping counter";

    @property
    def GetDescription(self):
        return "Keep track of users mentioning";

    async def OnMention(self, message, mentions):

        for user in mentions:

            if user:

                cache = g_Cache.get();

                mention = fmt.DiscordUserMention( user );

                counts = cache.get( mention, [ 0, user.name ] );

                counts[1] = user.name;

                counts[0] = counts[0] + 1;

                cache[ mention ] = counts;

        return True;

    async def OnCommand(self, message, command, args):

        if command != 'pings':
            return True;

        target: discord.Member = message.author;

        if len(args) > 0:
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

        if isinstance( target, discord.Interaction ):

            await bot.SendResponse( channel, MessagePrinter, );

        else:

            await bot.SendMessage( channel, MessagePrinter, mention_author=False, silent=True, allowed_mentions=False );

    @app_commands.describe( member='Member' )
    async def command_pings( self, interaction: discord.Interaction, member: discord.Member ):

        try:
            await self.GetPingCount( member, interaction );
        except Exception as e:
            from src.Bot import bot;
            bot.SendResponse( interaction.channel, embeds=bot.HandleException( e, "ping_counter::command_pings", SendToDevs=True ) );
