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

from discord import Member, User
from project import *;

@bot.event
async def on_message_delete( message: discord.Message ):

    # -TODO Get audith log and pass on the deleter
    deleter: User | Member = message.author;

    ExceptionItems: list[tuple] = [];

    if message.guild:
    #
        ExceptionItems.append( ( "Guild", f'``{message.guild.name}``\nID: ``{message.guild.id}``' ) );
    #

    if message.channel and not isinstance( message.channel, discord.DMChannel | discord.GroupChannel ):
    #
        ExceptionItems.append( ( "Channel", f'``{message.channel.name}``\nID: [{message.channel.id}]({message.channel.jump_url})' ) );
    #

    if message.author:
    #
        ExceptionItems.append( ( "Author", f'{message.author.name}\nID: {fmt.DiscordUserMention( message.author )}' ) );
    #

    ExceptionItems.append( ( "Message", f'{message.content}\nID: [{message.id}]({message.jump_url})' ) );

    await g_PluginManager.CallFunction(
        "OnMessageDelete",
        message,
        deleter,
        Guild=message.guild,
        items=ExceptionItems
    );
