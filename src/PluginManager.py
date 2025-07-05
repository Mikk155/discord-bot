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

from src.Plugin import Plugin;
from src.Sentences import g_Sentences;
from src.Logger import g_DiscordLogger;

class PluginManager():

    @property
    def GetName( self ) -> str:
        return "Plugin Manager";

    Plugins: list[Plugin] = [];

    def __init__( self ):
        print( "Initialized plugin manager")

    def Initialize( self ):

        from sys import executable;
        from os.path import exists;
        from utils.Path import Path;
        from utils.jsonc import jsonc;
        from pathlib import Path as PathLib;
        from subprocess import check_call;
        from src.ConfigContext import g_ConfigContext;
        from importlib.util import spec_from_file_location, module_from_spec;

        PluginsContext: list[dict] = jsonc( Path.enter( "config", "plugins.json" ) );
    
        PluginsContext.pop( "$schema", "" );

        for PluginName, PluginData in PluginsContext.items():

            g_DiscordLogger.trace( g_Sentences.get( "registering_plugin", PluginName ), name=self.GetName );

            if not g_ConfigContext.IsDeveloper and "requirements" in PluginData:

                requirements = PluginData[ "requirements" ];

                if requirements and requirements != '':

                    requirements_path = Path.enter( "plugins", f'{requirements}.txt' );

                    if exists( requirements_path ):

                        check_call( [ executable, "-m", "pip", "install", "-r", requirements_path ] );

                    else:

                        g_DiscordLogger.warn( g_Sentences.get( "invalid_requirements", PluginName ), name=self.GetName );
                        continue;

            script_path = PathLib( Path.enter( "plugins", f'{PluginName}.py' ) );

            module_name = script_path.stem;

            spec = spec_from_file_location( module_name, script_path );

            module = module_from_spec( spec );

            spec.loader.exec_module( module );

            if not hasattr( module, module_name ):

                g_DiscordLogger.error( g_Sentences.get( "fail_plugin_class", module_name, module_name, script_path ), name=self.GetName );

                continue;

            plugin: Plugin = getattr( module, module_name )();

            plugin.guilds = PluginData.get( "guilds", [] );

            plugin.filename = PluginName;

            plugin.disabled = PluginData.get( "disabled", False );

            if plugin.disabled is True:

                g_DiscordLogger.debug( g_Sentences.get( "plugin_disabled", PluginName ), name=self.GetName );

            else:

                plugin.OnPluginActivate();

            self.Plugins.append( plugin );

    @property
    def GetCurrentPlugin( self ) -> Plugin:

        from inspect import stack;
        from os.path import splitext, basename;

        Frame = stack()[1];

        Caller = splitext( basename( Frame.filename ) )[0];

        Any = [ plugin for plugin in self.Plugins if plugin.__class__.__name__ == Caller ];

        return Any[0] if len(Any) > 0 else None;

    async def CallFunction( self, fnName: str, *args, Guild = -1 ) -> None:

        for p in self.Plugins:

            if p.disabled is True:
                continue;

            if len( p.guilds ) > 0 and Guild != -1 and ( Guild is None or Guild.id in p.guilds ):
                continue; # This plugin doesn't want to work on this guild.

            try:

                fn = getattr( p, fnName );

                if len(args) > 0:

                    if await fn(*args) is False:

                        break;

                elif await fn() is False:

                    break;

            except Exception as e:

                from src.Bot import bot;
                bot.HandleException( e, SendToDevs=True );

global g_PluginManager;
g_PluginManager: PluginManager = PluginManager();
