from plugins.main import *

hooks = [
    Hooks.on_message
];

RegisterHooks( plugin_name='ping_counter', hook_list=hooks );

async def on_message( message: discord.Message ):

    mentioned_users = message.mentions

    for user in mentioned_users:
        mention = user.mention
        if mention.find( '!' ) != -1:
            mention = mention.replace( '!', '' );
        counts = json.load( open( '{}\\plugins\\ping_counter.json'.format( abspath ), 'r' ) );
        counts[ mention ] = counts[ mention ] + 1 if mention in counts else 1;
        open( '{}\\plugins\\ping_counter.json'.format( abspath ), 'w' ).write( json.dumps( counts, indent=1));

from plugins.main import *

command = Commands()
command.information ='''
Tell how many times a user has been pinged

- ping_counter ``user mention``
'''
command.function = 'on_command'

RegisterCommand( plugin_name='ping_counter', command_name='ping_counter', command_class=command );

async def on_command( message: discord.Message, arguments: dict ):

    if '0' in arguments:
        counts = json.load( open( '{}\\plugins\\ping_counter.json'.format( abspath ), 'r' ) );
        times = 0 if not arguments[ '0' ] in counts else counts[ arguments[ '0' ] ]
        await message.reply( "The user {} has been pinged {} times <:pingreee:911150900666572842>".format( arguments[ '0' ], times ))
