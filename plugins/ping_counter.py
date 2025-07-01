from src.main import *
from src.PluginManager import Plugin;

class ping_counter( Plugin ):

    def OnPluginActivate(self):

        command = app_commands.Command(
            name="pings",
            description="Get the pings of a user",
            callback=self.command_pings,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

        g_Sentences.push_back( "ping_counter" );

    def OnPluginDeactivate(self):

        bot.tree.remove_command( "pings" );

    @property
    def GetName(self):
        return "Ping counter";

    @property
    def GetDescription(self):
        return "Keep track of users mentioning";

    async def OnMention(self, message, mentions):

        for user in mentions:

            if user:

                cache = g_Cache.Get();

                mention = fmt.DiscordUserMention( user );

                counts = cache.get( mention, [ 0, user.name ] );

                counts[1] = user.name;

                counts[0] = counts[0] + 1;

                cache[ mention ] = counts;

        return True;

    async def OnCommand(self, message, command, args):

        if command != 'pings':
            return True;

        await message.channel.typing();

        target: discord.Member = message.author;

        if len(args) > 0:
            target = await bot.FindMemberByName( args[0], message.guild );

        if target is None:

            embed = g_BotLogger.error( g_Sentences.get( "failed_to_find_user", args[0], Guild=message.guild ), send=BotLogMode.Nothing );

            await message.reply( embed=embed, mention_author=False, silent=True, allowed_mentions=False );

            return False;

        await self.GetPingCount( target, message.channel );

        return False;

    async def GetPingCount( self, target: discord.Member, channel: discord.TextChannel ):

        cache = g_Cache.Get();

        mention = fmt.DiscordUserMention( target );

        counts = cache.get( mention, [ 0, target.name ] );

        if counts[0] > 0:

            await bot.SendMessage( channel, g_Sentences.get( "ping_counter_ping_count", counts[1], counts[0], Guild=channel.guild ), mention_author=False, silent=True, allowed_mentions=False );

        else:

            await bot.SendMessage( channel, g_Sentences.get( "ping_counter_first_ping", mention, Guild=channel.guild ), silent=True );

    @app_commands.describe( member='Member' )
    async def command_pings( self, interaction: discord.Interaction, member: discord.Member ):

        try:

            await self.GetPingCount( member, interaction.channel );

        except Exception as e:

            from src.Bot import bot;

            if interaction.response.is_done():

                await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );

            else:

                await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );
