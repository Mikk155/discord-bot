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

from discord import Embed, Interaction;
from functools import wraps

class Plugin():

    '''
        Plugin base. every plugin must inherit from this class

        Every method should return a boolean, True for keep executing plugins in the list. False if the plugin manager should stop calling subsequent plugins.
    '''

    @staticmethod
    def HandleExceptions():
    #
        def decorator( func ):
        #
            @wraps( func )
            async def wrapper( plugin: Plugin, interaction: Interaction, *args, **kwargs ):
            #
                try:
                #
                    await func( plugin, interaction, *args, **kwargs )
                #
                except Exception as e:
                #
                    ExceptionItems: list[tuple] = [];

                    if interaction.guild:
                    #
                        ExceptionItems.append( ( "Guild", f'``{interaction.guild.name}``\nID: ``{interaction.guild.id}``' ) );
                    #

                    if interaction.channel:
                    #
                        ExceptionItems.append( ( "Channel", f'``{interaction.channel.name}``\nID: [{interaction.channel.id}]({interaction.channel.jump_url})' ) );
                    #

                    if interaction.user:
                    #
                        from utils.fmt import fmt;
                        ExceptionItems.append( ( "Author", f'{interaction.user.name}\nID: {fmt.DiscordUserMention( interaction.user )}' ) );
                    #

                    ExceptionItems.append( ( f"Method {func.__name__}", f"Plugin {plugin.GetName}", False ) );

                    from src.Bot import bot;
                    embed: Embed = bot.HandleException( f'**{type(e).__name__}**: <r>{e}<>', SendToDevs=True, items=ExceptionItems, TraceUntil='Plugin.py' );
                    
                    if interaction.response.is_done():
                    #
                        await interaction.followup.send( embed=embed );
                    #
                    else:
                    #
                        await interaction.response.send_message( embed=embed );
                    #
                #
            #
            return wrapper
        #
        return decorator
    #

    guilds: list[int] = [];
    '''Guilds list to only listen events (if empty == all)'''

    def __init__( self ) -> None:
        pass;

    @property
    def GetFilename( self ) -> str:
        return self.filename;

    @property
    def GetDescription( self ) -> str:
        return None;

    @property
    def GetAuthorName( self ) -> str:
        return "Mikk155";

    @property
    def GetName( self ) -> str:
        return self.GetFilename;

    @property
    def GetAuthorSite( self ) -> str:
        return "https://github.com/Mikk155/discord-bot";
