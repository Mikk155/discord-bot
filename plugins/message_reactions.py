from src.main import *
from src.PluginManager import Plugin;

class message_reactions( Plugin ):

    def OnPluginActivate(self):

        command = app_commands.Command(
            name="cfg_message_reactions",
            description="Configure message reactions",
            callback=self.command_cfg_message_reactions,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

    def OnPluginDeactivate(self):

        bot.tree.remove_command( "cfg_message_reactions" );

    @property
    def GetDescription(self):
        return "React with emojis to specific words";

    async def OnMessage( self, message ):

        cache = g_Cache.Get();

        if not message.guild or not str( message.guild.id ) in cache:
            return True;

        GuildCache: dict = cache[ str( message.guild.id ) ];

        matches = [ v for k, v in GuildCache.items() if k in message.content ];

        for emojis in matches:
            for emoji in emojis:
                try:
                    await message.add_reaction( emoji );
                except: break;

        return True;

    @app_commands.guild_only()
    @app_commands.default_permissions( administrator=True )
    @app_commands.describe( trigger='word trigger', emoji='emoji/emojis' )
    async def command_cfg_message_reactions( self, interaction: discord.Interaction, trigger: str, emoji: str ):

        try:

            Emojis: list[str] = [ e for e in EMOJI.EMOJI_DATA if e in emoji ];

            for match in RegexCustomEmoji().finditer( emoji ):

                EmojiString = match.group(0);

                Emojis.append( EmojiString );

            if len(Emojis) > 0:

                cache = g_Cache.Get();

                GuildCache: dict = cache.get( str( interaction.guild_id ), {} );

                GuildCache[ trigger ] = Emojis;

                cache[ str( interaction.guild_id ) ] = GuildCache;

            from json import dumps;

            embed = discord.Embed(
                color = RGB(255,255,0).hex,
                title=trigger,
                description=''.join( e for e in Emojis )
            );

            await interaction.response.send_message( embed=embed );

        except Exception as e:

            from src.Bot import bot;

            if interaction.response.is_done():

                await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );

            else:

                await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );
