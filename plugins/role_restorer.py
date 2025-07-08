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

from project import *

class role_restorer( Plugin ):

    @property
    def GetName(self):
        return "Role restorer";

    @property
    def GetDescription(self):
        return "Keep track of user roles when they leave a server to add them back when the user rejoin";

    async def OnMemberLeave( self, user: discord.Member ) -> Hook:
    #
        if user.guild:
        #
            g_Cache.Plugin[ user.guild.id ][ user.id ] = [ Role.id for Role in user.roles if Role ];
        #
        return Hook.Continue;
    #

    async def OnMemberJoin( self, user: discord.Member ) -> Hook:
    #
        if user.guild:
        #
            GuildCache: Dictionary = g_Cache.Plugin[ user.guild.id ]
            UserCache: Dictionary = GuildCache[ user.id ];

            Roles: list[discord.Role] = [];

            if not UserCache.IsEmpty:
            #
                RolesID: list[int] = UserCache.pop( user.id );
                Roles = [ Role for Role in user.guild.roles if Role.id in RolesID ];
            #
            elif user.guild.id == 744769532513615922:
            #
                Roles.append( user.guild.get_role( 1316214066384994324 ) );
            #

            for Role in Roles:
            #
                try: # One by one iteration due in case of one failing mid-way
                #
                    await user.add_roles( Role );
                #
                except: pass;
            #
        #
        return Hook.Continue;
    #
