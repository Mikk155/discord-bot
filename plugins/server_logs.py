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

from discord import Embed
from discord import Embed
from discord.components import SelectOption
from discord.guild import Guild
from project import *

import difflib

from utils.Dictionary import Dictionary;


class LogType(IntEnum):
    MessageDeleted: int = 0;
    MessageEdited: int = 1;
    __LogsTypes__: int = 2;
    '''This is used to set the size. must be the same value as the last enumerated object'''

class ChannelSelect( discord.ui.Select ):

    def __init__( self,
        ItemName: str,
        Title: str,
        Guild: discord.Guild,
        fnOnUpdate: Callable[ [str, int, int], Awaitable[True] ] = None
    ):
    #
        self.fnOnUpdate: Callable[ [str, int, int], Awaitable[True] ] = fnOnUpdate;
        self.ItemName: str = ItemName;
        self.Guild: discord.Guild = Guild;

        options: list[SelectOption] = [
            discord.SelectOption( label = channel.name, value = str( channel.id ) )
            for channel in Guild.text_channels
        ];

        super().__init__( placeholder=Title, options=options, min_values=1, max_values=1 );
    #

    async def callback( self, interaction: discord.Interaction ):
    #
        if self.fnOnUpdate is not None:
        #
            await self.fnOnUpdate( self.ItemName, int( self.values[0] ), self.Guild.id );
            await interaction.response.send_message( "✅", ephemeral=True, delete_after=1.5 );
        #
    #

class ConfigView( discord.ui.View ):

    def __init__( self,
        Items: dict[str, str],
        Guild: discord.Guild,
        fnOnUpdate: Callable[ [str, int, int], Awaitable[True] ] = None,
        fnOnTimeOut: Callable[ [discord.ui.View], Awaitable[True] ] = None,
    ):
    #
        '''
            fnOnUpdate called when a option is updated. the first argument is a integer and is the channel id
        '''
        super().__init__( timeout=300 );
        self.guild = Guild
        self.fnOnTimeOut = fnOnTimeOut;

        for k, v in Items.items():
        #
            self.add_item( ChannelSelect( k, v, Guild, fnOnUpdate ) );
        #
    #

    async def on_timeout(self):
    #
        if self.fnOnTimeOut is not None:
        #
            await self.fnOnTimeOut(self);
        #
    #

class server_logs( Plugin ):

    def OnPluginActivate(self):
    #
        command = app_commands.Command(
            name="cfg_loggin",
            description="Configure the server-loggin messages",
            callback=self.command_cfg_loggin,
        );

        command.guild_only = True;
        bot.tree.add_command( command );
        g_Sentences.push_back( "server_logs" );
    #

    def OnPluginDeactivate(self):
    #
        bot.tree.remove_command( "cfg_loggin" );
    #

    @property
    def GetName(self):
    #
        return "Server loggin";
    #

    @property
    def GetDescription(self):
    #
        return "Keep track of messages deleted, edited, audit log entries and more";
    #

    def SetDefaultLabels( self, cache: Dictionary ) -> None:
    #
        if cache.IsEmpty:
        #
            cache[ "log_channels" ] = [];
            cache[ "filter_channels" ] = [];
        #

        while len(cache[ "log_channels" ]) < LogType.__LogsTypes__:
        #
            cache[ "log_channels" ].append( None );
        #
    #

    async def OnMessageEdited( self, before: discord.Message, after: discord.Message ) -> Hook:
    #
        channel: discord.TextChannel = after.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
        #
            return Hook.Continue;
        #

        cache: Dictionary = g_Cache.Plugin;

        if not after.guild or not after.guild.id in cache:
        #
            return Hook.Continue;
        #

        GuildCache: Dictionary = cache[ after.guild.id ];

        self.SetDefaultLabels( GuildCache );

        if after.channel.id in GuildCache[ "filter_channels" ]:
        #
            return Hook.Continue;
        #

        LogTypes: list[LogType] = GuildCache[ "log_channels" ];

        if LogTypes[LogType.MessageEdited] is None:
        #
            return Hook.Continue;
        #

        channel = bot.get_channel( LogTypes[LogType.MessageEdited] );

        if not channel or channel is None or isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
        #
            return Hook.Continue;
        #

        embed = discord.Embed(
            color = RGB(100,255,0).hex,
            title = g_Sentences.get(
                "server_logs_cfg_MessageEdited",
                Guild=after.guild
            ),
            description = g_Sentences.get(
                "server_logs_cfg_MessageEdited_info",
                after.author.mention,
                after.jump_url,
                Guild=after.guild
            )
        );

        old: str = before.content;
        new: str = after.content;

        matcher: difflib.SequenceMatcher[str] = difflib.SequenceMatcher( None, old, new );
        old_result: list[str] = [];
        new_result: list[str] = [];

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        #
            if tag == 'equal':
            #
                old_result.append(old[i1:i2]);
                new_result.append(new[j1:j2]);
            #
            elif tag == 'replace':
            #
                old_result.append(f"<replace old>{old[i1:i2]}<>");
                new_result.append(f"<replace new>{new[j1:j2]}<>");
            #
            elif tag == 'delete':
            #
                old_result.append(f"<deleted>{old[i1:i2]}<>");
            #
            elif tag == 'insert':
            #
                new_result.append(f"<inserted>{new[j1:j2]}<>");
            #
        #

        old: str = ''.join( o for o in old_result );
        new: str = ''.join( o for o in new_result );

        if old != new:
        #
            def TuncateEmbeds( _newEmbed: discord.Embed, _Text: str, _Sentence: str, _SentenceParts: str ) -> discord.Embed:
            #
                _CurrentPart: int = 1;

                if len(_Text) > 1024:
                #
                    while len( _Text ) > 1024:
                    #
                        _Text_part: str = _Text[ : 1024 ];
                        _Text = _Text[ 1024 : ];

                        _newEmbed.add_field( inline = False,
                            name = g_Sentences.get( _SentenceParts, _CurrentPart, Guild=after.guild ),
                            value = _Text_part
                        );
                        _CurrentPart = _CurrentPart + 1;
                    #
                #

                if len( _Text ) > 0:
                #
                    _newEmbed.add_field( inline = False,
                        name = g_Sentences.get( _Sentence, Guild=after.guild ) if _CurrentPart > 1 else g_Sentences.get( _Sentence, _SentenceParts, Guild=after.guild ),
                        value = _Text
                    );
                #

                return _newEmbed;
            #
            embed: Embed = TuncateEmbeds(
                embed, old,
                "server_logs_cfg_MessageEdited_Before",
                "server_logs_cfg_MessageEdited_BeforePart"
            );
            embed: Embed = TuncateEmbeds(
                embed, new,
                "server_logs_cfg_MessageEdited_New",
                "server_logs_cfg_MessageEdited_NewPart"
            );
            await channel.send( embed=embed, allowed_mentions=False, mention_author=False );
        #
        return Hook.Continue;
    #

    async def OnLogTypeUpdated( self, item: str, channel: int, Guild: int ) -> None:
    #
        if Guild is None:
        #
            return;
        #

        GuildCache: Dictionary = g_Cache.Plugin[ Guild ];

        self.SetDefaultLabels(GuildCache);

        if GuildCache.IsEmpty:
        #
            GuildCache[ "log_channels" ] = [ None, None ];
            GuildCache[ "filter_channels" ] = [];
        #

        ItemIndex: list[LogType] = [ T.value for T in LogType if T.name == item ];

        GuildCache[ "log_channels" ][ItemIndex[0]] = channel;
    #

    async def OnMessageDelete( self, message: discord.Message, deleter: Union[discord.User | discord.Member] ) -> Hook:

        channel: discord.TextChannel = message.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
        #
            return Hook.Continue;
        #

        cache: Dictionary = g_Cache.Plugin;

        if not message.guild or not message.guild.id in cache:
        #
            return Hook.Continue;
        #

        GuildCache: Dictionary = cache[ message.guild.id ];

        self.SetDefaultLabels( GuildCache );

        if message.channel.id in GuildCache[ "filter_channels" ]:
        #
            return Hook.Continue;
        #

        LogTypes: list[LogType] = GuildCache[ "log_channels" ];

        if LogTypes[LogType.MessageDeleted] is None:
        #
            return Hook.Continue;
        #

        channel = bot.get_channel( LogTypes[LogType.MessageDeleted] );

        if not channel or channel is None or isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
        #
            return Hook.Continue;
        #

        AuthorMSG: str = message.author.mention;

        if message.webhook_id is not None: # Is this a webhook?
        #
            WebHookAt: list[discord.Webhook] = [ w for w in await message.channel.webhooks() if w.id == message.webhook_id ];

            if len(WebHookAt) > 0:
            #
                AuthorMSG = f'{AuthorMSG} (Webhook ``{WebHookAt[0].name}``)';
            #
        #

        embed = discord.Embed(
            color = RGB(255,0,0).hex,
            title=g_Sentences.get( "server_logs_cfg_MessageDeleted", Guild=message.guild ),
            description=g_Sentences.get( "server_logs_message_deleted_info", AuthorMSG, message.channel.jump_url, Guild=message.guild )
        );

        try:
        #
            replied: discord.Message = await message.channel.fetch_message( message.reference.message_id );

            if replied:
            #
                embed.description = embed.description + '\n' + g_Sentences.get( "server_logs_message_deleted_replied", replied.jump_url, Guild=message.guild );
            #
        #
        except:
        #
            pass;
        #

        if message.content:
        #
            content = message.content;

            if len(content) > 1024:
            #
                part: int = 1;

                while len( content ) > 1024:
                #
                    content_part = content[ : 1024 ];
                    content = content[ 1024 : ];

                    embed.add_field( inline = False,
                        name =g_Sentences.get( "server_logs_message_deleted_content", part, Guild=message.guild ),
                        value = content_part
                    );

                    part = part + 1;
                #
                if len(content) > 0:
                #
                    embed.add_field( inline = False,
                        name =g_Sentences.get( "content", Guild=message.guild ),
                        value = content
                    );
                #
            #
            else:
            #
                embed.add_field( inline = False,
                    name =g_Sentences.get( "content", Guild=message.guild ),
                    value = content
                );
            #
        #

        if deleter.id != message.author.id:
        #
            embed.add_field( inline = False,
                name = g_Sentences.get( "server_logs_message_deleted_by", Guild=message.guild ),
                value = fmt.DiscordUserMention(deleter)
            );
        #

        if message.embeds and len(message.embeds) > 0:
        #
            embeds: list[discord.Embed] = message.embeds;
            embeds.insert( 0, embed );
            await channel.send( embeds=embeds, allowed_mentions=False, mention_author=False, silent=True );
        #
        else:
        #
            await channel.send( embed=embed, allowed_mentions=False, mention_author=False, silent=True );
        #
        return Hook.Continue;
    #

    @Plugin.HandleExceptions()
    @app_commands.describe()
    @app_commands.default_permissions( administrator=True )
    async def command_cfg_loggin( self, interaction: discord.Interaction ):
    #
        plugin: server_logs = g_PluginManager.GetCurrentPlugin;

        Items: dict[str, str] = { T.name: g_Sentences.get( f'server_logs_cfg_{T.name}', Guild=interaction.guild ) for T in LogType };

        UiView = ConfigView( Items, interaction.guild, plugin.OnLogTypeUpdated );

        await interaction.response.send_message( "server_logs_cfg_select", view=UiView );
    #
