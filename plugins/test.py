from src.PluginManager import Plugin

class test( Plugin ):
    def __init__( self ):
        print( "Hello world from test" );
        super().__init__();
