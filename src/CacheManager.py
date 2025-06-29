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

class CacheManager:

    from utils.Logger import Logger
    m_Logger = Logger( "Cache System" );

    __cache__: CCacheDictionary = {};
    '''The whole cache (Do NOT modify directly! use g_Cache.get())'''

    @property
    def GetCacheDir( self ) -> str:
        from utils.Path import Path;
        return Path.enter( "config", "cache.json", CreateIfNoExists = True, SupressWarning = True )

    def __init__( self ):
        
        from utils.jsonc import jsonc;

        from src.BotLoggin import g_BotLogger;
        self.__cache__ = CCacheDictionary( jsonc( self.GetCacheDir, exists_ok=True ) );

    def UpdateCache( self ):

        from json import dumps;

        try: # Store cache context

            obj = dumps( dict(self.__cache__), indent=4 );

            if obj and len(obj) > 1:

                open( self.GetCacheDir, 'w' ).write( obj );

        except Exception as e:

            self.m_Logger.warn( "Failed to store the cache: <r>{}<>", e );

    def get( self, label: str = None ) -> CCacheDictionary:

        '''
            Return a dict which automatically stores into the cache.json when setting variables to it
        '''

        if label is None:

            from inspect import stack;

            frame = stack()[1]; # Get caller plugin name

            from os.path import basename;
            label = basename( frame.filename );

        return self.__cache__[ label ];

global g_Cache;
g_Cache: CacheManager = CacheManager();
