from src.main import *

@bot.tree.command()
@app_commands.describe( language='Language' )
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
@app_commands.choices( language = fmt.DiscordCommandsChoices( g_Sentences[ "languages" ] ) )
async def cfg_language( interaction: discord.Interaction, language: app_commands.Choice[str] ):

    """Set the language the bot should use in this server"""

    try:

        cache = g_Cache.Get( "language" );

        cache[ str( interaction.guild_id ) ] = language.name;

        embed = g_DiscordLogger.info( g_Sentences.get( "language_updated_to", language.name, Guild=interaction.guild_id ), flags=LoggerFlags.Nothing );

        await interaction.response.send_message( embed=embed );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embeds=bot.HandleException(e) );

        else:

            await interaction.response.send_message( embeds=bot.HandleException(e) );
