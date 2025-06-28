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

class ConfigContext( dict ):

    '''
        Configuration context
    '''

    developer: bool;
    '''Is this bot running on developer mode?'''
    developer_token: str;
    '''Bot token to use if developer is true'''
    developer: int;
    '''Guild target to update commands if developer is true'''

    token: str;
    '''Bot token to use'''

    prefix: str = None;

    language: str = "english";
    '''Default language to use for sentences'''

    def __init__( self ) -> None:

        from utils.Path import Path;
        from utils.jsonc import jsonc;

        super().__init__( jsonc( Path.enter( "config", "bot.json" ) ) );

        self.DeveloperContext();
        self.token = self.pop( "token", None );
        self.prefix = self.pop( "prefix", None );
        self.language = self.pop( "language", "english" );
        self.LoggerContext();

    def DeveloperContext( self ) -> None:

        self.pop( "$schema", "" );

        DeveloperContext: dict = self.pop( "developer", {} );
        self.developer = DeveloperContext.pop( "active", False );
        self.developer_token = DeveloperContext.pop( "token", None );
        self.developer_guild = DeveloperContext.pop( "guild", None );

        if self.developer_guild is None or self.developer_token is None:
            self.developer = False;

    def LoggerContext( self ) -> None:

        from utils.Logger import LoggerSetLevel, LoggerClearLevel, LoggerLevel;

        LoggerContext: dict[ str, bool ] = self.pop( "Logger", {} );

        if LoggerContext.pop( "Warning", False ):
            LoggerSetLevel( LoggerLevel.Warning );
        else:
            LoggerClearLevel( LoggerLevel.Warning );

        if LoggerContext.pop( "Information", False ):
            LoggerSetLevel( LoggerLevel.Information );
        else:
            LoggerClearLevel( LoggerLevel.Information );

        if LoggerContext.pop( "Debug", False ):
            LoggerSetLevel( LoggerLevel.Debug );
        else:
            LoggerClearLevel( LoggerLevel.Debug );

        if LoggerContext.pop( "Trace", False ):
            LoggerSetLevel( LoggerLevel.Trace );
        else:
            LoggerClearLevel( LoggerLevel.Trace );

global g_ConfigContext;
g_ConfigContext: ConfigContext = ConfigContext();
