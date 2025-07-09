from project import *

class role_menu( Plugin ):

    def OnPluginActivate(self) -> None:
    #
        command = app_commands.Command(
            name="roles",
            description="Create a menu on wich users can choose roles",
            callback=self.command_roles,
        );

        command.guild_only = True;

        bot.tree.add_command( command );

        g_Sentences.push_back( "role_menu" );
    #

    def OnPluginDeactivate(self) -> None:
    #
        bot.tree.remove_command( "roles" );
    #

    @property
    def GetName(self):
    #
        return "Role menu";
    #

    @property
    def GetDescription(self):
    #
        return "Create a menu on wich users can choose roles";
    #

    class CRoleSelectionView( discord.ui.View ):
    #
        def __init__( self, Buttons: Dictionary, fnCallback, ExpireTime = None ):
        #
            if ExpireTime is None:
                ExpireTime = Buttons[ "life" ];

            super().__init__( timeout=ExpireTime );

            for name, button in Buttons.items():
            #
                if isinstance( button, Dictionary ):
                    button: dict = button.ToDict;

                if not isinstance( button, dict ):
                    continue;

                Roles: dict[str, str] = button[ "roles" ];

                Options: list[ discord.SelectOption ] = [ discord.SelectOption( label = info, value = role ) for role, info in Roles.items() ];

                Selection = discord.ui.Select( placeholder=button[ "title" ], options=Options );

                Selection.callback = fnCallback;

                self.add_item( Selection );
            #
        #

    @Plugin.HandleExceptions()
    async def SelectRole( self, interaction: discord.Interaction ) -> None:
    #
        role: discord.Role = interaction.guild.get_role( int( interaction.data[ "values" ][0] ) )

        if role in interaction.user.roles:
        #
            await interaction.user.remove_roles( role );

            await interaction.response.send_message(
                g_Sentences.get(
                    "role_menu_removed_role",
                    role.mention,
                    interaction.user.mention,
                    Guild=interaction.guild_id
                ),
                allowed_mentions=False,
                delete_after=5,
                silent=True
            );
        #
        else:
        #
            await interaction.user.add_roles( role );

            await interaction.response.send_message(
                g_Sentences.get( "role_menu_added_role",
                    role.mention,
                    interaction.user.mention,
                    Guild=interaction.guild_id
                ),
                allowed_mentions=False,
                delete_after=5,
                silent=True
            );
        #
        # -TODO How to reset this without recreating the view class and updating the message?
    #

    InteractionsOnChannels: dict[ int, datetime ] = {};

    async def OnCommand( self, message: discord.Message, command: str, args: list[str] ) -> Hook:
    #
        if command != 'roles':
            return Hook.Continue;

        if message.author.id == bot.user.id:
            return Hook.Break;

        channel: discord.TextChannel = message.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
            return Hook.Break;

        await self.RoleMenuInteraction( channel );
        return Hook.Break;
    #

    async def RoleMenuInteraction( self, channel: discord.Message ) -> None:
    #
        now: datetime = datetime.now();

        cache: Dictionary = g_Cache.Plugin;

        if channel.id in self.InteractionsOnChannels:
        #
            before: datetime = self.InteractionsOnChannels[ channel.id ];

            Elapsed: timedelta = ( now - before );

            Remaining: int = int( cache[ "life" ] - Elapsed.total_seconds() );

            if Remaining > 0:
            #
                await channel.send(
                    "There's already a menu interaction in this channel. it will timeout in {} seconds".format( Remaining ),
                    allowed_mentions=False,
                    mention_author=False,
                    silent=True
                );
                return;
            #
            else:
            #
                self.InteractionsOnChannels.pop( channel.id );
            #
        #

        view = self.CRoleSelectionView( cache, fnCallback=self.SelectRole );

        self.InteractionsOnChannels[ channel.id ] = datetime.now();
        await channel.send( view=view, allowed_mentions=False, mention_author=False, silent=True, delete_after=cache[ "life" ] );
    #

    @Plugin.HandleExceptions()
    async def command_roles( self, interaction: discord.Interaction ):
        await self.RoleMenuInteraction( interaction.channel );
        await interaction.response.send_message( "✅", ephemeral=True, delete_after=0.5 );
