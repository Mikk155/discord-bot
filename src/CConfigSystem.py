"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

class g_Config:
    
    '''
    Configuration System
    '''

    from src.CLogger import CLogger
    m_Logger = CLogger( "Configuration System" );

    configuration: dict = {};
    '''General configuration'''

    plugins: dict = {};
    '''Loaded plugins'''

    @staticmethod
    def initialize() -> None:

        from src.utils.Path import g_Path;
        from src.utils.CJsonCommentary import jsonc;
        from src.constdef import INVALID_INDEX;

        __plugins__ = jsonc.load( g_Path.join( "plugins.json" ) )

        loggers = __plugins__.get( "loggers", [ "debug", "warning", "info", "trace" ] );
        loggers.append( "critical" );
        loggers.append( "error" );
        g_Config.configuration[ "loggers" ] = loggers;
        g_Config.configuration[ "server_id" ]  = __plugins__.get( "server_id", INVALID_INDEX() );
        g_Config.configuration[ "log_id" ]     = __plugins__.get( "log_id", INVALID_INDEX() );
        g_Config.configuration[ "owner_id" ]   = __plugins__.get( "owner_id", INVALID_INDEX() );
        g_Config.configuration[ "github_id" ]  = __plugins__.get( "github_id", INVALID_INDEX() );

        g_Config.plugins = __plugins__.get( "plugins", [] );

        g_Config.m_Logger.info(
            "object.initialized",
            [
                __name__
            ],
            dev=True
        );