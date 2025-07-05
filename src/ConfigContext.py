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

from utils.jsonc import jsonc;
from discord import User, Member;
from src.constants import LoggerLevel;

class ContextBot():

    @property
    def Prefix( self ) -> None | str:
        return self.__prefix__;

    @property
    def TargetGuildCommands( self ) -> None | int:
        return self.__guild__;

    __token__: str;

    def __init__( self, label: jsonc ) -> None:

        self.__guild__: int | None = label.pop( "developer_guild", None );
        self.__prefix__: str | None = label.pop( "prefix", None );
        self.__owner__: int | None = label.pop( "owner", None );

        self.__token_method__: int = ( "env", "file", "argument" ).index( label[ "token_method" ] );

        match self.__token_method__:

            case 0:
            #
                from os import getenv;
                env_name: str = label[ "token" ];
                TokenEnv: str | None = getenv( env_name );

                if TokenEnv is None:
                #
                    print( f"ENV {env_name} doesn't exists!" );
                    exit(1);
                #
                else:
                #
                    self.__token__ = TokenEnv;
                #
            #
            case 1:
            #
                from os.path import exists;
                from utils.Path import Path;

                TokenPath = Path.enter( "config", label[ "token" ] );

                if not exists( TokenPath ):
                #
                    print( f"File {TokenPath} doesn't exists!" );
                    exit(1);
                #
                else:
                #
                    self.__token__ = open( TokenPath, "r" ).read();
                #
            #
            case 2:
            #

                import sys;

                if not '-token' in sys.argv:
                #
                    print( "No -token argument given!" );
                    exit(1);
                #
                elif len(sys.argv) == sys.argv.index( '-token' ) + 1:
                #
                    print( "No token given after the -token argument!" );
                    exit(1);
                #
                else:
                #
                    self.__token__ = sys.argv[ sys.argv.index( '-token' ) + 1 ];
                #
            #

class ContextBotLoggin():

    @property
    def MaxMessages( self ) -> int:
        return self.__max_mps__;

    @property
    def IsActive( self ) -> bool:
        return self.__active__;

    @property
    def Channel( self ) -> int:
        return self.__channel__;

    @property
    def Guild( self ) -> int:
        return self.__guild__;

    LogLevels: LoggerLevel = ( LoggerLevel.Critical | LoggerLevel.Error );

    def __init__( self, label: jsonc ) -> None:

        self.__active__: bool = label[ "active" ];

        if self.__active__ is False:
        #
            return;
        #

        self.__max_mps__: int = label[ "max_mps" ];
        self.__channel__: int = label[ "channel" ];
        self.__guild__: int = label[ "guild" ];

        __LoggerLevels__: dict[ str, bool ] = label[ "Loggers" ];

        from utils.Logger import ToLoggerLevel;

        for k, v in __LoggerLevels__.items():
        #
            if v is True:
            #
                self.LogLevels |= ToLoggerLevel(k);
            #
        #

class ConfigContext():

    '''
        Configuration contexts
    '''

    bot: ContextBot;

    log: ContextBotLoggin;

    @property
    def IsDeveloper( self ) -> bool:
        return self.__developer__;

    def IsOwner( self, user: User | Member | int ) -> bool:
        '''
            Returns whatever this user is the owner of this app
        '''
        if self.bot.__owner__ is None:
        #
            return False;
        #
        elif isinstance( user, int ):
        #
            return ( self.bot.__owner__ == user );
        #
        return ( user and self.bot.__owner__ == user.id );

    def __init__( self ) -> None:

        from sys import argv;
        self.__developer__: bool = True if '-dev' in argv or '-developer' in argv else False;

        from utils.Path import Path;

        try:
        #
            LogginData = jsonc( Path.enter( "config", "Loggin.json" ), schema_validation=Path.enter( "schemas", "Loggin.json" ) );
            self.log = ContextBotLoggin( LogginData );
            del LogginData;

            BotData = jsonc( Path.enter( "config", "bot.json" ), schema_validation=Path.enter( "schemas", "bot.json" ) );
            self.bot = ContextBot( BotData );
            del BotData;
        #
        except Exception as e:
        #
            print( f"Critical json validation: {e}" );
            exit(1);
        #

global g_ConfigContext;
g_ConfigContext: ConfigContext = ConfigContext();
