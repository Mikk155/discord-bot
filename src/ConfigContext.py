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

class ContextBot():

    @property
    def IsDeveloper( self ) -> bool:
        return False;

    @property
    def Prefix( self ) -> None | str:
        return self.__prefix__;

    @property
    def TargetGuildCommands( self ) -> None | int:
        return self.__guild__;
    __guild__ = None;

    token: str;

    def __init__( self, label: dict ) -> None:

        self.token = label.pop( "token", None );

        self.__prefix__ = label.pop( "prefix", None );

class ContextBotDeveloper( ContextBot ):

    @property
    def IsDeveloper( self ) -> bool:
        return True;

    def __init__( self, label: dict, guild ) -> None:
        self.__guild__ = guild;
        super().__init__( label );

class ContextBotLoggin():

    @property
    def MaxMessages( self ) -> int:
        return self.__max_mps__;

    @property
    def IsActive( self ) -> bool:
        return self.__active__;
    __active__ = False;

    @property
    def Channel( self ) -> int:
        return self.__channel__;

    LogLevels: int = 0;

    def __init__( self, label: dict ) -> None:

        if "bot" in label and "channel" in label:

            self.__active__ = True
            self.__channel__ = label[ "channel" ];
            self.__max_mps__ = label.get( "max_mps", 5 );

            from utils.Logger import ToLoggerLevel;

            for k, v in label[ "bot" ].items():
                if v is True:
                    self.LogLevels |= ToLoggerLevel(k);

class ConfigContext():

    '''
        Configuration contexts
    '''

    bot: ContextBot | ContextBotDeveloper;

    log: ContextBotLoggin;

    @property
    def Language( self ) -> str:
        return self.__language__;

    def __init__( self ) -> None:

        from utils.Path import Path;
        from utils.jsonc import jsonc;

        data = jsonc( Path.enter( "config", "bot.json" ) );

        DataDeveloper = data.pop( "developer", {} );

        self.bot = ContextBot( data[ "bot" ] ) if DataDeveloper.pop( "active", False ) is False \
            else ContextBotDeveloper( DataDeveloper[ "bot" ], DataDeveloper[ "guild" ] );

        self.__language__ = data.pop( "language", "english" );

        LogginContext: dict[ str, bool ] = data.pop( "Loggin", {} );

        from utils.Logger import LoggerSetLevel, LoggerClearLevel, ToLoggerLevel;

        for k, v in LogginContext[ "terminal" ].items():

            if v is True:
                LoggerSetLevel( ToLoggerLevel(k) )
            else:
                LoggerClearLevel( ToLoggerLevel(k) );

        self.log = ContextBotLoggin( LogginContext );

global g_ConfigContext;
g_ConfigContext: ConfigContext = ConfigContext();
