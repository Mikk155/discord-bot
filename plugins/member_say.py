from src.main import *
from src.main import *
from src.PluginManager import Plugin;

class member_say( Plugin ):

    def __init__(self):

        command = app_commands.Command(
            name="say",
            description="Makes the bot say something",
            callback=self.command_say,
        );

        command.guild_only = True

        bot.tree.add_command( command )

    def GetName(self):
        return "User say";

    def GetDescription(self):
        return "Makes the bot say something";

    async def OnCommand(self, message, command, args):

        if command != 'say':
            return True;

        if len(args) > 0:

            await message.delete();

            await self.MakeUserSay( bot.user, args[0], message.channel );

        else:

            await message.reply( "You need to provide an argument surrounded by quotes", mention_author=False, silent=True, allowed_mentions=False );

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

        await self.MakeUserSay( member, message, interaction.channel );
