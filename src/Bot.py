import discord
from discord import app_commands

class Bot( discord.Client ):

    from src.BotLoggin import BotLoggin;
    m_Loggin = BotLoggin();

    __on_start_called__: bool = False

    def __init__( self ):

        super().__init__( intents = discord.Intents.all() );

        self.tree = app_commands.CommandTree( self );

    async def setup_hook( self ):

        from src.ConfigContext import g_ConfigContext;

        if g_ConfigContext.developer:

            TargetGuild = discord.Object( id = g_ConfigContext.developer_guild );

            if TargetGuild:

                self.tree.clear_commands( guild=TargetGuild );

                self.tree.copy_global_to( guild=TargetGuild );

                await self.tree.sync( guild=TargetGuild );

                return;

        await self.tree.sync();

    async def FindMemberByName( self, name: str, guild: discord.Guild | int ) -> None | discord.Member:

        if isinstance( guild, int ):

            guild = discord.Object( id = guild );

        for member in guild.members:

            if name in ( member.name, member.display_name, member.global_name ):
                return member;

            # Partial? This maybe is a bad idea
            if name in member.name or name in member.display_name or name in member.global_name:
                return member;

        return None;

global bot;
bot: Bot = Bot();
