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
from discord import Member, GroupChannel, TextChannel, DMChannel, User, Message, Reaction, Attachment, audit_logs;
from src.constants import ReactionState, ServerBoostState, EmojiFlags;

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
        return self.filename;

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

    def OnPluginActivate( self ) -> bool:
        '''The has been enabled'''
        return True;

    def OnPluginDeactivate( self ) -> bool:
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

    async def OnAuditLog( self, entry: audit_logs.AuditLogEntry  ) -> bool:
        '''Called when a new entry to the audit log is made'''
        return True;

    async def OnEmoji( self, message: Message, emojis: list[ tuple[str, EmojiFlags] ] ):
        '''Called when a message contains emojis'''
        return True;
