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

from src.main import *;

@bot.event
async def on_message( message: discord.Message ):

    try:

        await g_PluginManager.CallFunction( "OnMessage", message, Guild=message.guild );

        if g_ConfigContext.bot.Prefix is not None and message.content.startswith( g_ConfigContext.bot.Prefix ):

            try:

                arguments_string = message.content[ len(g_ConfigContext.bot.Prefix) : ];

                from shlex import split as SplitArgs;

                arguments = SplitArgs( arguments_string );

                command = arguments.pop(0);

                await g_PluginManager.CallFunction( "OnCommand", message, command, arguments, Guild=message.guild );
        
            except Exception as e:

                await message.reply( embed=bot.HandleException( e ) );

        if message.mentions and len( message.mentions ) > 0:

            await g_PluginManager.CallFunction( "OnMention", message, message.mentions, Guild=message.guild );

        if message.reference and message.reference.message_id:

            try:
                replied_message = await message.channel.fetch_message( message.reference.message_id );
                await g_PluginManager.CallFunction( "OnReply", message, replied_message, Guild=message.guild );
            except:
                pass;

        if 'https://' in message.content or 'www.' in message.content:

            urls: tuple[str] = tuple( url for url in message.content.split() if url.startswith( 'https://' ) or url.startswith( 'www.' ) );

            if len(urls) > 0:

                await g_PluginManager.CallFunction( "OnLink", message, urls, Guild=message.guild );

                from src.constants import RegexMessageReference;

                for ReGuildID, ReChannelID, ReMessageID in RegexMessageReference().findall( message.content ):

                    await g_PluginManager.CallFunction( "OnMessageReference", message, ReGuildID,ReChannelID, ReMessageID,Guild=message.guild );

                if any( ( a.lower().endswith( '.gif' ) and 'cdn.discordapp.com' in a ) for a in urls ):

                    await g_PluginManager.CallFunction( "OnMessageGIF", message, Guild=message.guild );

        if message.attachments:

            await g_PluginManager.CallFunction( "OnAttachment", message, message.attachments, Guild=message.guild );

        Emojis: list[ tuple[ str, EmojiFlags ] ] = [];

        Emojis += [ ( e, EmojiFlags.Unicode ) for e in EMOJI.EMOJI_DATA if e in message.content ];

        for match in RegexCustomEmoji().finditer( message.content ):

            EmojiString = match.group(0);
            EmojiID = int( match.group(1) );

            flags = EmojiFlags.ServerCustom

            CustomEmoji = discord.utils.get( message.guild.emojis, id=EmojiID );

            if CustomEmoji and CustomEmoji.is_usable():

                flags |= EmojiFlags.BotCanUse

            Emojis.append( ( EmojiString, flags ) );

        if len( Emojis ) > 0:

            await g_PluginManager.CallFunction( "OnEmoji", message, Emojis, Guild=message.guild );

        BoostServerMessages = (
            discord.MessageType.premium_guild_subscription,
            discord.MessageType.premium_guild_tier_1,
            discord.MessageType.premium_guild_tier_2,
            discord.MessageType.premium_guild_tier_3
        );

        if message.type == discord.MessageType.pins_add:

            PinnedMessages = await message.channel.pins()

            if PinnedMessages:

                await g_PluginManager.CallFunction("OnMessagePinned", message, PinnedMessages[0], Guild=message.guild );

        # elif message.type == discord.MessageType.forwarded:

        #     await g_PluginManager.CallFunction("OnMessageForwarded", message, Guild=message.guild );

        elif message.type in BoostServerMessages:

            await g_PluginManager.CallFunction("OnServerBoost", message, BoostServerMessages.index( message.type ), Guild=message.guild );

    except Exception as e:

        bot.HandleException( e, SendToDevs=True, data={ "message": message } );
