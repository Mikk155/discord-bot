from plugins.main import *

command = Commands()
command.information = '''
Checks if the upstream repository has any commit ahead, if so then fetch changes pull and restart the bot

- update

Forces the bot to restart even if it is up-to-date
- update ``force``
'''
command.function = 'on_command'
command.allowed = [ config[ "mikkserver" ][ "MODERATOR_ROLE" ], config[ "testserver" ][ "MODERATOR_ROLE" ] ]

RegisterCommand( plugin_name='cmd_bot_updater', command_name='update', command_class=command );

async def on_command( message: discord.Message, arguments: dict ):

    repo = Repo( abspath );

    origin = repo.remotes.origin;
    origin.fetch();

    commits_behind = repo.iter_commits( 'HEAD..origin/main' );

    changes = sum( 1 for _ in commits_behind );

    restart = False;

    if arguments.get( '0', '' ) == "force":

        restart = True;

    if changes > 0:

        await message.reply( 'The local repository is out of date. Pulling changes... {}'.format( changes ) );

        origin.pull();

        restart = True;

    elif not restart:

        await message.reply( 'The upstream repository is up to date.' );

    if restart:

        await message.reply( 'Restarting..' );

        bot_path = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'bot.py' );

        os.execv( sys.executable, [ sys.executable, bot_path, "True" if gpGlobals.developer else '' ] );
