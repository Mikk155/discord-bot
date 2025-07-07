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

from project import *;

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

            embed = g_DiscordLogger.info( g_Sentences.get( "no_plugins_running", Guild=interaction.guild_id ), flags=LoggerFlags.Nothing );

            await interaction.response.send_message( embed=embed );

            return;

        plugins = g_PluginManager.Plugins.copy();

        view = PluginPaginator( plugins );

        embed = view.GetNextPage();

        await interaction.response.send_message( embed=embed, view=view );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embed=bot.HandleException(e) );

        else:

            await interaction.response.send_message( embed=bot.HandleException(e) );
