from src.main import *

@bot.tree.command( guild=bot.get_guild( g_ConfigContext.bot.TargetGuildCommands ) )
@app_commands.describe( json='json object containing the cache to upload.' )
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
async def dev_cache( interaction: discord.Interaction, json: Optional[ discord.Attachment ] = None ):

    """Get or update the bot cache"""

    await interaction.response.defer( thinking=True );

    try:

        if json is not None:

            if not g_ConfigContext.IsOwner( interaction.user.id ):

                await interaction.followup.send( g_Sentences.get( "bot_owner_only", Guild=interaction.guild_id ) )

            else:

                from src.Bot import bot;
                session = await bot.FileToJson( json, interaction.guild_id );

                await interaction.followup.send( embed=session[1] )

                if session[0] is None:
                    return;
    
                g_Cache.__cache__ = session[0];

        else:
                
            with open( g_Cache.GetCacheDir, "rb") as file:

                await interaction.followup.send( "cache", file=discord.File( file, "data.json" ) );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embeds=bot.HandleException(e) );

        else:

            await interaction.response.send_message( embeds=bot.HandleException(e) );
