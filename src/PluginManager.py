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

from datetime import datetime;
from discord import Member, GroupChannel, TextChannel, DMChannel, User, Message, Reaction, Attachment;
from src.constants import ReactionState, ServerBoostState;

class Plugin():

    '''
        Plugin base. every plugin must inherit from this class

        Every method should return a boolean, True for keep executing plugins in the list. False if the plugin manager should stop calling subsequent plugins.
    '''

    guilds: list[int] = [];
    '''Guilds list to only listen events (if empty == all)'''

    def __init__( self ):
        ''''''

    @property
    def GetFilename( self ) -> str:
        return __name__;

    @property
    def GetDescription( self ) -> str:
        return "";

    @property
    def GetAuthorName( self ) -> str:
        return "Mikk155";

    @property
    def GetName( self ) -> str:
        return self.GetFilename;

    @property
    def GetAuthorSite( self ) -> str:
        return "https://github.com/Mikk155/discord-bot";

    async def OnInitialize( self ) -> bool:
        '''The python scripts has just been run. This is called before the bot is running and just after every plugin has been loaded'''
        return True;

    async def OnPluginActivate( self ) -> bool:
        '''The has been enabled'''
        return True;

    async def OnPluginDeactivate( self ) -> bool:
        '''The has been disabled'''
        return True;

    async def OnBotStart( self ) -> bool:
        '''Called once. when the bot first starts.'''
        return True;

    async def OnReconnect( self ) -> bool:
        '''Called when the bot is back online after a connection lost'''
        return True;

    async def OnThink( self, time: datetime ) -> bool:
        '''Called every second. time is the current time when the plugin manager is just called. use this as a prediction.'''
        return True;

    async def OnMemberLeave( self, user: Member ) -> bool:
        '''Called when a user leaves a guild'''
        return True;

    async def OnMemberJoin( self, user: Member ) -> bool:
        '''Called when a user joins a guild'''
        return True;

    async def OnTyping( self, channel: TextChannel | GroupChannel | DMChannel, user: Member | User, when: datetime ) -> bool:
        '''Called when a user starts typing'''
        return True;

    async def OnMessage( self, message: Message ) -> bool:
        '''Called when a user sends a message'''
        return True;

    async def OnMention( self, message: Message, mentions: tuple[ User | Member ] ) -> bool:
        '''Called when a user sends a message containing mentions'''
        return True;

    async def OnReply( self, message: Message, replied: Message ) -> bool:
        '''Called when a user sends a message replying to a message'''
        return True;

    async def OnLink( self, message: Message, urls: tuple[str] ) -> bool:
        '''Called when a user sends a message containing urls'''
        return True;

    async def OnMessageReference( self, message: Message, guild_id: int, channel_id: int, message_id: int ) -> bool:
        '''Called when a user sends a message containing a url to a discord message'''
        return True;

    async def OnAttachment( self, message: Message, attachments: list[Attachment] ) -> bool:
        '''Called when a user sends a message containing attachments'''
        return True;

    async def OnMessageGIF( self, message: Message ) -> bool:
        '''Called when a user sends a message containing a GIF'''
        return True;

    async def OnMessagePinned( self, message: Message, pinned: Message ) -> bool:
        '''Called when a message is pinned'''
        return True;

    async def OnServerBoost( self, message: Message, boost: ServerBoostState ) -> bool:
        '''Called when a the server is boosted'''
        return True;

    async def OnMessageDelete( self, message: Message, deleter: User | Member ) -> bool:
        '''Called when a message is deleted'''
        return True;

    async def OnMessageEdited( self, before: Message, after: Message ) -> bool:
        '''Called when a message is edited'''
        return True;

    async def OnReaction( self, reaction: Reaction, state: ReactionState, user: User | Member ) -> bool:
        '''Called when a message's reaction has changed'''
        return True;

    async def OnCommand( self, message: Message, command: str, args: list ) -> bool:
        '''Called when a message contains a command prefix'''
        return True;

class PluginManager():

    @property
    def GetName( self ) -> str:
        return "Plugin Manager";

    Plugins: list[Plugin] = [];

    def __init__( self ):

        from sys import executable;
        from os.path import exists;
        from utils.Path import Path;
        from utils.jsonc import jsonc;
        from pathlib import Path as PathLib;
        from subprocess import check_call;
        from src.BotLoggin import g_BotLogger;
        from src.ConfigContext import g_ConfigContext;
        from importlib.util import spec_from_file_location, module_from_spec;

        PluginsContext: list[dict] = jsonc( Path.enter( "config", "plugins.json" ) );
    
        PluginsContext.pop( "$schema", "" );

        for PluginName, PluginData in PluginsContext.items():

            g_BotLogger.info( "Registering plugin \"<c>{}<>\"", PluginName, name=self.GetName );

            if not g_ConfigContext.bot.IsDeveloper and "requirements" in PluginData:

                requirements = PluginData[ "requirements" ];

                if requirements and requirements != '':

                    requirements_path = Path.enter( "plugins", f'{requirements}.txt' );

                    if exists( requirements_path ):

                        check_call( [ executable, "-m", "pip", "install", "-r", requirements_path ] );

                    else:

                        g_BotLogger.warn( "Invalid requirement file \"<c>{}<>\" for plugin <g>{}<>.", PluginName, name=self.GetName );
                        continue;

            script_path = PathLib( Path.enter( "plugins", f'{PluginName}.py' ) );

            module_name = script_path.stem;

            spec = spec_from_file_location( module_name, script_path );

            module = module_from_spec( spec );

            spec.loader.exec_module( module );

            if not hasattr( module, module_name ):

                g_BotLogger.error( "Couldn't find object \"<c>{}<>\" in module \"<g>{}<>\" in the script \"<g>{}<>\"", \
                    module_name, module_name, script_path, name=self.GetName );

                continue;

            plugin: Plugin = getattr( module, module_name )();

            plugin.guilds = PluginData.get( "guilds", [] );

            plugin.filename = PluginName;

            plugin.disabled = PluginData.get( "disabled", False );

            if plugin.disabled is True:

                g_BotLogger.debug( "Plugin \"<c>{}<>\" disabled by config.", PluginName, name=self.GetName );

            else:

                plugin.OnPluginActivate();

            self.Plugins.append( plugin );

    async def CallFunction( self, fnName: str, *args, GuildID = None ) -> None:

        for p in self.Plugins:

            if p.disabled is True:
                continue;

            if len( p.guilds ) > 0 and GuildID is not None and not GuildID in p.guilds:
                continue; # This plugin doesn't want to work on this guild.

            try:

                fn = getattr( p, fnName );

                if len(args) > 0:

                    if await fn(*args) is False:

                        break;

                elif await fn() is False:

                    break;

            except Exception as e:

                from src.Bot import bot;
                bot.HandleException( e, "PluginManager::CallFunction", SendToDevs=True );

global g_PluginManager;
g_PluginManager: PluginManager = PluginManager();
