from plugins.main import *

command = Commands()
command.information = 'Checks for a upstream commit in github and if found, restarts the bot'
command.command = '**update**'
command.function = 'on_command'
command.allowed = [ config[ "mikkserver" ][ "MODERATOR_ROLE" ] ]

RegisterCommand( plugin_name='cmd_bot_updater', command_name='update', command_class=command );

from git import Repo

async def on_command( message: discord.Message ):

    repo = Repo( abs );

    origin = repo.remotes.origin;
    origin.fetch();

    commits_behind = repo.iter_commits( 'HEAD..origin/main' );

    changes = sum( 1 for _ in commits_behind );

    if changes > 0:

        await message.reply( 'There are some commits ahead. i\'m going to rest a moment while downloading... {}'.format( changes ) )

        origin.pull()

        bot_path = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'bot.py' )

        os.execv( sys.executable, [ sys.executable, bot_path ] )

    else:
        await message.reply( 'There aren\'t any commit ahead to update.' )