from src.main import *
from src.PluginManager import Plugin;

class role_menu( Plugin ):

    MaxMenus = 5;

    TimeoutConfiguration: float = 500;

    ConfiguringMessages: list[ tuple[ int, int, int, datetime ] ] = [];
    '''Contains message ID, channel ID and guild ID of a message that is currently being configured'''

    def OnPluginActivate(self):

        command = app_commands.Command(
            name="cfg_role_menu",
            description="Create a menu on wich users can choose roles",
            callback=self.command_cfg_role_menu,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

        g_Sentences.push_back( "role_menu" );

    def OnPluginDeactivate(self):

        bot.tree.remove_command( "cfg_role_menu" );

    @property
    def GetName(self):
        return "Role menu";

    @property
    def GetDescription(self):
        return "Create a menu on wich users can choose roles";

    async def OnThink( self, time ):

        now = datetime.now() - timedelta( seconds=self.TimeoutConfiguration ) ;

        cache = g_Cache.Get();

        for C in self.ConfiguringMessages:

            if C[3] is None or now > C[3]:

                cacheGuild: dict = cache.get( str( C[2] ), {} );

                cacheMessage: dict = cacheGuild.get( str( C[0] ), {} );

                if not "roles" in cacheMessage or len( cacheMessage[ "roles" ] ) == 0:

                    cacheGuild.pop( str( C[0] ), {} );
                    cache[  str( C[2] ) ] = cacheGuild;

                    try:
                        msg = await bot.get_channel( C[1] ).fetch_message( C[0] );
                        await msg.delete();
                    except: pass;

    class CRoleSelectionView( discord.ui.View ):

        def __init__( self, roles: dict[ str, str ], title: str ):

            super().__init__( timeout=None );

            Options: list[ discord.SelectOption ] = [];

            for role, info in roles.items():

                Options.append( discord.SelectOption( label = info[0], value = role, description = info[1] ) );

            Selection = discord.ui.Select( placeholder=title, options=Options );

            Selection.callback = self.SelectRole;

            self.add_item( Selection );

        async def SelectRole( self, interaction: discord.Interaction ):

            try:

                role = interaction.guild.get_role( int( interaction.data[ "values" ][0] ) )

                if role in interaction.user.roles:

                    await interaction.user.remove_roles( role );

                    await interaction.response.send_message(
                        g_Sentences.get( "role_menu_removed_role", role.mention, Guild=interaction.guild_id ),
                        ephemeral=True,
                        allowed_mentions=False
                    );

                else:

                    await interaction.user.add_roles( role );

                    await interaction.response.send_message(
                        g_Sentences.get( "role_menu_added_role",
                            role.mention,
                            Guild=interaction.guild_id
                        ),
                        ephemeral=True,
                        allowed_mentions=False
                    );

            except Exception as e:

                from src.Bot import bot;

                if interaction.response.is_done():

                    await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );

                else:

                    await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );

    async def UpdateMenu( self, _c: dict, _m: discord.Message ):

        Roles: dict[ str, str ] = _c.get( "roles", {} );

        view = self.CRoleSelectionView( Roles, _c.get( "button", "Select a role" ) ) if len( Roles ) > 0 else None;

        embed = discord.Embed(
            color=RGB(0,100,0).hex,
            title=_c.get( "name", "" ),
            description=_c.get( "description", "" )
        ) if "name" in _c else None;

        await _m.edit( content='', embed=embed, view=view );

    async def TrackMessages( self, Guild: discord.Guild, target: Optional[ Union[ int, discord.Message ] ] = 0 ):

        cache = g_Cache.Get();

        GuildCache: dict = cache.get( str( Guild.id if isinstance( Guild, discord.Guild ) else Guild ), {} );

        if target == 0:

            for k, v in GuildCache.items():

                if not "roles" in v or len( v[ "roles" ] ) == 0:
                    self.ConfiguringMessages.append( ( int(k), v[ "channel" ], int(GuildCache), None ) );
                    continue;

                try:
                    channel = bot.get_channel( v[ "channel" ] );

                    message = await channel.fetch_message( int(k) );

                    await self.UpdateMenu( v, message );
                except: pass;

        elif isinstance( target, discord.Message ):

            await self.UpdateMenu( GuildCache[ str( target.id ) ], target );

        else:

            k = GuildCache[ str( target ) ];

            channel = bot.get_channel( k[ "channel" ] );

            message = await channel.fetch_message( str( target ) );

            await self.UpdateMenu( k, message );

    async def OnBotStart(self):
        for Guild in bot.guilds:
            await self.TrackMessages(Guild);
        return True;

    async def OnReconnect(self):
        for Guild in bot.guilds:
            await self.TrackMessages(Guild);
        return True;

    class ConfigModal( discord.ui.Modal, title="" ):

        def __init__( self, interaction: discord.Interaction, menu: discord.Message, owner: Plugin ):

            super().__init__( timeout=owner.TimeoutConfiguration );

            self.interaction = interaction;
            self.menu = menu;
            self.owner: role_menu = owner;

            self.ItemName = discord.ui.TextInput(
                label=g_Sentences.get( "name", Guild=interaction.guild_id ),
                placeholder=g_Sentences.get( "role_menu_embed_title", Guild=interaction.guild_id ),
                max_length=100
            );

            self.add_item( self.ItemName );

            self.ItemDescription = discord.ui.TextInput(
                label=g_Sentences.get( "description", Guild=interaction.guild_id ),
                placeholder=g_Sentences.get( "role_menu_embed_description", Guild=interaction.guild_id ),
                max_length=100
            );

            self.add_item( self.ItemDescription );

            self.ItemButton = discord.ui.TextInput(
                label=g_Sentences.get( "role_menu_selection_title", Guild=interaction.guild_id ),
                placeholder=g_Sentences.get( "role_menu_selection_description", Guild=interaction.guild_id ),
                max_length=100
            );

            self.add_item( self.ItemButton );

            self.owner.ConfiguringMessages.append( ( self.menu.id, self.menu.channel, self.interaction.guild_id, datetime.now() ) );

        async def on_submit( self, interaction: discord.Interaction ):

            cache = g_Cache.Get(); #-TODO i should reaaaally see into cache managment class. this get/set is annoying.
            cacheGuild = cache.get( str( self.interaction.guild_id ), {} );
            cacheMessage = cacheGuild.get( str( self.menu.id ), {} );
            cacheMessage[ "name" ] = self.ItemName.value;
            cacheMessage[ "description" ] = self.ItemDescription.value;
            cacheMessage[ "button" ] = self.ItemButton.value;
            cacheMessage[ "channel" ] = self.interaction.channel_id;
            cacheGuild[ str( self.menu.id ) ] = cacheMessage;
            cache[ str( self.interaction.guild_id ) ] = cacheGuild;

            await self.owner.UpdateMenu( cacheMessage, self.menu );

            await interaction.response.send_message(
                    g_Sentences.get( "role_menu_starting",
                    self.owner.TimeoutConfiguration,
                    self.menu.id,
                    Guild=interaction.guild_id
                ),
                silent=True,
                allowed_mentions=False,
                delete_after=self.owner.TimeoutConfiguration
            );

    @app_commands.guild_only()
    @app_commands.default_permissions( administrator=True )
    @app_commands.describe(
        menu='Message ID to alter or to delete if not role provided',
        role='Role to add to the current configuring message.',
        description='Description for the role'
    )
    async def command_cfg_role_menu(
        self,
        interaction: discord.Interaction,
        role: Optional[ discord.Role ] = None,
        description: Optional[ str ] = None,
        menu: Optional[ str ] = None
    ):

        '''Create a role menu. run with no arguments to start configuring'''

        try:

            UserRoleMenu: discord.Message = None;

            if menu is not None:

                try:

                    UserRoleMenu: discord.Message = await interaction.channel.fetch_message( int(menu) );

                except:

                    await interaction.response.send_message(
                        g_Sentences.get( "role_menu_failed_find",
                            menu,
                            interaction.channel.jump_url,
                            Guild=interaction.guild_id
                        ),
                        silent=True,
                        allowed_mentions=False
                    );

                    pass;

                if role is None:

                    cache = g_Cache.Get();
                    cacheGuild = cache.get( str( interaction.guild_id ), {} );

                    if str( UserRoleMenu.id ) in cacheGuild:

                        cacheGuild.pop( str( UserRoleMenu.id ), {} );
                        cache[ str( interaction.guild_id ) ] = cacheGuild;

                        await UserRoleMenu.delete();

                        await interaction.response.send_message(
                            g_Sentences.get( "message_deleted", Guild=interaction.guild_id ),
                            silent=True,
                            allowed_mentions=False
                        );

                    else:

                        await interaction.response.send_message(
                            g_Sentences.get( "role_menu_no_cache",
                                UserRoleMenu.id,
                                Guild=interaction.guild_id
                            ),
                            silent=True,
                            allowed_mentions=False
                        );

                else:

                    cache = g_Cache.Get();
                    cacheGuild = cache.get( str( interaction.guild_id ), {} );
                    cacheMessage = cacheGuild.get( menu, {} );
                    cacheRoles = cacheMessage.get( "roles", {} );

                    if str( role.id ) in cacheRoles:

                        cacheRoles.pop( str( role.id ), None );
                        await interaction.response.send_message(
                            g_Sentences.get( "role_menu_removed_role",
                                role.mention,
                                Guild=interaction.guild_id
                            ),
                            silent=True,
                            allowed_mentions=False
                        );

                    elif not role.is_assignable():

                        await interaction.response.send_message(
                            g_Sentences.get( "role_menu_bad_hierarchy",
                                role.mention,
                                Guild=interaction.guild_id
                            ),
                            silent=True,
                            allowed_mentions=False
                        );
                        return;

                    else:

                        cacheRoles[ str( role.id ) ] = [ role.name, description ];

                        await interaction.response.send_message(
                            g_Sentences.get( "role_menu_added_role", role.mention, Guild=interaction.guild_id ),
                            silent=True,
                            allowed_mentions=False
                        );

                    cacheMessage[ "roles" ] = cacheRoles;
                    cacheGuild[ str( UserRoleMenu.id ) ] = cacheMessage;
                    cache[ str( interaction.guild_id ) ] = cacheGuild;

                    await self.UpdateMenu( cacheMessage, UserRoleMenu );

            else:

                cache = g_Cache.Get();
                cacheGuild = cache.get( str( interaction.guild_id ), {} );

                if len(cacheGuild) > 0:

                    embeds: list[ discord.Embed ] = [];

                    from src.Bot import bot;

                    for channel_ID, roleinfo in cacheGuild.items():

                        validation = None;

                        try:
                            validation = await bot.get_channel( roleinfo[ "channel" ] ).fetch_message( channel_ID );
                        except: pass;

                        embeds.append(
                            discord.Embed(
                                color=RGB(0,100,0).hex,
                                title=channel_ID,
                                description=validation.jump_url if validation is not None else "null"
                            )
                        );

                    await interaction.response.send_message(
                        g_Sentences.get( "role_menu_menus_limit", self.MaxMenus, Guild=interaction.guild_id ),
                        embeds=embeds,
                        silent=True,
                        allowed_mentions=False
                    );

                    return;

                UserRoleMenu = await interaction.channel.send( "✅" );

                await interaction.response.send_modal( self.ConfigModal( interaction, UserRoleMenu, self ) );

        except Exception as e:

            from src.Bot import bot;

            if interaction.response.is_done():

                await interaction.followup.send( embeds=bot.HandleException( e, SendToDevs=True ) );

            else:

                await interaction.response.send_message( embeds=bot.HandleException( e, SendToDevs=True ) );
