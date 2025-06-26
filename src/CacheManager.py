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

        self.__cache__ = CCacheDictionary( jsonc( self.GetCacheDir, exists_ok=True ) );

    def UpdateCache( self ):

        from json import dumps;

        try: # Store cache context

            obj = dumps( dict(self.__cache__), indent=4 );

            if obj and len(obj) > 1:

                open( self.GetCacheDir, 'w' ).write( obj );

            else:

                self.m_Logger.warn( "Failed to store the cache" );

        except Exception as e:

            self.m_Logger.warn( "Failed to store the cache: <r>{}<>", e );

    def get( self, label: str = None ) -> CCacheDictionary:

        '''
            Return a dict which automatically stores into the cache.json when setting variables to it
        '''

        if label is None:

            from inspect import stack;

            frame = stack()[1]; # Get caller plugin name

            label = frame.filename;

        return self.__cache__[ label ];

global g_Cache;
g_Cache: CacheManager = CacheManager();
