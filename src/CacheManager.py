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

from inspect import FrameInfo
from io import TextIOWrapper
from src.constants import TemporalCache;
from utils.Dictionary import Dictionary;

class CacheLabel( Dictionary ):

    def __init__( self, parent=None, key=None ) -> None:
        super().__init__( parent, key );

    @property
    def ToCodeBlock( self ) -> str:
        '''Return a rich code block for discord'''
        return f'```json\n{self.ToJson}\n``';

from src.Logger import g_DiscordLogger, LoggerFlags;
from datetime import timedelta, datetime;

class CacheManager:

    __cache__: CacheLabel = {};
    '''The whole cache (Do NOT modify directly! use g_Cache.Get())'''

    @property
    def GetCacheDir( self ) -> str:
        from utils.Path import Path;
        return Path.enter( "config", "cache.json", CreateIfNoExists = True, SupressWarning = True )

    def __init__( self ) -> None:
        from utils.jsonc import jsonc;
        self.__cache__ = CacheLabel( jsonc( self.GetCacheDir, exists_ok=True ) );

    def UpdateCache( self ) -> None:

        from json import dumps;

        try: # Store cache context
        #
            obj: str = dumps( self.__cache__.ToDict, indent=4 );

            if obj and len(obj) > 1:
            #
                file: TextIOWrapper = open( self.GetCacheDir, 'w' );
                file.write( obj );
                file.close();
            #
        #
        except Exception as e:
        #
            g_DiscordLogger.warn( "Failed to store the cache: <r>{}<>", e, flags=LoggerFlags.PrintTerminal );
        #

    def Get( self, label: str = None ) -> CacheLabel:

        '''
            Return a dict which automatically stores into the cache.json when setting variables to it
        '''

        if label is None:
        #
            from inspect import stack;

            frame: FrameInfo = stack()[1]; # Get caller plugin name

            from os.path import basename;
            label = basename( frame.filename );
        #

        return self.__cache__[ label ];

    def Set( self, label: str, value ) -> None:
        self.__cache__[ label ] = value;

    def SetTemporal( self, label: str, delta: timedelta, data: dict = None ) -> None:

        '''
            Set a temporal variable to the cache

            delta is how long time we should store it

            data is for your own usage when accessing through GetTemporal
        '''

        temp_vars: CacheLabel = g_Cache.Get( "temp" );

        time_diff: datetime = datetime.now() + delta;

        temp_vars[ label ] = [ time_diff.strftime( "%Y-%m-%d %H:%M:%S" ), data ];

    def GetTemporal( self, label: str ) -> tuple[ TemporalCache, datetime, dict ]:
        '''
            Get a temporal variable from the cache

            See TemporalCache for posible values and decriptions

            The third value may be None or not based on when the variable was stored.
        '''

        temp: CacheLabel = self.Get( "temp" );

        if label in temp:
        #
            temp_variable: CacheLabel = temp[ label ];

            time: datetime = datetime.strptime( temp_variable[0], "%Y-%m-%d %H:%M:%S" );

            if datetime.now() > time:
            #
                temp.pop( label );
                return ( TemporalCache.Expired, time, temp_variable[1] );
            #
            return ( TemporalCache.Exists, time, temp_variable[1] );
        #
        return ( TemporalCache.NoExists, None, None );

global g_Cache;
g_Cache: CacheManager = CacheManager();
