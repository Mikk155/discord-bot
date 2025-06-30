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

class CCacheDictionary( dict ):

    def __getitem__( self, key ):

        if key not in self:

            self[ key ] = CCacheDictionary();

        return super().__getitem__( key );

    def __setitem__( self, key, value ):

        if isinstance( value, dict ):

            value = CCacheDictionary( value );

        super().__setitem__( key, value );

    def __repr__( self ):

        from json import dumps;

        return dumps( super().__repr__(), indent=4 );

from utils.Logger import Logger;
from datetime import timedelta, datetime;

class CacheManager:

    m_Logger = Logger( "Cache System" );

    __cache__: CCacheDictionary = {};
    '''The whole cache (Do NOT modify directly! use g_Cache.Get())'''

    @property
    def GetCacheDir( self ) -> str:
        from utils.Path import Path;
        return Path.enter( "config", "cache.json", CreateIfNoExists = True, SupressWarning = True )

    def __init__( self ):
        
        from utils.jsonc import jsonc;
        self.__cache__ = CCacheDictionary( jsonc( self.GetCacheDir, exists_ok=True ) );

    def UpdateCache( self ):

        from json import dumps;

        try: # Store cache context

            obj = dumps( dict(self.__cache__), indent=4 );

            if obj and len(obj) > 1:

                open( self.GetCacheDir, 'w' ).write( obj );

        except Exception as e:

            self.m_Logger.warn( "Failed to store the cache: <r>{}<>", e );

    def Get( self, label: str = None ) -> CCacheDictionary:

        '''
            Return a dict which automatically stores into the cache.json when setting variables to it
        '''

        if label is None:

            from inspect import stack;

            frame = stack()[1]; # Get caller plugin name

            from os.path import basename;
            label = basename( frame.filename );

        return self.__cache__[ label ];

    def Set( self, label: str, value ) -> None:

        self.__cache__[ label ] = value;

    def SetTemporal( self, label: str, delta: timedelta, data: dict = None ) -> None:

        '''
            Set a temporal variable to the cache

            delta is how long time we should store it

            data is for your own usage when accessing through GetTemporal
        '''

        temp_vars = g_Cache.Get( "temp" );

        time_diff = datetime.now() + delta;

        temp_vars[ label ] = [ time_diff.strftime( "%Y-%m-%d %H:%M:%S" ), data ];

    def GetTemporal( self, label: str ) -> tuple[ TemporalCache, datetime, dict ]:
        '''
            Get a temporal variable from the cache

            See TemporalCache for posible values and decriptions

            The third value may be None or not based on when the variable was stored.
        '''

        temp = self.Get( "temp" );

        if label in temp:

            temp_variable = temp[ label ];

            time = datetime.strptime( temp_variable[0], "%Y-%m-%d %H:%M:%S" );

            if datetime.now() > time:

                temp.pop( label );

                return ( TemporalCache.Expired, time, temp_variable[1] );

            return ( TemporalCache.Exists, time, temp_variable[1] );

        return ( TemporalCache.NoExists, None, None );

global g_Cache;
g_Cache: CacheManager = CacheManager();
