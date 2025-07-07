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

from project import *;

@bot.event
async def on_message( message: discord.Message ):

    ExceptionItems: list[tuple] = [];

    if message.guild:
    #
        ExceptionItems.append( ( "Guild", f'``{message.guild.name}``\nID: ``{message.guild.id}``' ) );
    #

    if message.channel:
    #
        ExceptionItems.append( ( "Channel", f'``{message.channel.name}``\nID: [{message.channel.id}]({message.channel.jump_url})' ) );
    #

    if message.author:
    #
        ExceptionItems.append( ( "Author", f'{message.author.name}\nID: {fmt.DiscordUserMention( message.author )}' ) );
    #

    ExceptionItems.append( ( "Message", f'{message.content}\nID: [{message.id}]({message.jump_url})' ) );

    await g_PluginManager.CallFunction(
        "OnMessage",
        message,
        Guild=message.guild,
        items=ExceptionItems
    );

    if g_ConfigContext.bot.Prefix is not None and message.content.startswith( g_ConfigContext.bot.Prefix ):
    #
        try:
        #
            # Strip the prefix
            arguments_string: str = message.content[ len( g_ConfigContext.bot.Prefix ) : ];

            from shlex import split as SplitArgs;

            arguments: list[str] = SplitArgs( arguments_string );

            command: str = arguments.pop(0); # strip the command name

            await g_PluginManager.CallFunction(
                "OnCommand",
                message,
                command,
                arguments,
                Guild=message.guild,
                items=ExceptionItems
            );
        #
        except Exception as e: # Tell the user if shlex failed due to bad arguments
        #
            await message.reply( embed=bot.HandleException( e ) );
        #
    #

    if message.mentions and len( message.mentions ) > 0:
    #
        await g_PluginManager.CallFunction(
            "OnMention",
            message,
            message.mentions,
            Guild=message.guild,
            items=ExceptionItems
        );
    #

    if message.reference and message.reference.message_id:
    #
        try: # Try getting the replied message
        #
            replied_message: discord.Message = await message.channel.fetch_message( message.reference.message_id );

            await g_PluginManager.CallFunction(
                "OnReply",
                message,
                replied_message,
                Guild=message.guild,
                items=ExceptionItems
            );
        #
        except: pass;
    #

    if 'https://' in message.content or 'www.' in message.content:
    #
        urls: tuple[str] = tuple( url for url in message.content.split() if url.startswith( 'https://' ) or url.startswith( 'www.' ) );

        if len(urls) > 0:
        #
            await g_PluginManager.CallFunction(
                "OnLink",
                message,
                urls,
                Guild=message.guild,
                items=ExceptionItems
            );

            # Is this a link to a discord's message?
            for ReGuildID, ReChannelID, ReMessageID in re.compile( RegexPattern.DiscordMessageReference ).findall( message.content ):
            #
                await g_PluginManager.CallFunction(
                    "OnMessageReference",
                    message,
                    ReGuildID,
                    ReChannelID,
                    ReMessageID,
                    Guild=message.guild,
                    items=ExceptionItems
                );
            #

            # Is this a gif from tenor?
            if any( ( a.lower().endswith( '.gif' ) and 'cdn.discordapp.com' in a ) for a in urls ):
            #
                await g_PluginManager.CallFunction(
                    "OnMessageGIF",
                    message,
                    Guild=message.guild,
                    items=ExceptionItems
                );
            #
        #
    #

    if message.attachments:
    #
        await g_PluginManager.CallFunction(
            "OnAttachment",
            message,
            message.attachments,
            Guild=message.guild,
            items=ExceptionItems
        );
    #

    # Find unicode emojis in the message
    Emojis: list[ tuple[ str, EmojiFlags ] ] = [ ( e, EmojiFlags.Unicode ) for e in EMOJI.EMOJI_DATA if e in message.content ];

    # Find server emojis in the message
    for match in re.compile( RegexPattern.DiscordCustomEmoji ).finditer( message.content ):
    #
        EmojiString: str = match.group(0);
        EmojiID = int( match.group(1) );

        flags: EmojiFlags = EmojiFlags.ServerCustom

        if bot.CanBotUseEmoji( EmojiID ):
        #
            flags |= EmojiFlags.BotCanUse;
        #

        Emojis.append( ( EmojiString, flags ) );
    #

    if len( Emojis ) > 0:
    #
        await g_PluginManager.CallFunction(
            "OnEmoji",
            message,
            Emojis,
            Guild=message.guild,
            items=ExceptionItems
        );
    #

    if message.type == discord.MessageType.pins_add:
    #
        PinnedMessages: list[discord.Message] = await message.channel.pins();

        if PinnedMessages:
        #
            await g_PluginManager.CallFunction(
                "OnMessagePinned",
                message,
                PinnedMessages[0],
                Guild=message.guild,
                items=ExceptionItems
            );
        #
    #
    else:
    #
        BoostServerMessages: tuple[ discord.MessageType ] = (
            discord.MessageType.premium_guild_subscription,
            discord.MessageType.premium_guild_tier_1,
            discord.MessageType.premium_guild_tier_2,
            discord.MessageType.premium_guild_tier_3
        );

        if message.type in BoostServerMessages:
        #
            await g_PluginManager.CallFunction(
                "OnServerBoost",
                message,
                BoostServerMessages.index( message.type ),
                Guild=message.guild,
                items=ExceptionItems
            );
        #
    #
