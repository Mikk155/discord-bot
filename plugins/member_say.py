from src.main import *
from src.PluginManager import Plugin;

class member_say( Plugin ):

    def OnPluginActivate(self):

        command = app_commands.Command(
            name="say",
            description="Makes the bot say something",
            callback=self.command_say,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

        g_Sentences.push_back( "member_say" );

    def OnPluginDeactivate(self):

        bot.tree.remove_command( "say" );

    @property
    def GetName(self):
        return "User say";

    @property
    def GetDescription(self):
        return "Makes the bot say something";

    async def OnCommand(self, message, command, args):

        if command != 'say':
            return True;

        if len(args) > 0:

            await message.delete();

            await self.MakeUserSay( bot.user, args[0], message.channel );

        else:

            embed = g_DiscordLogger.error( g_Sentences.get( "member_say_no_quotation", Guild=message.guild ), flags=LoggerFlags.Nothing );

            await message.reply( embed=embed, mention_author=False, silent=True, allowed_mentions=False );

        return False;

    async def MakeUserSay( self, target: discord.Member, message: str, channel: discord.TextChannel ):

        avatar = target.avatar.url if target.avatar else None;
        username = target.display_name;

        webhook = await channel.create_webhook( name='say_cmd' );

        if webhook:

            said = await webhook.send( content=message, username=username, avatar_url=avatar );

            await webhook.delete()

            if said:

                ''''''
                # -TODO Log to the server's loggin system

    @app_commands.describe( message='Message', member='Member' )
    async def command_say( self, interaction: discord.Interaction, message: str, member: Optional[discord.Member] = None ):

        if not member:

            member = bot.user;

        try:

            await self.MakeUserSay( member, message, interaction.channel );

        except Exception as e:

            from src.Bot import bot;

            if interaction.response.is_done():

                await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );

            else:

                await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );
