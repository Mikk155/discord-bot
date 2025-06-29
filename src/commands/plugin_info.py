from src.main import *
from src.PluginManager import Plugin;

@bot.tree.command()
async def plugin_info( interaction: discord.Interaction, plugin: str ):

    """Get a information for a given plugin"""

    try:

        plugins: list[Plugin] = [ a for a in g_PluginManager.Plugins if plugin == a.GetFilename ];

        if len( plugins ) == 0:

            await interaction.response.send_message( f"Plugin \"{plugin}\" not found" );

            return;

        plgn = plugins[0];

        embed = discord.Embed( color = HexColor.CYAN, title = plgn.GetFilename, description = plgn.GetName );

        embed.add_field( name = "Description", value = plgn.GetDescription, inline = False );
        embed.add_field( name = "Author", value = plgn.GetAuthorName, inline = False );
        embed.add_field( name = "Author site", value = plgn.GetAuthorSite, inline = False );

        await interaction.response.send_message( embed=embed );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embeds=bot.HandleException( e, "command::plugin_info" ) );

        else:

            await interaction.response.send_message( embeds=bot.HandleException( e, "command::plugin_info" ) );
