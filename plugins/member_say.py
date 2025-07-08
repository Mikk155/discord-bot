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

    def OnPluginDeactivate(self) -> None:

        bot.tree.remove_command( "say" );

    @property
    def GetName(self):
        return "User say";

    @property
    def GetDescription(self):
        return "Makes the bot say something";

    async def OnCommand( self, message: discord.Message, command: str, args: list[str] ) -> Hook:

        if message.author.id == bot.user.id or command != 'say':
            return Hook.Continue;

        channel: discord.TextChannel = message.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
            return Hook.Continue;

        if len(args) > 0:

            await message.delete(); #-TODO Log it if needed

            await self.MakeUserSay( bot.user, args[0], message.channel );

        else:

            embed: discord.Embed = g_DiscordLogger.error(
                g_Sentences.get(
                    "member_say_no_quotation",
                    Guild=message.guild
                ),
                flags=LoggerFlags.Nothing
            );

            await message.reply( embed=embed, mention_author=False, silent=True, allowed_mentions=False );

        return Hook.Break;

    async def MakeUserSay( self, target: discord.Member, message: str, channel: discord.TextChannel ) -> None:

        avatar: str | None = target.avatar.url if target.avatar else None;
        username: str = target.display_name;

        webhook = bot.webhook( channel );

        said: discord.WebhookMessage = await webhook.send( content=message, username=username, avatar_url=avatar );

        # -TODO Log to the server's loggin system

    @Plugin.HandleExceptions()
    @app_commands.describe( message='Message', member='Member' )
    async def command_say( self, interaction: discord.Interaction, message: str, member: Optional[discord.Member] = None ):
        await self.MakeUserSay( member if member is not None else bot.user, message, interaction.channel );
