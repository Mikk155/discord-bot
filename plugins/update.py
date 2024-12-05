"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from src.main import *

from git import Repo
"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from src.main import *

def on_initialization() -> dict:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.
    '''

    # Create data for g_PluginManager
    __data__: dict = {};
    __data__["name"] = "Update the bot";
    __data__["description"] = "Updates the bot (re-run) and Fetch&Pull lastest changes from the github upstream repository";

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe( git='Fetch and pull lastest github\'s commits in the upstream repositor' )
async def dev_update( interaction: discord.Interaction, git: bool = False ):
    """Update the bot"""

    await interaction.response.defer( thinking=True );

    try:

        if interaction.user.id != g_Config.configuration[ "owner_id" ]:

            await interaction.followup.send(
                g_Format.brackets(
                    g_Sentences.get(
                        "only.owner",
                        interaction.guild_id
                    ) ) [
                    g_Config.configuration[ "owner_id" ]
                ]
            );

            return;

        if git:

            repo = Repo( os.path.abspath( "" ) );

            origin = repo.remotes.origin;

            origin.fetch();

            commits_behind = repo.iter_commits( 'HEAD..origin/main' );

            changes = sum( 1 for _ in commits_behind );

            if changes > 0:

                await interaction.followup.send(
                    g_Format.brackets(
                        g_Sentences.get(
                            "update.pull.commits",
                            interaction.guild_id 
                        ), [ changes ]
                    )
                );

                origin.pull();

            else:

                await interaction.followup.send( g_Sentences.get( "update.no.outdated", interaction.guild_id  ) );

        await interaction.followup.send( g_Sentences.get( "update.restarting", interaction.guild_id  ) );

        bot_path = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'bot.py' );

        await bot.close();

        # -TODO Pass on all the arguments
        os.execv( sys.executable, [ sys.executable, bot_path, '-dev' if DEVELOPER() else '' ] );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

