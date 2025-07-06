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
