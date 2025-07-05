from project import *

class role_restorer( Plugin ):

    @property
    def GetName(self):
        return "Role restorer";

    @property
    def GetDescription(self):
        return "Keep track of user roles when they leave a server to add them back when the user rejoin";

    async def OnMemberLeave( self, user ):

        if not user.guild:
            return True;

        GuildID = str( user.guild.id );

        cache = g_Cache.Get();

        GuildCache = cache.get( GuildID, {} );

        Roles = [ Role.id for Role in user.roles if Role ];

        GuildCache[ str( user.id ) ] = Roles;

        cache[ GuildID ] = GuildCache;

        return True;

    async def OnMemberJoin( self, user ):

        if not user.guild:
            return True;

        GuildID = str( user.guild.id );

        cache = g_Cache.Get();

        GuildCache = cache.get( GuildID, {} );

        RolesID = GuildCache.pop( str( user.id ), {} );

        cache[ GuildID ] = GuildCache;

        Roles = [ Role for Role in user.guild.roles if Role.id in RolesID ];

        if len( Roles ) == 0: # No roles? Then is a new member.
            Roles.append( user.guild.get_role( 1316214066384994324 ) );

        for Role in Roles:

            try: # One by one iteration due in case of one failing mid-way

                await user.add_roles( Role );

            except: pass;

        return True;
