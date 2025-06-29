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

from typing import *;
import discord
from discord import app_commands

class Bot( discord.Client ):

    __on_start_called__: bool = False

    def __init__( self ):

        super().__init__( intents = discord.Intents.all() );

        self.tree = app_commands.CommandTree( self );

    async def setup_hook( self ):

        from src.ConfigContext import g_ConfigContext;

        if g_ConfigContext.bot.IsDeveloper is True and g_ConfigContext.bot.TargetGuildCommands is not None:

            TargetGuild = discord.Object( id = g_ConfigContext.bot.TargetGuildCommands );

            if TargetGuild:

                self.tree.clear_commands( guild=TargetGuild );

                self.tree.copy_global_to( guild=TargetGuild );

                await self.tree.sync( guild=TargetGuild );

                return;

        self.tree.clear_commands();

        await self.tree.sync();

    def GetCallTraceEmbeds( self, embed: discord.Embed, PythonLibraries = False ) -> discord.Embed:

        from utils.Path import Path;
        from sys import exc_info;
        from traceback import extract_tb;
        exc_type, exc_value, exc_traceback = exc_info();
        traceback_list = extract_tb( exc_traceback );

        EmbedFields = [];
        
        for frame in traceback_list:

            if PythonLibraries is False and frame.filename.find( "Python" ) != -1:
                continue;

            EmbedFields.append(
                (
                    f'**{exc_type.__name__}** line: ``{frame.lineno}``',
                    "```py\n{}``` `{}`".format(
                        frame.line,
                        frame.filename[ frame.filename.rfind( "Python" )
                            if ( frame.filename.find( "Python" ) != -1 )
                            else len(Path.Workspace()) : ]
                    ),
                    False
                )
            );

        return self.AddEmbedFields( embed, EmbedFields );

    from inspect import FrameInfo;
    def GetCallChain( self, overloads: int = 1 ) -> list[ FrameInfo ]:
        from inspect import stack;
        return stack()[overloads:];

    def GetCallChainEmbeds( self, embed: discord.Embed, PythonLibraries = False, overloads: int = 2 ) -> discord.Embed:

        callbacks = self.GetCallChain(overloads);

        from utils.Path import Path;

        EmbedFields = [];
        
        for call in callbacks:

            if PythonLibraries is False and call.filename.find( "Python" ) != -1:
                continue;

            EmbedFields.append(
                (
                    call.function, '``{}``\n```py\n{}\n```\nL: {}'.format(
                        call.filename[ call.filename.rfind( "Python" ) \
                            if ( call.filename.find( "Python" ) != -1 ) \
                                else len(Path.Workspace()) : ],
                        ''.join( i.strip( ' ' ) for i in call.code_context ) \
                            if call.code_context is not None else '<--Unknown-->',
                        call.lineno
                    ),
                    False
                )
            );

        return self.AddEmbedFields( embed, EmbedFields );

    async def FindMemberByName( self, name: str, guild: discord.Guild | int ) -> None | discord.Member:

        if isinstance( guild, int ):

            guild = discord.Object( id = guild );

        for member in guild.members:

            ListNames = [ MemberName.lower() for MemberName in ( member.name, member.display_name, member.name ) if MemberName is not None ];

            if name.lower() in ListNames:
                return member;

            # Maybe it was a partial name?
            for n in ListNames:
                if n.startswith( name ):
                    return member;

        return None;

    #================================================
    # Utilities bellow
    #================================================

    async def SendMessage( self, target: discord.TextChannel | discord.Message | discord.Interaction,
        content: Optional[str] = None, *,
        tts: bool = False,
        embed: Optional[discord.Embed] = None,
        embeds: Optional[list[discord.Embed]] = None,
        file: Optional[discord.File] = None,
        stickers: Optional[list[discord.StickerItem]] = None,
        delete_after: float = None,
        nonce: Union[str, int] = None,
        allowed_mentions: Optional[discord.AllowedMentions] = None,
        suppress_embeds: bool = False,
        silent: bool = False,
        mention_author: bool = None,
        poll: discord.Poll = None,
        view: Optional[discord.ui.View] = None,
        ) -> discord.Message:
        '''
            Send a message depending on the target type.

            `target`: The message destination. If it is a `discord.Message`, the message will be a reply.
                - If it is a `discord.TextChannel`, it will send a regular message.
                - If it is a `discord.Interaction`, it will respond or follow up depending on interaction state.

            `content`: The message content (text). Can be None if sending only embed or file.

            `tts`: Whether the message should be sent as a text-to-speech message.

            `embed`: A single embed object to include in the message.

            `embeds`: A list of embeds to include in the message (cannot be used with `embed`).

            `file`: A single file to attach to the message.

            `stickers`: A list of sticker items to include in the message.

            `delete_after`: Automatically delete the message after a certain number of seconds.

            `nonce`: Used for optimistic message sending (client-side identifier).

            `silent`: Whether the message should not trigger notifications for mentioned users.

            `mention_author`: Whether to mention the author of the message being replied to.

            `allowed_mentions`: Controls which mentions are allowed (roles, users, everyone).

            `suppress_embeds`: If True, any embeds in links will be suppressed.

            `view`: A `discord.ui.View` with interactive components to attach to the message.

            `poll`: A `discord.Poll` object to attach (if supported by your version).
        '''

        if isinstance( target, discord.Message ):
            return await target.reply( content, tts=tts, embed=embed, embeds=embeds, file=file, stickers=stickers,
                delete_after=delete_after, nonce=nonce, silent=silent, mention_author=mention_author,
                allowed_mentions=allowed_mentions, suppress_embeds=suppress_embeds, view=view, poll=poll
            );

        elif isinstance( target, discord.Interaction ):

            return await self.SendResponse( target, content, tts=tts, embed=embed, embeds=embeds, file=file,
                silent=silent, allowed_mentions=allowed_mentions, suppress_embeds=suppress_embeds, view=view, poll=poll
            );

        else:
            return await target.send( content, tts=tts, embed=embed, embeds=embeds, file=file, stickers=stickers,
                delete_after=delete_after, nonce=nonce, silent=silent, mention_author=mention_author,
                allowed_mentions=allowed_mentions, suppress_embeds=suppress_embeds, view=view, poll=poll
            );

    async def SendResponse( self, interaction: discord.Interaction,
        content: Optional[str] = None, *,
        username: str = None,
        avatar_url: Any = None,
        tts: bool = None,
        ephemeral: bool = None,
        file: discord.File = None,
        files: Sequence[discord.File] = None,
        embed: discord.Embed = None,
        embeds: Sequence[discord.Embed] = None,
        allowed_mentions: discord.AllowedMentions = None,
        view: discord.ui.View = None,
        thread = None,
        thread_name: str = None,
        wait: Literal[True] = None,
        suppress_embeds: bool = None,
        silent: bool = None,
        applied_tags: List[discord.ForumTag] = None,
        poll: discord.Poll = None
        ) -> discord.WebhookMessage:
        '''
            Sends a response to an interaction, choosing between
            `interaction.response.send_message()` and `interaction.followup.send()`.

            `target`: The interaction to respond to.

            `content`: The message content (text). Can be None if sending only embed or file.

            `username`: Override the default bot username for this message (webhook only).

            `avatar_url`: Override the default bot avatar for this message (webhook only).

            `tts`: Whether the message should be sent as a text-to-speech message.

            `ephemeral`: Whether the message should only be visible to the invoking user.

            `file`: A single file to attach to the message.

            `files`: A list of files to attach (cannot be used with `file`).

            `embed`: A single embed object to include in the message.

            `embeds`: A list of embeds to include in the message (cannot be used with `embed`).

            `allowed_mentions`: Controls which mentions are allowed (roles, users, everyone).

            `view`: A `discord.ui.View` with interactive components to attach to the message.

            `thread`: The thread to send the message to.

            `thread_name`: Name of the thread to create (if applicable).

            `wait`: Whether to wait for the webhook message to be created and return it.

            `suppress_embeds`: If True, disables link embeds.

            `silent`: Whether to send the message without triggering mention notifications.

            `applied_tags`: A list of `discord.ForumTag` to apply (for use in forum threads).

            `poll`: A `discord.Poll` object to attach to the message (if supported).
        '''

        if interaction.response.is_done():
            return await interaction.followup.send( content, username=username, avatar_url=avatar_url,
                tts=tts, ephemeral=ephemeral, file=file, files=files, embed=embed, embeds=embeds,
                allowed_mentions=allowed_mentions, view=view, thread=thread, thread_name=thread_name,
                wait=wait, suppress_embeds=suppress_embeds, silent=silent, applied_tags=applied_tags, poll=poll,
            );

        else:
            return await interaction.response.send_message( content, username=username, avatar_url=avatar_url,
                tts=tts, ephemeral=ephemeral, file=file, files=files, embed=embed, embeds=embeds,
                allowed_mentions=allowed_mentions, view=view, thread=thread, thread_name=thread_name,
                wait=wait, suppress_embeds=suppress_embeds, silent=silent, applied_tags=applied_tags, poll=poll,
            );

    def AddEmbedFields( self, embed: discord.Embed, items: tuple[ str, str, bool ] ) -> discord.Embed:

        fields = 0;

        for item in items:

            fields += 1;

            if fields > 25:

                from src.BotLoggin import g_BotLogger;

                g_BotLogger.warn( "Can not add all fields to the message \"<c>{}<>\" it's above discord's max capacity of 24 fields!", embed.title );

                break;

            field_title = item[0];
            if len( field_title ) > 256:
                    field_title = field_title[ : 256 ];

            field_description = item[1];
            if len( field_description ) > 1024:
                    field_description = field_description[ : 1024 ];

            field_inline = item[2] if len(item) > 2 else True;

            embed.add_field( name=field_title, value=field_description, inline =field_inline );

        return embed;

    from datetime import datetime;
    def CreateEmbed( self, title: str, *,
        description: str = None,
        color: int =0xf000FF,
        time: datetime = None,
        items: tuple[ str, str, bool ] = None
    ) -> discord.Embed:

        embed = discord.Embed( color = color, title=title, description=description, timestamp=time );

        if items is not None and isinstance( items, ( tuple | list ) ):
            embed = self.AddEmbedFields( embed, items );

        return embed;

    def HandleException( self,
        exception: Exception,
        message: str = None,
        *args,
        SendToDevs = False,
        data: dict = None,
    ) -> discord.Embed:
        '''
            Build a exception message

            message: Message to display as description, formated with *args.

            SendToDevs: If true, this message will be delivered to the developer server formated with data

            data: dictionary of anything that could be useful to print on the developer server.
        '''

        from src.BotLoggin import g_BotLogger;
        from src.constants import BotLogMode;
        embed = g_BotLogger.error( '' if message is None else message, *args, send=BotLogMode.Nothing, name="Exception" );
        embed = self.AddEmbedFields( embed, [ ( "Exception", str(exception), False ) ] );

        if SendToDevs is True:

            g_BotLogger.Messages.append( embed );

            g_BotLogger.Messages.append(
                self.GetCallTraceEmbeds(
                    self.CreateEmbed(
                        "Callback traces",
                        description="The previous Exception were the cause of these callbacks",
                        color=embed.color
                    ),
                    True
                )
            );

            if data is not None and len(data) > 0:

                from utils.fmt import fmt;

                for k, v in data.copy().items():

                    if isinstance( v, str ):
                        continue;

                    if isinstance( v, ( float | int | bool ) ):
                        data[ k ] = str(v);
                    elif isinstance( v, ( discord.User | discord.Member ) ):
                        data[ k ] = f'User: {fmt.DiscordUserMention(v)}';
                        data[ k ] = f'Guild: {v.guild} {v.guild.id if v.guild else ""}';
                    elif isinstance( v, discord.Message ):
                        data[ k ] = f'Message: {v.jump_url} {v.content}';
                        data[ k ] = f'Guild: {v.channel.guild if v.channel else ""} {v.channel.guild.id if v.channel.guild else ""}';
                        data[ k ] = f'User: {fmt.DiscordUserMention(v.author)}';
                    elif isinstance( v, discord.TextChannel ):
                        data[ k ] = f'Guild: {v.guild} {v.guild.id if v.guild else ""}';
                    elif isinstance( v, discord.Interaction ):
                        data[ k ] = f'Guild: {v.guild} {v.guild_id}';
                        data[ k ] = f'User: {fmt.DiscordUserMention(v.user)}';

                from json import dumps;
                g_BotLogger.Messages.append( "Additional data providedby the Exception\n```json\n{}\n```".format( dumps(data, indent=1) ) );

        return embed;

global bot;
bot: Bot = Bot();
