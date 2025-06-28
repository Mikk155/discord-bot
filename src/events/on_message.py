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

    await g_PluginManager.CallFunction( "OnMessage", message, GuildID=message.guild.id );

    if g_ConfigContext.prefix is not None and message.content.startswith( g_ConfigContext.prefix ):

        arguments_string = message.content[ len(g_ConfigContext.prefix) : ];

        from shlex import split as SplitArgs;

        arguments = SplitArgs( arguments_string );

        command = arguments.pop(0);

        await g_PluginManager.CallFunction( "OnCommand", message, command, arguments, GuildID=message.guild.id );

    if message.mentions and len( message.mentions ) > 0:

        await g_PluginManager.CallFunction( "OnMention", message, message.mentions, GuildID=message.guild.id );

    if message.reference and message.reference.message_id:

        replied_message = await message.channel.fetch_message( message.reference.message_id );

        if replied_message:

            await g_PluginManager.CallFunction( "OnReply", message, replied_message, GuildID=message.guild.id );

    if 'https://' in message.content or 'www.' in message.content:

        urls: tuple[str] = ( url for url in message.content.split() if url.startswith( 'https://' ) or url.startswith( 'www.' ) );

        await g_PluginManager.CallFunction( "OnLink", message, urls, GuildID=message.guild.id );
