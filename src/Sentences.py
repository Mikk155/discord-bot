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

from utils.Path import Path;
from utils.jsonc import jsonc;
from discord import Guild

class Sentences( dict ):

    @property
    def GetName( self ) -> str:
        return "Sentences";

    def __init__( self ):

        super().__init__( jsonc( Path.enter( "sentences", "bot.json" ), exists_ok=True ) );

    def push_back( self, filename: str ) -> None:

        '''
            Push a custom sentences into this object.

            The file path is default set to sentences/ and no .json extension should be specified.

            Have a prefix to avoid conflicts.

            These sentences are merged in this object
        '''

        NewSentences = jsonc( Path.enter( "sentences", filename + ".json" ), exists_ok=True );

        for s, o in NewSentences.items():

            if not s in self:
    
                self[ s ] = o;

            else:

                g_DiscordLogger.warn( self.get( "sentence_already_exists", s ), name=self.GetName );

    def get( self, name: str, *args, Guild: Guild | int = None ) -> str:

        if not name in self:

            # Prevent recursion. check if exists
            g_DiscordLogger.warn( self.get( "sentence_no_exists", name ) if "sentence_no_exists" in self else '', name=self.GetName );

            return name;

        SentenceGroup: dict = super().__getitem__( name );

        Sentence: str = None;

        from src.CacheManager import g_Cache;

        cache = g_Cache.Get( "language" );

        if Guild is not None:

            GuildID = str( Guild if isinstance( Guild, int ) else Guild.id );

            if GuildID in cache:

                Sentence = SentenceGroup.get( cache[ GuildID ], None );

        from src.ConfigContext import g_ConfigContext;

        DefaultLanguage = g_ConfigContext.Language;

        if Sentence is None:

            if DefaultLanguage in SentenceGroup:

                Sentence = SentenceGroup[ DefaultLanguage ];

            else:

                g_DiscordLogger.error( self.get( "sentence_no_label", DefaultLanguage, name ), name=self.GetName );

                return SentenceGroup.get( "english", "" );

        try:
            Sentence = Sentence.format( *args );
        except Exception as e:
            from src.Bot import bot;
            bot.HandleException( e, SendToDevs=True );

        return Sentence;

global g_Sentences;
g_Sentences: Sentences = Sentences();
