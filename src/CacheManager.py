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

from src.constants import TemporalCache;
from utils.Dictionary import Dictionary;

from src.Logger import g_DiscordLogger, LoggerFlags;
from datetime import timedelta, datetime;

class CacheDictionary( Dictionary ):

    @property
    def ToCodeBlock( self ) -> str:
        '''Return a rich code block for discord'''
        return f'```json\n{self.Serialize}\n``';

    @property
    def PluginName( self ) -> str:
    #
        from inspect import stack, FrameInfo;
        frame: FrameInfo = stack()[1]; # Get caller plugin name
        from os.path import basename;
        return basename( frame.filename );
    #

    @property
    def Plugin( self ) -> "Dictionary":
    #
        from inspect import stack, FrameInfo;
        frame: FrameInfo = stack()[1]; # Get caller plugin name
        from os.path import basename;
        PluginName: str = basename( frame.filename );
        return self[ PluginName ];
    #

    def SetTemporal( self, label: str, delta: timedelta, data: str = None ) -> None:
    #
        '''
            Set a temporal variable to the cache

            delta is how long time we should store it

            data is for your own usage when accessing through GetTemporal
        '''

        time_diff: datetime = datetime.now() + delta;

        self[ "temp" ][ label ] = { "time": time_diff.strftime( "%Y-%m-%d %H:%M:%S" ), "data": data };
    #

    def GetTemporal( self, label: str ) -> tuple[ TemporalCache, datetime, str ]:
    #
        '''
            Get a temporal variable from the cache

            See TemporalCache for posible values and decriptions

            The third value may be None or not based on when the variable was stored.
        '''

        temp: Dictionary = self[ "temp" ];

        if label in temp:
        #
            temp_variable: Dictionary = temp[ label ];

            time: datetime = datetime.strptime( temp_variable[ "time" ], "%Y-%m-%d %H:%M:%S" );

            if datetime.now() > time:
            #
                temp.pop( label );
                return ( TemporalCache.Expired, time, temp_variable[ "data" ] );
            #
            return ( TemporalCache.Exists, time, temp_variable[ "data" ] );
        #
        return ( TemporalCache.NoExists, None, None );
    #

def __GetCacheDir__() -> str:
#
    from utils.Path import Path;
    return Path.enter( "config", "cache.json", CreateIfNoExists = True, SupressWarning = True )
#

def __UpdateCache__() -> None:
#
    try: # Store cache context
    #
        with open( __GetCacheDir__(), 'w' ) as f:
        #
            global g_Cache;
            f.write( g_Cache.ToJson( indent=1 ) );
        #
    #
    except Exception as e:
    #
        g_DiscordLogger.warn( "Failed to store the cache: <r>{}<>", e, flags=LoggerFlags.PrintTerminal );
    #
#

global g_Cache;

from utils.jsonc import jsonc;
__data__: jsonc = jsonc( __GetCacheDir__(), exists_ok=True );

g_Cache: CacheDictionary = CacheDictionary.FromDict( __data__, fnCallback=__UpdateCache__ );
