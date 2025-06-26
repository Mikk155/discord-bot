class Plugin():

    def __init__( self ):
        print( "Hello world from PluginManager Plugin Base" );

    def OnInitialize( self ) -> bool:
        '''The python scripts has just been run. This is called before the bot is running and just after every plugin has been loaded'''
        return True;

class PluginManager():

    from utils.Logger import Logger
    m_Logger = Logger( "Plugin Manager" );

    Plugins: list = [];

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

            self.push_back( plugin );

        return 

    def push_back( self, plugin: Plugin ):

        self.Plugins.append( plugin );

    def CallFunction( self, fnName: str, *args ) -> None:

        for plugin in self.Plugins:

            fn = getattr( plugin, fnName );

            if len(args) > 0:

                if fn(*args) is False:

                    break;

            elif fn() is False:

                break;

global g_PluginManager;
g_PluginManager: PluginManager = PluginManager();
