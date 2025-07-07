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

@bot.tree.command( guild=bot.get_guild( g_ConfigContext.bot.TargetGuildCommands ) )
@app_commands.describe( json='json object containing the cache to upload.', obj='Label object to target if None is the whole cache' )
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
async def dev_cache( interaction: discord.Interaction, json: Optional[ discord.Attachment ] = None, obj: Optional[ str ] = None ):

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

                if obj is None:

                    g_Cache.__cache__ = session[0];

                else:

                    g_Cache.Set( obj, session[0] );

        else:

            if obj is None:

                with open( g_Cache.GetCacheDir, "rb") as file:

                    await interaction.followup.send( "cache", file=discord.File( file, "data.json" ) );

            else:

                cache = g_Cache.Get( obj );

                await interaction.followup.send( "cache", file=discord.File( cache, "data.json" ) );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embed=bot.HandleException(e) );

        else:

            await interaction.response.send_message( embed=bot.HandleException(e) );
