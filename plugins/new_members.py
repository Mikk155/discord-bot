from project import *

#-TODO Add commands and allow this as a global plugin
class new_members( Plugin ):

    @property
    def GetDescription(self):
        return "Display information when a user joins/leaves a server";

    __GuildInvites__: dict[ str, int ] = {};

    async def OnBotStart( self ) -> Hook:
    #
        GuildInvites: list[discord.Invite] = await bot.get_guild( 744769532513615922 ).invites();

        for Invite in GuildInvites:
        #
            self.__GuildInvites__[ Invite.code ] = Invite.uses;
        #
        return Hook.Destroy; # Does this actually free some memory?
    #

    async def OnMemberJoin( self, user: discord.Member ) -> Hook:
    #
        embed = discord.Embed(
            color=RGB(200,0,200).hex,
            title=user.name,
            description = "{} joined the server".format( fmt.DiscordUserMention( user ) )
        ); # Maybe random messages from cache?

        embed.add_field(
            inline = False,
            name = "Account creation",
            value = f'{user.created_at.day}/{user.created_at.month}/{user.created_at.year}'
        );

        GuildInvites: list[discord.Invite] = await user.guild.invites();

        InviteUsed: list[discord.Invite] = [ I for I in GuildInvites if I.code in self.__GuildInvites__ and I.uses > self.__GuildInvites__[ I.code ] ];

        if len( InviteUsed ) > 0:

            InviteUsed: discord.Invite = InviteUsed[0];

            self.__GuildInvites__[ InviteUsed.code ] += 1;

            match InviteUsed.code:
            #
                case '2ErNUQh6fE': # *
                #
                    embed.add_field( inline = False, name = "Joined by", value = "Static unlimited invite" );
                #
                case '9RCY6DsYjY': # 100
                #
                    embed.add_field( inline = False, name = "Joined by", value = f"Game server {InviteUsed.uses}/100" );
                #
                case 'ksY4XmBDfC': # 50
                #
                    embed.add_field( inline = False, name = "Joined by", value = f"Mikk's Steam profile {InviteUsed.uses}/50" );
                #
                case 'Wm8WqCSCUX': # 25
                #
                    embed.add_field( inline = False, name = "Joined by", value = f"Mikk's Github profile {InviteUsed.uses}/25" );
                #
                case 'HHMZj3MSWT': # 10
                #
                    embed.add_field( inline = False, name = "Joined by", value = f"Mikk's Discord profile {InviteUsed.uses}/10" );
                #
                case _:
                #
                    if InviteUsed.inviter:
                    #
                        embed.add_field( inline = False, name = "Invited by", value = fmt.DiscordUserMention( InviteUsed.inviter ) );
                        embed.set_footer( text=InviteUsed.inviter.name, icon_url=InviteUsed.inviter.avatar.url if InviteUsed.inviter.avatar else None );
                    #
                #
            #

        embed.set_author( name=user.name, icon_url=user.avatar.url if user.avatar else None, url=user.avatar.url if user.avatar else None );

        await bot.get_channel( 1343203830787080203 ).send( embed=embed, allowed_mentions=False );

        return Hook.Continue;
    #

    async def OnMemberLeave( self, user: discord.Member ) -> Hook:

        embed = discord.Embed(
            color=RGB(200,0,200).hex,
            title=user.name,
            description = "{} Left the server".format( fmt.DiscordUserMention( user ) )
        ); # Maybe random messages from cache?

        embed.set_author( name=user.name, icon_url=user.avatar.url if user.avatar else None, url=user.avatar.url if user.avatar else None );

        await bot.get_channel( 1343203830787080203 ).send( embed=embed, allowed_mentions=False );
