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

# When not :)
from typing import *;

from scripts.FixRelativeImport import SetWorkspace;

WORKSPACE: str = SetWorkspace(__file__);

from scripts.InstallRequirements import InstallRequirements;

if __name__ == "__main__":

    import sys;

    if not '-dev' in sys.argv:
    #
        from scripts.UpdateRepository import UpdateRepoSubmodules;
        UpdateRepoSubmodules( WORKSPACE );

        from os.path import join;
        InstallRequirements( join( WORKSPACE, "requirements.txt" ) ); # < These should already be installed by the user.
        InstallRequirements( join( join( WORKSPACE, "utils" ), "requirements.txt" ) );
    #

    # Set workspace for Path to work propertly
    from utils.Path import Path;
    Path.SetWorkspace( WORKSPACE );

from src.constants import LoggerFlags;

global g_DiscordLogger;
from src.Logger import g_DiscordLogger;

global g_ConfigContext;
from src.ConfigContext import g_ConfigContext;

global bot;
from src.Bot import bot;

global g_PluginManager;
from src.PluginManager import g_PluginManager;

if __name__ == "__main__":

    SourceFolders: tuple[str] = ( "events", "commands" );

    from os import walk;
    from os.path import join;
    from pathlib import Path as PathLib;
    from importlib.util import spec_from_file_location, module_from_spec;
    from importlib.machinery import ModuleSpec;
    from types import ModuleType;

    SourcesFolder: str = join( WORKSPACE, "src" );

    for SourceFolder in SourceFolders:
    #
        for root, _, SourceFiles in walk( join( SourcesFolder, SourceFolder ) ):
        #
            for SourceFile in SourceFiles:
            #
                if SourceFile.endswith( ".py" ):
                #
                    SourceFile = PathLib( join( root, SourceFile ) );
                    spec: ModuleSpec = spec_from_file_location( SourceFile.stem, SourceFile );

                    module: ModuleType = module_from_spec( spec );

                    spec.loader.exec_module( module );
                #
            #
        #
    #

    g_PluginManager.Initialize();
    from asyncio import run as AsyncRun;
    AsyncRun( g_PluginManager.CallFunction( "OnInitialize" ) );

    try:
    #
        from src.ConfigContext import g_ConfigContext;
        bot.run( token = g_ConfigContext.bot.__token__, reconnect = True );
        del g_ConfigContext.bot.__token__;
    #
    except Exception as e:
    #
        g_DiscordLogger.critical( "Exception: <r>{}<>", e, Exit=True, flags=LoggerFlags.PrintTerminal );
    #
