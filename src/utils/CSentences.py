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

    sentences: dict[dict] = {};
    '''Dict of sentences'''

    @staticmethod
    def initialize() -> None:

        from src.utils.CJsonCommentary import jsonc;

        from src.utils.Path import g_Path;

        __plugins__ = jsonc.load( g_Path.join( "sentences.json" ) )

        g_Sentences.sentences = __plugins__;

        print(g_Sentences.sentences)

    @staticmethod
    def push_back( file_dir: str ) -> None:
        '''
        Push a sentences json into the main sentences

        **NOTE:** The sentences will be formated and the keys will be prefixed with the plugin's filename

        So for example your plugin is called ``Activity.py`` and your sentence is ``display`` it will be accessed as ``Activity.display``
        '''


    from src.constdef import INVALID_INDEX;

    @staticmethod
    def get(name: str, server_id: int = INVALID_INDEX() ):
        
        '''
        Gets a sentence from the sentences json
        
        depending on the global language or server-language if index is provided
        '''
        __sentence__: str = None;

        if name in g_Sentences.sentences:

            __sslot__ = g_Sentences.sentences[ name ];

            # -TODO Get from cache system
            __language__ = "english"

            from src.constdef import INVALID_INDEX;

            if server_id != INVALID_INDEX():

                # -TODO Get from cache system for this specific server
                __language__ = "english"

            if __language__ in __sslot__:

                __sentence__ = __sslot__[ __language__ ];

        if __sentence__ is None:

            return f"#{name}";
    
        return __sentence__;