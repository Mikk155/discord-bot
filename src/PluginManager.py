class Plugin():

    '''
        Plugin base. every plugin must inherit from this class

        Every method should return a boolean, True for keep executing plugins in the list. False if the plugin manager should stop calling subsequent plugins.
    '''

    guilds: list[int] = [];
    '''Guilds list to only listen events (if empty == all)'''

    def __init__( self ):
        ''''''

    async def OnInitialize( self ) -> bool:
        '''The python scripts has just been run. This is called before the bot is running and just after every plugin has been loaded'''
        return True;

    async def OnBotStart( self ) -> bool:
        '''Called once. when the bot first starts.'''
        return True;

    async def OnReconnect( self ) -> bool:
        '''Called when the bot is back online after a connection lost'''
        return True;

    from datetime import datetime;
    async def OnThink( self, time: datetime ) -> bool:
        '''Called every second. time is the current time when the plugin manager is just called. use this as a prediction.'''
        return True;

    from discord import Member;
    async def OnMemberLeave( self, user: Member ) -> bool:
        '''when a user leaves a guild'''
        return True;

    async def OnMemberJoin( self, user: Member ) -> bool:
        '''when a user joins a guild'''
        return True;

class PluginManager():

    from utils.Logger import Logger
    m_Logger = Logger( "Plugin Manager" );

    Plugins: list[Plugin] = [];

    def __init__( self ):

        from os.path import exists;
        from utils.Path import Path;
        from utils.jsonc import jsonc;
        from pathlib import Path as PathLib;
        from src.ConfigContext import g_ConfigContext;
        from src.InstallRequirements import InstallRequirements;
        from importlib.util import spec_from_file_location, module_from_spec;

        PluginsContext: list[dict] = jsonc( Path.enter( "config", "plugins.json" ) );
    
        for PluginName, PluginData in PluginsContext.items():

            if PluginData.get( "disabled", False ) is True:
                self.m_Logger.debug( "Plugin \"<c>{}<>\" disabled by config.", PluginName );
                continue;

            self.m_Logger.info( "Registering plugin \"<c>{}<>\"", PluginName );

            if not g_ConfigContext.developer and "requirements" in PluginData:

                requirements = PluginData[ "requirements" ];

                if requirements and requirements != '':

                    requirements_path = Path.enter( "plugins", f'{requirements}.txt' );

                    if exists( requirements_path ):

                        InstallRequirements( requirements_path );

                    else:

                        self.m_Logger.warn( "Invalid requirement file \"<c>{}<>\" for plugin <g>{}<>", PluginName );

            script_path = PathLib( Path.enter( "plugins", f'{PluginName}.py' ) );

            module_name = script_path.stem;

            spec = spec_from_file_location( module_name, script_path );

            module = module_from_spec( spec );

            spec.loader.exec_module( module );

            if not hasattr( module, module_name ):

                self.m_Logger.error( "Couldn't find object \"<c>{}<>\" in module \"<g>{}<>\" in the script \"<g>{}<>\"", module_name, module_name, script_path );

                continue;

            plugin = getattr( module, module_name )();

            plugin.guilds = PluginData.get( "guilds", [] );

            self.push_back( plugin );

    def push_back( self, plugin: Plugin ):

        self.Plugins.append( plugin );

    async def CallFunction( self, fnName: str, *args, GuildID = None ) -> None:

        for p in self.Plugins:

            if GuildID is not None and len( p.guilds ) > 0 and not GuildID in p.guilds:
                continue; # This plugin doesn't want to work on this guild.

            fn = getattr( p, fnName );

            if len(args) > 0:

                if await fn(*args) is False:

                    break;

            elif await fn() is False:

                break;

global g_PluginManager;
g_PluginManager: PluginManager = PluginManager();
