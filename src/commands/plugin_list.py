from src.main import *
from src.PluginManager import Plugin;

class PluginPaginator( discord.ui.View ):

    def __init__( self, Plugins: list[Plugin], PerPage: int = 10 ):

        super().__init__( timeout=120 );

        self.Plugins = Plugins;

        self.Page = 0;

        self.PerPage = PerPage;

        self.MaxPages = ( len( Plugins ) + PerPage - 1 ) // PerPage;

        self.message = None;

    def GetNextPage( self ):

        embed = discord.Embed(
            color=HexColor.GREEN,
            title="Installed plugins",
            description=f"Page {self.Page + 1}/{self.MaxPages}"
        );

        start = self.Page * self.PerPage;

        end = min( start + self.PerPage, len( self.Plugins ) );

        for plugin in self.Plugins[ start : end ]:

            embed.add_field( name=plugin.GetFilename, value=plugin.GetName, inline=False );

        return embed;

    @discord.ui.button( label="<", style=discord.ButtonStyle.blurple )
    async def previous( self, interaction: discord.Interaction, button: discord.ui.Button ):

        self.Page = self.Page - 1 if self.Page > 0 else self.MaxPages -1;

        await interaction.response.edit_message( embed = self.GetNextPage(), view=self );

    @discord.ui.button( label=">", style=discord.ButtonStyle.blurple )
    async def next( self, interaction: discord.Interaction, button: discord.ui.Button ):

        self.Page = self.Page + 1 if self.Page < self.MaxPages -1 else 0;

        await interaction.response.edit_message( embed=self.GetNextPage(), view=self );

@bot.tree.command()
async def plugin_list( interaction: discord.Interaction ):

    """Get a list of all installed plugins"""

    try:

        if len( g_PluginManager.Plugins ) == 0:

            await interaction.response.send_message( "There are no plugins running." );

            return;

        plugins = g_PluginManager.Plugins.copy();

        view = PluginPaginator( plugins );

        embed = view.GetNextPage();

        await interaction.response.send_message( embed=embed, view=view );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embeds=bot.HandleException( e, "command::plugin_list" ) );

        else:

            await interaction.response.send_message( embeds=bot.HandleException( e, "command::plugin_list" ) );
