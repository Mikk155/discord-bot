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

    def __init__( self ) -> None:

        from utils.Path import Path;
        from utils.jsonc import jsonc;

        super().__init__( jsonc( Path.enter( "config", "bot.json" ) ) );

        self.DeveloperContext();
        self.token = self.pop( "token", None );
        self.prefix = self.pop( "prefix", None );
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
