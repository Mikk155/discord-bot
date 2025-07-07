from project import *;

@bot.tree.command()
async def plugin_info( interaction: discord.Interaction, plugin: str ):

    """Get a information for a given plugin"""

    try:

        plugins: list[Plugin] = [ a for a in g_PluginManager.Plugins if plugin == a.GetFilename ];

        if len( plugins ) == 0:

            embed = g_DiscordLogger.error( g_Sentences.get( "plugin_not_found", plugin, Guild=interaction.guild_id ), flags=LoggerFlags.Nothing );

            await interaction.response.send_message( embed=embed );

            return;

        plgn = plugins[0];

        embed = discord.Embed( color = HexColor.CYAN, title = plgn.GetFilename, description = plgn.GetName );

        
        embed.add_field( name = g_Sentences.get( "description", Guild=interaction.guild_id ), value = plgn.GetDescription, inline = False );
        embed.add_field( name = g_Sentences.get( "author", Guild=interaction.guild_id ), value = plgn.GetAuthorName, inline = False );
        embed.add_field( name = g_Sentences.get( "author_site", Guild=interaction.guild_id ), value = plgn.GetAuthorSite, inline = False );
        embed.add_field( name = g_Sentences.get( "state", Guild=interaction.guild_id ),
            value = "❌" + g_Sentences.get( "disabled", Guild=interaction.guild_id ) if plgn.disabled
                else "✅" + g_Sentences.get( "enabled", Guild=interaction.guild_id ), inline = False );

        await interaction.response.send_message( embed=embed );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embed=bot.HandleException(e) );

        else:

            await interaction.response.send_message( embed=bot.HandleException(e) );
