from typing import *;
import discord
from discord import app_commands

class Bot( discord.Client ):

    from src.BotLoggin import BotLoggin;
    m_Loggin = BotLoggin();

    __on_start_called__: bool = False

    def __init__( self ):

        super().__init__( intents = discord.Intents.all() );

        self.tree = app_commands.CommandTree( self );

    async def setup_hook( self ):

        from src.ConfigContext import g_ConfigContext;

        if g_ConfigContext.developer:

            TargetGuild = discord.Object( id = g_ConfigContext.developer_guild );

            if TargetGuild:

                self.tree.clear_commands( guild=TargetGuild );

                self.tree.copy_global_to( guild=TargetGuild );

                await self.tree.sync( guild=TargetGuild );

                return;

        await self.tree.sync();

    async def FindMemberByName( self, name: str, guild: discord.Guild | int ) -> None | discord.Member:

        if isinstance( guild, int ):

            guild = discord.Object( id = guild );

        for member in guild.members:

            if name in ( member.name, member.display_name, member.global_name ):
                return member;

            # Partial? This maybe is a bad idea
            if name in member.name or name in member.display_name or name in member.global_name:
                return member;

        return None;

    async def SendMessage( self, target: discord.TextChannel | discord.Message | discord.Interaction,
        content: Optional[str] = ..., *,
        tts: bool = False,
        embed: Optional[discord.Embed] = None,
        embeds: Optional[list[discord.Embed]] = None,
        file: Optional[discord.File] = None,
        stickers: Optional[list[discord.StickerItem]] = None,
        delete_after: float = ...,
        nonce: Union[str, int] = ...,
        allowed_mentions: Optional[discord.AllowedMentions] = None,
        suppress_embeds: bool = False,
        silent: bool = False,
        reference: Union[discord.Message, discord.MessageReference, discord.PartialMessage] = ...,
        mention_author: bool = ...,
        poll: discord.Poll = ...,
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

            `reference`: The message to reply to; only used when `target` is not already a Message.

            `silent`: Whether the message should not trigger notifications for mentioned users.

            `mention_author`: Whether to mention the author of the message being replied to.

            `allowed_mentions`: Controls which mentions are allowed (roles, users, everyone).

            `suppress_embeds`: If True, any embeds in links will be suppressed.

            `view`: A `discord.ui.View` with interactive components to attach to the message.

            `poll`: A `discord.Poll` object to attach (if supported by your version).
        '''

        if isinstance( target, discord.Message ):
            return await target.reply( content, tts=tts, embed=embed, embeds=embeds, file=file, stickers=stickers,
                delete_after=delete_after, nonce=nonce, reference=reference, silent=silent, mention_author=mention_author,
                allowed_mentions=allowed_mentions, suppress_embeds=suppress_embeds, view=view, poll=poll
            );

        else:
            return await target.send( content, tts=tts, embed=embed, embeds=embeds, file=file, stickers=stickers,
                delete_after=delete_after, nonce=nonce, reference=reference, silent=silent, mention_author=mention_author,
                allowed_mentions=allowed_mentions, suppress_embeds=suppress_embeds, view=view, poll=poll
            );

    async def SendResponse( self, target: discord.TextChannel | discord.Message | discord.Interaction,
        content: Optional[str] = ..., *,
        username: str = ...,
        avatar_url: Any = ...,
        tts: bool = ...,
        ephemeral: bool = ...,
        file: discord.File = ...,
        files: Sequence[discord.File] = ...,
        embed: discord.Embed = ...,
        embeds: Sequence[discord.Embed] = ...,
        allowed_mentions: discord.AllowedMentions = ...,
        view: discord.ui.View = ...,
        thread = ...,
        thread_name: str = ...,
        wait: Literal[True] = ...,
        suppress_embeds: bool = ...,
        silent: bool = ...,
        applied_tags: List[discord.ForumTag] = ...,
        poll: discord.Poll = ...,
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

        if target.response.is_done():
            return await target.followup.send( content, username=username, avatar_url=avatar_url,
                tts=tts, ephemeral=ephemeral, file=file, files=files, embed=embed, embeds=embeds,
                allowed_mentions=allowed_mentions, view=view, thread=thread, thread_name=thread_name,
                wait=wait, suppress_embeds=suppress_embeds, silent=silent, applied_tags=applied_tags, poll=poll,
            );

        else:
            return await target.response.send_message( content, username=username, avatar_url=avatar_url,
                tts=tts, ephemeral=ephemeral, file=file, files=files, embed=embed, embeds=embeds,
                allowed_mentions=allowed_mentions, view=view, thread=thread, thread_name=thread_name,
                wait=wait, suppress_embeds=suppress_embeds, silent=silent, applied_tags=applied_tags, poll=poll,
            );

global bot;
bot: Bot = Bot();
