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

class g_Sentences:

    '''
    Sentences
    '''

    from src.CLogger import CLogger
    m_Logger = CLogger( "Sentences" );

    sentences: dict[dict] = {};
    '''Dict of sentences'''

    languages = [ "english" ];
    '''Supported languages'''

    __filenames__ = [];

    @staticmethod
    def push_back( filename: str ) -> None:
        '''
        Push a sentences json into the main sentences

        **NOTE:** The sentences will be formated and the keys will be prefixed with ``{filename}.{}``
    
        **NOTE:** If ``filename`` has been registered before this won't be added
        '''

        if not filename in g_Sentences.__filenames__:

            from src.utils.CJsonCommentary import jsonc;

            from src.utils.Path import g_Path;

            __sentences__ = jsonc.load( g_Path.join( f"sentences/plugins/{filename}.json" ) )

            for k, v in __sentences__.items():

                g_Sentences.sentences[ f'{filename}.{k}' ] = v;

            g_Sentences.__filenames__.append( filename );


    @staticmethod
    def initialize() -> None:

        from src.utils.Path import g_Path;
        from src.utils.CJsonCommentary import jsonc;

        g_Sentences.languages = jsonc.load( g_Path.join( "sentences/__langs__.json" ) );
        g_Sentences.sentences = jsonc.load( g_Path.join( "sentences/__main__.json" ) );

        g_Sentences.m_Logger.info( "object_initialized", [ __name__ ], dev=True );

    from src.constdef import INVALID_INDEX;

    @staticmethod
    def get(name: str, id: int = None, maps: list[str] = None ) -> str:
        
        '''
        Gets a sentence from the sentences json
        
        depending on the global language or server-language if index is provided
        '''
        __sentence__: str = None;

        if name in g_Sentences.sentences:

            __sslot__ = g_Sentences.sentences[ name ];

            __language__ = "english"

            if id:

                from src.CCacheManager import g_Cache;

                cache = g_Cache.get( "language.py" );

                __language__ = cache.get( str( id ), "english" );

            if __language__ in __sslot__:

                __sentence__ = __sslot__[ __language__ ];

            else:

                __sentence__ = __sslot__[ 'english' ];

        if __sentence__ is None:

            return f"{name}";

        if maps:

            from src.utils.format import g_Format;

            __sentence__ = g_Format.brackets( __sentence__, maps );

        return __sentence__;
