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

from discord import Embed;
from src.constants import HexColor
from src.main import g_Logger;
from typing import *

class BotLogMode:

    DeveloperChannel = ( 1 << 0 );
    ConsoleTerminal = ( 1 << 1 );

class BotLoggin():

    Messages: list[ Embed | str | tuple[ Embed | str ] ] = [];

    async def SendAllMessages( self ) -> None:

        from src.ConfigContext import g_ConfigContext;

        SentMessages = g_ConfigContext.log.MaxMessages

        while len(self.Messages) > 0 and SentMessages > 0:

            SentMessages -= 1;

            MessageSend = self.Messages.pop(0);

            MessageToSend = None;
            EmbedToSend = None;

            if isinstance( MessageSend, Embed ):
                EmbedToSend = MessageSend;
            elif isinstance( MessageSend, str ):
                MessageToSend = MessageSend;
            elif isinstance( MessageSend, tuple ):
                for i in MessageSend:
                    if isinstance( i, Embed ):
                        EmbedToSend = i;
                    elif isinstance( i, str ):
                        MessageToSend = i;

            from src.Bot import bot;

            channel = bot.get_channel( g_ConfigContext.log.Channel );

            if channel and ( MessageToSend is not None or EmbedToSend is not None ):

                await channel.send( content=MessageToSend, embed=EmbedToSend, silent=True, allowed_mentions=False, mention_author=False );

    def log( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        emoji: Optional[str] = ...,
        color: Optional[int] = 0xf000FF,
        level: Optional[str] = ...,
        items: tuple[ str, str, bool ] = ...
        ) -> Embed:

        from src.Bot import bot;
        from datetime import datetime;

        try:

            message = message.format( *args );

        except Exception as e:

            bot.HandleException( e, "BotLoggin::log", SendToDevs=True );

        if send & BotLogMode.ConsoleTerminal:

            ColorList = ( "R", "G", "Y", "B", "M", "C", "red", "green", "yellow", "blue", "magenta", "cyan" );

            for pv in ColorList:
                pv = [ pv.upper(), pv.lower() ];
                for p in pv:
                    while f'<{p}>' in message:
                        message = message.replace( f'<{p}>', '``', 1 );
                        message = message.replace( f'<>', '``', 1 );

        title = f'{emoji} [{level}]';

        if name:
            title += f' {name}';

        embed: Embed = bot.CreateEmbed( title, description=message, time=datetime.now(), items=items, color=color );

        if send & BotLogMode.DeveloperChannel:

            self.Messages.append( embed );

        return embed;

    def debug( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        items: tuple[ str, str, bool ] = ...
    ) -> Embed:
        if send & BotLogMode.ConsoleTerminal:
            g_Logger.debug( message, *args, name=name );
        return self.log( message, *args, level="Debug", emoji="📝", color=HexColor.CYAN,
            name=name, send=send, items=items );

    def warn( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        items: tuple[ str, str, bool ] = ...
    ) -> Embed:
        if send & BotLogMode.ConsoleTerminal:
            g_Logger.debug( message, *args, name=name );
        return self.log( message, *args, level="Warning", emoji="⚠️", color=HexColor.YELLOW,
            name=name, send=send, items=items );

    def error( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        items: tuple[ str, str, bool ] = ...,
        Exit: Optional[bool] = False
    ) -> Embed:
        if send & BotLogMode.ConsoleTerminal:
            g_Logger.debug( message, *args, name=name );
        if Exit is True:
            print( message.format( *args ) );
            exit(0);
        return self.log( message, *args, level="Error", emoji="‼️", color=HexColor.RED,
            name=name, send=send, items=items );

    def info( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        items: tuple[ str, str, bool ] = ...
    ) -> Embed:
        if send & BotLogMode.ConsoleTerminal:
            g_Logger.debug( message, *args, name=name );
        return self.log( message, *args, level="Info", emoji="❕", color=HexColor.GREEN,
            name=name, send=send, items=items );

    def critical( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        items: tuple[ str, str, bool ] = ...,
        Exit: Optional[bool] = False
    ) -> Embed:
        if send & BotLogMode.ConsoleTerminal:
            g_Logger.debug( message, *args, name=name );
        if Exit is True:
            print( message.format( *args ) );
            exit(0);
        return self.log( message, *args, level="Critical", emoji="⛔", color=HexColor.RED,
            name=name, send=send, items=items );

    def trace( self, message: str, *args,
        name: Optional[str] = None,
        send: Optional[BotLogMode] = ( BotLogMode.ConsoleTerminal | BotLogMode.DeveloperChannel ),
        items: tuple[ str, str, bool ] = ...
    ) -> Embed:
        if send & BotLogMode.ConsoleTerminal:
            g_Logger.debug( message, *args, name=name );
        return self.log( message, *args, level="Trace", emoji="➡", color=HexColor.BLUE,
            name=name, send=send, items=items );

global g_BotLogger;
g_BotLogger = BotLoggin();
