# Fix relative library importing by appending the directory of *this* file in the sys path.
import sys
from os.path import abspath, dirname, exists;
MyWorkspace: str = abspath( dirname( __file__ ) );

sys.path.append( MyWorkspace );

from utils.Path import Path;
Path.SetWorkspace( MyWorkspace );

from src.ConfigContext import g_ConfigContext;

if not g_ConfigContext.developer:

    from src.InstallRequirements import InstallRequirements;
    InstallRequirements( Path.enter( "requirements.txt" ) );
    InstallRequirements( Path.enter( "utils", "requirements.txt" ) );

from src.main import g_Logger;
from src.main import bot;

from src.PluginManager import g_PluginManager;
g_PluginManager.CallFunction( "OnInitialize" );

try:

    from src.ConfigContext import g_ConfigContext;

    TokenFile: str;

    if g_ConfigContext.developer:

        TokenFile = g_ConfigContext.developer_token;
    
    else:

        TokenFile = g_ConfigContext.token;

    TokenPath = Path.enter( "config", TokenFile );

    if not exists( TokenPath ):

        g_Logger.critical( "File <g>{}<> Doesn't exists!", TokenPath, Exit=True );

    Token = open( TokenPath, "r" ).read();

    bot.run( token = Token, reconnect = True );

except Exception as e:

    g_Logger.critical( "Exception: <r>{}<>", e, Exit=True );
