from typing import *;
from discord import Embed;
from utils.RGB import RGB;
from datetime import datetime;

class LoggerLevel:

    AllLoggers = -1;
    Critical: int = ( 1 << 0 ); # critical is ignored and will always being enable
    Error: int = ( 1 << 1 ); # The same goes for error
    Warning: int = ( 1 << 2 );
    Information: int = ( 1 << 3 );
    Debug: int = ( 1 << 4 );
    Trace: int = ( 1 << 5 );

def ToLoggerLevel( level: str ) -> int:
    _Levels = {
        'critical': LoggerLevel.Critical,
        'error': LoggerLevel.Error,
        'warning': LoggerLevel.Warning,
        'information': LoggerLevel.Information,
        'debug': LoggerLevel.Debug,
        'trace': LoggerLevel.Trace,
        'allloggers': LoggerLevel.AllLoggers
    };
    return _Levels.get( level, 0 );

class LoggerFlags:
    Nothing: int = 0;
    PrintTerminal: int = ( 1 << 0 );
    PrintDiscord: int = ( 1 << 1 );

class DiscordLogger():

    name: str = "Bot";

    __Messages: list[ Union[ Embed, str ] ];

    def __init__( self ):

        self.__Messages = [];

    def push_back( self, message: Union[ Embed, str ] ):
        self.__Messages.append( message );

    async def SendAllMessages( self ) -> None:

        from src.ConfigContext import g_ConfigContext;

        SentMessages = g_ConfigContext.log.MaxMessages

        while len(self.__Messages) > 0 and SentMessages > 0:

            SentMessages -= 1;

            MessageSend = self.__Messages.pop(0);

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

    def LogCore( self,
        message: str,
        color: RGB,
        emoji: str,
        level_name: str,
        level: LoggerLevel,
        name: Optional[str],
        items: Optional[ tuple[ str, str, bool ] ],
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord ),
        *args
        ) -> Embed:

        if len(args) > 0:

            try:

                message = message.format( *args );

            except Exception as e:

                print( RGB(255,0,0).cmd("ERROR") + ": Failed to format message on DiscordLogger for " + RGB(255,255,0).cmd(message) );

        name = name if name is not None else self.name;

        now = datetime.now();

        from src.ConfigContext import g_ConfigContext;

        if flags & LoggerFlags.PrintTerminal:

            print( '[{}:{}:{}] [{}] [{}] {}'.format(
                RGB(255,255,0).cmd( now.hour ),
                RGB(255,255,0).cmd( now.minute ),
                RGB(255,255,0).cmd( now.second ),
                color.cmd( level_name ),
                RGB(0,200,255).cmd( name ),
                message
            ) );

        embed = Embed( color = color.hex, title = f'{emoji}{level_name} {name}', description=message, timestamp=now );

        if items is not None and len(items) > 0:

            fields = 0;

            for item in items:

                fields += 1;

                if fields > 25:

                    g_DiscordLogger.warn( "Can not add all fields to the message \"<c>{}<>\" it's above discord's max capacity of 24 fields!", embed.title );

                    break;

                if isinstance( item, tuple ):

                    field_title = item[0];
                    if field_title is not None and len( field_title ) > 256:
                            field_title = field_title[ : 256 ];

                    field_description = item[1];
                    if field_description is not None and len( field_description ) > 1024:
                            field_description = field_description[ : 1024 ];

                    field_inline = item[2] if len(item) > 2 else True;

                    embed.add_field( name=field_title, value=field_description, inline =field_inline );

                else:

                    embed.add_field( name=field_title );

        if flags & LoggerFlags.PrintDiscord:

            if level in ( LoggerLevel.Critical, LoggerLevel.Error, LoggerLevel.AllLoggers ) or g_ConfigContext.log.LogLevels & level:

                self.__Messages.append( embed );

        return embed;

    def debug( self, message: str, *args, name: str = None,
        items: Union[ str, Optional[ tuple[ str, str, Optional[bool] ] ] ] = None,
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord )
    ) -> Embed:
        '''
            ``message``: Message to send

            ``args``: Arguments to format *message*

            ``name``: Custom name. if None it is "Bot"

            ``items``: fields to add to the embed, could be a str representing the title of a field or a tuple with either title and description only or a third item representing the inline boolean

            ``flags``: bits. PrintTerminal to print into the CMD, PrintDiscord to send to the discord server. or Nothing to just create the embed and do nothing else.

            Returns a discord.Embed
        '''
        return self.LogCore(message, RGB(100,100,200), "📝", "Debug", LoggerLevel.Debug, name, items, flags, *args );

    def trace( self, message: str, *args, name: str = None,
        items: Union[ str, Optional[ tuple[ str, str, Optional[bool] ] ] ] = None,
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord )
    ) -> Embed:
        '''
            ``message``: Message to send

            ``args``: Arguments to format *message*

            ``name``: Custom name. if None it is "Bot"

            ``flags``: bits. PrintTerminal to print into the CMD, PrintDiscord to send to the discord server. or Nothing to just create the embed and do nothing else.

            ``items``: fields to add to the embed, could be a str representing the title of a field or a tuple with either title and description only or a third item representing the inline boolean

            Returns a discord.Embed
        '''
        return self.LogCore(message, RGB(0,255,255), "➡", "Trace", LoggerLevel.Trace, name, items, flags, *args );

    def info( self, message: str, *args, name: str = None,
        items: Union[ str, Optional[ tuple[ str, str, Optional[bool] ] ] ] = None,
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord )
    ) -> Embed:
        '''
            ``message``: Message to send

            ``args``: Arguments to format *message*

            ``name``: Custom name. if None it is "Bot"

            ``items``: fields to add to the embed, could be a str representing the title of a field or a tuple with either title and description only or a third item representing the inline boolean

            ``flags``: bits. PrintTerminal to print into the CMD, PrintDiscord to send to the discord server. or Nothing to just create the embed and do nothing else.

            Returns a discord.Embed
        '''
        return self.LogCore(message, RGB(0,255,0), "❕", "Info", LoggerLevel.Information, name, items, flags, *args );

    def warn( self, message: str, *args, name: str = None,
        items: Union[ str, Optional[ tuple[ str, str, Optional[bool] ] ] ] = None,
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord )
    ) -> Embed:
        '''
            ``message``: Message to send

            ``args``: Arguments to format *message*

            ``name``: Custom name. if None it is "Bot"

            ``items``: fields to add to the embed, could be a str representing the title of a field or a tuple with either title and description only or a third item representing the inline boolean

            ``flags``: bits. PrintTerminal to print into the CMD, PrintDiscord to send to the discord server. or Nothing to just create the embed and do nothing else.

            Returns a discord.Embed
        '''
        return self.LogCore(message, RGB(255,200,0), "⚠️", "Warning", LoggerLevel.Warning, name, items, flags, *args );

    def error( self, message: str, *args, Exit:bool = False, name: str = None,
        items: Union[ str, Optional[ tuple[ str, str, Optional[bool] ] ] ] = None,
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord )
    ) -> Embed:
        '''
            ``message``: Message to send

            ``args``: Arguments to format *message*

            ``name``: Custom name. if None it is "Bot"

            ``items``: fields to add to the embed, could be a str representing the title of a field or a tuple with either title and description only or a third item representing the inline boolean

            ``flags``: bits. PrintTerminal to print into the CMD, PrintDiscord to send to the discord server. or Nothing to just create the embed and do nothing else.

            ``Exit``: if true the program is closed

            Returns a discord.Embed
        '''
        return self.__ShouldQuit__( self.LogCore(message, RGB(255,80,0), "‼️", "Error", LoggerLevel.Error, name, items, flags, *args ), Exit );

    def critical( self, message: str, *args, Exit:bool = False, name: str = None,
        items: Union[ str, Optional[ tuple[ str, str, Optional[bool] ] ] ] = None,
        flags: LoggerFlags = ( LoggerFlags.PrintTerminal | LoggerFlags.PrintDiscord )
    ) -> Embed:
        '''
            ``message``: Message to send

            ``args``: Arguments to format *message*

            ``name``: Custom name. if None it is "Bot"

            ``items``: fields to add to the embed, could be a str representing the title of a field or a tuple with either title and description only or a third item representing the inline boolean

            ``flags``: bits. PrintTerminal to print into the CMD, PrintDiscord to send to the discord server. or Nothing to just create the embed and do nothing else.

            ``Exit``: if true the program is closed

            Returns a discord.Embed
        '''
        return self.__ShouldQuit__( self.LogCore(message, RGB(255,0,0), "⛔", "Critical", LoggerLevel.Critical, name, items, flags, *args ), Exit );

    def __ShouldQuit__( self, Embed, Exit ) -> Embed:
        if Exit is True:
            from sys import exit;
            exit(1);
        return Embed;

global g_DiscordLogger;
g_DiscordLogger: DiscordLogger = DiscordLogger();