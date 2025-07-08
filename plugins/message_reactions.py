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

from re import Pattern
from project import *
from utils.Dictionary import Dictionary

class message_reactions( Plugin ):

    def OnPluginActivate(self):
    #
        command = app_commands.Command(
            name="cfg_message_reactions",
            description="Configure message reactions",
            callback=self.command_cfg_message_reactions,
        );

        command.guild_only = True;

        bot.tree.add_command( command );
    #

    def OnPluginDeactivate(self):
    #
        bot.tree.remove_command( "cfg_message_reactions" );
    #

    @property
    def GetDescription(self):
    #
        return "React with emojis to specific words";
    #

    async def OnMessage( self, message: discord.Message ) -> Hook:
    #
        if message.author.id == bot.user.id:
            return Hook.Continue;

        channel: discord.TextChannel = message.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
            return Hook.Continue;

        cache: Dictionary = g_Cache.Plugin;

        if not message.guild or not message.guild.id in cache:
            return Hook.Continue;

        GuildCache: Dictionary = cache[ str( message.guild.id ) ];

        matches: list[str] = [ v for k, v in GuildCache.items() if k in message.content ];

        InvalidEmojis: list[str] = [];

        for emojis in matches:
        #
            for emoji in emojis:
            #
                try:
                #
                    await message.add_reaction( emoji );
                #
                except discord.NotFound:
                #
                    InvalidEmojis.append( emoji );
                #
                except TypeError:
                #
                    InvalidEmojis.append( emoji );
                #
                except:
                #
                    break;
                #
            #
        #

        CacheCopy: dict[str, list[str]] = GuildCache.ToDict;

        # Remove invalid emojis
        for word, emojis in CacheCopy.items():
        #
            for InvalidEmoji in InvalidEmojis:
            #
                if InvalidEmoji in emojis:
                #
                    emojis.pop( InvalidEmoji )
                #
            #
            GuildCache[ word ] = emojis;
        #
        return Hook.Continue;
    #

    @Plugin.HandleExceptions()
    @app_commands.guild_only()
    @app_commands.default_permissions( administrator=True )
    @app_commands.describe( trigger='word trigger', emoji='emoji/emojis' )
    async def command_cfg_message_reactions( self, interaction: discord.Interaction, trigger: Optional[str] = None, emoji: Optional[str] = None ):
    #
        cache: Dictionary = g_Cache.Plugin[ interaction.guild_id ];

        if trigger is None:
        #
            if cache.IsEmpty:
            #
                await interaction.response.send_message( content=g_Sentences.get( "not_configured", Guild=interaction.guild_id ) );
            #
            else:
            #
                await interaction.followup.send( "cache", file=discord.File( cache.Serialize, "reactions.json" ) );
            #
        #
        elif emoji is None:
        #
            cache.pop( trigger );

            await interaction.response.send_message(
                content=g_Sentences.get(
                    "message_reactions_removed",
                    trigger,
                    Guild=interaction.guild_id
                )
            );
        #
        else:
        #
            Emojis: list[str] = [ e for e in EMOJI.EMOJI_DATA if e in emoji ];

            CustomEmojiRegex: Pattern[str] = re.compile( RegexPattern.DiscordCustomEmoji );

            for match in CustomEmojiRegex.finditer( emoji ):
            #
                EmojiString: str = match.group(0);
                Emojis.append( EmojiString );
            #
            if len(Emojis) > 0:
            #
                cache[ trigger ] = Emojis;
            #

            embed = discord.Embed(
                color = RGB(255,255,0).hex,
                title=trigger,
                description=''.join( e for e in Emojis )
            );

            await interaction.response.send_message( embed=embed );
        #
    #
