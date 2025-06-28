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

# Fix relative library importing by appending the directory of *this* file in the sys path.
import sys
from os.path import abspath, dirname, exists;
MyWorkspace: str = abspath( dirname( __file__ ) );

sys.path.append( MyWorkspace );

from utils.Path import Path;
Path.SetWorkspace( MyWorkspace );

if "-licence" in sys.argv:
    from utils.fmt import fmt;
    fmt.FormatSourcesWithLicence( Path.enter( "LICENCE.txt" ), sources_folder=Path.enter( "src" ) );
    fmt.FormatSourcesWithLicence( Path.enter( "LICENCE.txt" ), sources_folder=Path.enter( "utils" ) );
    exit(0);
from src.ConfigContext import g_ConfigContext;

if not g_ConfigContext.bot.IsDeveloper:

    from src.InstallRequirements import InstallRequirements;
    InstallRequirements( Path.enter( "requirements.txt" ) );
    InstallRequirements( Path.enter( "utils", "requirements.txt" ) );

from src.main import g_Logger;
from src.main import bot;

# -TODO Lazy shit, maybe importlib events/*?
from src.events.on_member_join import on_member_join;
from src.events.on_member_remove import on_member_remove;
from src.events.on_message_delete import on_message_delete;
from src.events.on_message_edit import on_message_edit;
from src.events.on_message import on_message;
from src.events.on_reaction_add import on_reaction_add;
from src.events.on_reaction_remove import on_reaction_remove;
from src.events.on_ready import on_ready;

from asyncio import run as AsyncRun;
from src.PluginManager import g_PluginManager;
AsyncRun( g_PluginManager.CallFunction( "OnInitialize" ) );

try:

    from src.ConfigContext import g_ConfigContext;

    TokenPath = Path.enter( "config", g_ConfigContext.bot.token );

    if not exists( TokenPath ):

        g_Logger.critical( "File <g>{}<> Doesn't exists!", TokenPath, Exit=True );

    Token = open( TokenPath, "r" ).read();

    bot.run( token = Token, reconnect = True );

except Exception as e:

    g_Logger.critical( "Exception: <r>{}<>", e, Exit=True );
