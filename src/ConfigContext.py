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

    def __init__( self ) -> None:

        from utils.Path import Path;
        from utils.jsonc import jsonc;

        super().__init__( jsonc( Path.enter( "config", "bot.json" ) ) );

        DeveloperContext: dict = self.pop( "developer", {} );
        self.developer = DeveloperContext.pop( "active", False );
        self.developer_token = DeveloperContext.pop( "token", None );
        self.developer_guild = DeveloperContext.pop( "guild", None );

        if self.developer_guild is None or self.developer_token is None:

            self.developer = False;

        self.token = self.pop( "token", None );

global g_ConfigContext;
g_ConfigContext: ConfigContext = ConfigContext();
