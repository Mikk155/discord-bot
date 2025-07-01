from src.main import *
from src.PluginManager import Plugin;

import difflib;

#-TODO Maybe move this to somewhere else? May be util to other plugins
class ChannelSelect( discord.ui.Select ):

    def __init__( self,
        ItemName: str,
        Title: str,
        Guild: discord.Guild,
        fnOnUpdate: Callable[ [str, int, int], Awaitable[True] ] = None
    ):

        self.fnOnUpdate = fnOnUpdate;

        self.ItemName = ItemName;

        self.Guild = Guild;

        options = [
            discord.SelectOption( label = channel.name, value = str( channel.id ) )
            for channel in Guild.text_channels
        ];

        super().__init__( placeholder=Title, options=options, min_values=1, max_values=1 );

    async def callback( self, interaction: discord.Interaction ):

        if self.fnOnUpdate is not None:

            await self.fnOnUpdate( self.ItemName, int( self.values[0] ), self.Guild );
            await interaction.response.send_message( "✅", ephemeral=True, delete_after=1.5 );

class ConfigView( discord.ui.View ):

    def __init__( self,
        Items: dict[str, str],
        Guild: discord.Guild,
        fnOnUpdate: Callable[ [str, int, int], Awaitable[True] ] = None,
        fnOnTimeOut: Callable[ [discord.ui.View], Awaitable[True] ] = None,
    ):
        '''
            fnOnUpdate called when a option is updated. the first argument is a integer and is the channel id
        '''

        super().__init__( timeout=300 );

        self.guild = Guild
        self.fnOnTimeOut = fnOnTimeOut;

        for k, v in Items.items():

            self.add_item( ChannelSelect( k, v, Guild, fnOnUpdate ) );

    async def on_timeout(self):

        if self.fnOnTimeOut is not None:
            await self.fnOnTimeOut(self);

class server_logs( Plugin ):

    def OnPluginActivate(self):

        command = app_commands.Command(
            name="cfg_loggin",
            description="Configure the server-loggin messages",
            callback=self.command_cfg_loggin,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

        g_Sentences.push_back( "server_logs" );

    def OnPluginDeactivate(self):

        bot.tree.remove_command( "cfg_loggin" );

    @property
    def GetName(self):
        return "Server loggin";

    @property
    def GetDescription(self):
        return "Keep track of messages deleted, edited, audit log entries and more";

    LogTypes = (
        "OnMessageEdited",
        "OnMessageDelete"
    );

    async def OnMessageEdited(self, before, after):

        if after.author.id == bot.user.id or not after.guild:
            return True;

        GuildID = after.guild.id;

        cache = g_Cache.Get();

        channel = bot.get_channel( cache.get( str( GuildID ), {} ).get( self.LogTypes[0], 0 ) );

        if not channel or channel is None:
            return True;

        embed = discord.Embed(
            color = RGB(100,255,0).hex,
            title = g_Sentences.get( "server_logs_cfg_OnMessageEdited", Guild=GuildID ),
            description = g_Sentences.get( "server_logs_cfg_OnMessageEdited_info", after.author.mention, after.jump_url, Guild=GuildID )
        );

        old = before.content;
        new = after.content;

        matcher = difflib.SequenceMatcher( None, old, new );
        old_result = [];
        new_result = [];

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                old_result.append(old[i1:i2]);
                new_result.append(new[j1:j2]);
            elif tag == 'replace':
                old_result.append(f"<replace old>{old[i1:i2]}<>");
                new_result.append(f"<replace new>{new[j1:j2]}<>");
            elif tag == 'delete':
                old_result.append(f"<deleted>{old[i1:i2]}<>");
            elif tag == 'insert':
                new_result.append(f"<inserted>{new[j1:j2]}<>");

        old = ''.join( o for o in old_result );
        new = ''.join( o for o in new_result );

        if old != new:

            def TuncateEmbeds( _newEmbed: discord.Embed, _Text: str, _Sentence: str, _SentenceParts: str ) -> discord.Embed:

                _CurrentPart = 1;

                if len(_Text) > 1024:

                    while len( _Text ) > 1024:

                        _Text_part = _Text[ : 1024 ];

                        _Text = _Text[ 1024 : ];

                        _newEmbed.add_field( inline = False,
                            name = g_Sentences.get( _SentenceParts, _CurrentPart, Guild=GuildID ),
                            value = _Text_part
                        );

                        _CurrentPart = _CurrentPart + 1;

                if len( _Text ) > 0:

                    _newEmbed.add_field( inline = False,
                        name = g_Sentences.get( _Sentence, Guild=GuildID ) if _CurrentPart > 1 else g_Sentences.get( _Sentence, _SentenceParts, Guild=GuildID ),
                        value = _Text
                    );

                return _newEmbed;

            embed = TuncateEmbeds( embed, old, "server_logs_cfg_OnMessageEdited_Before", "server_logs_cfg_OnMessageEdited_BeforePart" );
            embed = TuncateEmbeds( embed, new, "server_logs_cfg_OnMessageEdited_New", "server_logs_cfg_OnMessageEdited_NewPart" );

            await channel.send( embed=embed, allowed_mentions=False, mention_author=False );

        return True;

    async def OnLogTypeUpdated( self, item: str, channel: int, Guild: int ):

        if Guild is None:
            return;

        cache = g_Cache.Get();

        GuildConfig = cache.get( str( Guild.id ), {} );

        GuildConfig[ item ] = channel;

        cache[ str( Guild.id ) ] = GuildConfig;

    async def OnMessageDelete( self, message, deleter ):

        if message.author.id == bot.user.id or not message.guild:
            return True;

        GuildID = message.guild.id;

        cache = g_Cache.Get();

        channel = bot.get_channel( cache.get( str( GuildID ), {} ).get( self.LogTypes[1], 0 ) );

        if not channel or channel is None:
            return;

        embed = discord.Embed(
            color = RGB(255,0,0).hex,
            title=g_Sentences.get( "server_logs_cfg_OnMessageDelete", Guild=GuildID ),
            description=g_Sentences.get( "server_logs_message_deleted_info", message.author.mention, message.channel.jump_url, Guild=GuildID )
        );

        try:
            replied = await message.channel.fetch_message( message.reference.message_id );
            if replied:
                embed.description = embed.description + '\n' + g_Sentences.get( "server_logs_message_deleted_replied", replied.jump_url, Guild=GuildID );
        except:
            pass;

        if message.content:

            content = message.content;

            if len(content) > 1024:

                part = 1;

                while len( content ) > 1024:

                    content_part = content[ : 1024 ];
                    content = content[ 1024 : ];

                    embed.add_field( inline = False,
                        name =g_Sentences.get( "server_logs_message_deleted_content", part, Guild=GuildID ),
                        value = content_part
                    );

                    part = part + 1;

                if len(content) > 0:

                    embed.add_field( inline = False,
                        name =g_Sentences.get( "content", Guild=GuildID ),
                        value = content
                    );

            else:

                embed.add_field( inline = False,
                    name =g_Sentences.get( "content", Guild=GuildID ),
                    value = content
                );

        if deleter.id != message.author.id:

            embed.add_field( inline = False,
                name = g_Sentences.get( "server_logs_message_deleted_by", Guild=GuildID ),
                value = fmt.DiscordUserMention(deleter)
            );

        if message.embeds and len(message.embeds) > 0:

            embeds = message.embeds;

            embeds.insert( 0, embed );

            await channel.send( embeds=embeds, allowed_mentions=False, mention_author=False, silent=True );

        else:

            await channel.send( embed=embed, allowed_mentions=False, mention_author=False, silent=True );

        return True;

    @app_commands.describe()
    @app_commands.default_permissions( administrator=True )
    async def command_cfg_loggin( self, interaction: discord.Interaction ):

        try:

            from src.PluginManager import g_PluginManager;
            plugin: server_logs = g_PluginManager.GetCurrentPlugin;

            Items = { k: g_Sentences.get( f'server_logs_cfg_{k}', Guild=interaction.guild ) for k in plugin.LogTypes };

            UiView = ConfigView( Items, interaction.guild, plugin.OnLogTypeUpdated );

            await interaction.response.send_message( "server_logs_cfg_select", view=UiView );

        except Exception as e:

            from src.Bot import bot;

            if interaction.response.is_done():

                await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );

            else:

                await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );
