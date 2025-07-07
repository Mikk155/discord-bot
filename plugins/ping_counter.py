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

class ping_counter( Plugin ):

    def OnPluginActivate(self):
    #
        command = app_commands.Command(
            name="pings",
            description="Get the pings of a user",
            callback=self.command_pings,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

        g_Sentences.push_back( "ping_counter" );
    #

    def OnPluginDeactivate(self):
    #
        bot.tree.remove_command( "pings" );
    #

    @property
    def GetName(self):
    #
        return "Ping counter";
    #

    @property
    def GetDescription(self):
    #
        return "Keep track of users mentioning";
    #

    async def OnMention(self, message, mentions):
    #
        dat = {};
        s = dat[ "sexo" ];

        for user in mentions:
        #
            if user:
            #
                UserCache: Dictionary = g_Cache.Plugin[ user.id ];

                if UserCache.IsEmpty:
                #
                    UserCache[ "pings" ] = 0;
                #
                UserCache[ "name" ] = user.name;
                UserCache[ "pings" ] += 1;
            #
        #
        return True;
    #

    async def OnCommand(self, message, command, args):
    #
        if command != 'pings':
        #
            return True;
        #

        await message.channel.typing();

        target: discord.Member = message.author;

        if len(args) > 0:
        #
            target = await bot.FindMemberByName( args[0], message.guild );
        #

        if target is None:
        #
            embed: discord.Embed = g_DiscordLogger.error(
                g_Sentences.get(
                    "failed_to_find_user",
                    args[0],
                    Guild=message.guild
                ),
                flags=LoggerFlags.Nothing
            );

            await message.reply(
                embed=embed,
                mention_author=False,
                silent=True,
                allowed_mentions=False
            );

            return False;
        #

        await self.GetPingCount( target, message.channel );

        return False;
    #

    async def GetPingCount( self, target: discord.Member, channel: discord.TextChannel ):
    #
        UserCache: Dictionary = g_Cache.Plugin[ target.id ];

        mention: str = fmt.DiscordUserMention( target );

        if UserCache.IsEmpty:
        #
            await bot.SendMessage(
                channel,
                g_Sentences.get(
                    "ping_counter_first_ping",
                    mention,
                    Guild=channel.guild
                ),
                silent=True
            );
        #
        else:
        #
            await bot.SendMessage(
                channel,
                g_Sentences.get(
                    "ping_counter_ping_count",
                    UserCache[ "name" ],
                    UserCache[ "pings" ],
                    Guild=channel.guild
                ),
                mention_author=False,
                silent=True,
                allowed_mentions=False
            );
        #
    #

    @app_commands.describe( member='Member' )
    async def command_pings( self, interaction: discord.Interaction, member: discord.Member ):
    #
        try:
        #
            await self.GetPingCount( member, interaction.channel );
        #
        except Exception as e:
        #
            from src.Bot import bot;

            if interaction.response.is_done():
            #
                await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );
            #
            else:
            #
                await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );
            #
        #
    #
