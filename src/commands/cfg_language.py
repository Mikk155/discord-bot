from src.main import *

@bot.tree.command()
@app_commands.describe( language='Language' )
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
@app_commands.choices( language = fmt.DiscordCommandsChoices( g_Sentences[ "languages" ] ) )
async def cfg_language( interaction: discord.Interaction, language: app_commands.Choice[str] ):

    """Set the language the bot should use in this server"""

    try:

        cache = g_Cache.get( "language" );

        cache[ str( interaction.guild_id ) ] = language.name;

        await interaction.response.send_message( f"Updated language to {language.name}" );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embeds=bot.HandleException( e, "command::cfg_language" ) );

        else:

            await interaction.response.send_message( embeds=bot.HandleException( e, "command::cfg_language" ) );
