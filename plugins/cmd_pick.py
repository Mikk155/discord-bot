from plugins.main import *

command = Commands()
command.information ='''
Pick a random option from the arguments provided,

- pick ``option 1``, ``option 2``, ``option 3``, ``etc``
'''
command.function = 'on_command'

RegisterCommand( plugin_name='cmd_pick', command_name='pick', command_class=command );

async def on_command( message: discord.Message, arguments: dict ):

    if len(arguments) >= 1:
        choice = random.randint( 0, len( arguments ) - 1 );
        choice = arguments[ str( choice ) ];
        await message.channel.send( "I pick ``{}``".format( choice ) );
