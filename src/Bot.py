import discord
from discord import app_commands

class Bot( discord.Client ):

    from src.BotLoggin import BotLoggin;
    m_Loggin = BotLoggin();

    __on_start_called__: bool = False

    def __init__( self ):

        super().__init__( intents = discord.Intents.all() )

        self.tree = app_commands.CommandTree( self )

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
