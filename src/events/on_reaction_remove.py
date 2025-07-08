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
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):

    ExceptionItems: list[tuple] = [];

    if reaction.message.guild:
    #
        ExceptionItems.append( ( "Guild", f'``{reaction.message.guild.name}``\nID: ``{reaction.message.guild.id}``' ) );
    #

    if reaction.message.channel:
    #
        ExceptionItems.append( ( "Channel", f'``{reaction.message.channel.name}``\nID: [{reaction.message.channel.id}]({reaction.message.channel.jump_url})' ) );
    #

    if user:
    #
        ExceptionItems.append( ( "Author", f'{user.name}\nID: {fmt.DiscordUserMention( user )}' ) );
    #

    if isinstance( reaction.emoji, str ): # Is a unicode emoji
    #
        ExceptionItems.append( ( "Reaction", f'{reaction}\n' ) );
    #
    else:
    #
        ExceptionItems.append( ( "Reaction", f'{reaction.emoji.name}\nID: {reaction.emoji.id}' ) );
    #

    await g_PluginManager.CallFunction(
        "OnReaction",
        reaction,
        ReactionState.Removed,
        Guild=reaction.message.guild,
        items=ExceptionItems
    );
