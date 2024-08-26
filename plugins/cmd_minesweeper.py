from plugins.main import *

command = Commands()
command.information ='''
Pick a random option from the arguments provided,

- minesweeper ``number of bombs``, ``blocks``, ``objetive emoji``
'''
command.function = 'on_command'

RegisterCommand( plugin_name='cmd_minesweeper', command_name='minesweeper', command_class=command );

async def on_command( message: discord.Message, arguments: dict ):

    num_bombas = 1
    if '0' in arguments:
        num_bombas = int(arguments["0"])

    blocks = 4
    if '1' in arguments:
        blocks = int(arguments['1'])

    objetive_emote = '<:walter:808255870113939477>'
    if '2' in arguments:
        objetive_emote = arguments["2"]

    columnas = 10

    total_espacios = (blocks * columnas) - num_bombas
    bombas = [":bomb:" for _ in range(num_bombas)]
    espacios = [":x:" for _ in range(total_espacios)]

    espacios.append(objetive_emote)

    tablero = bombas + espacios
    random.shuffle(tablero)

    mensaje = ""
    for i in range(blocks):
        linea = tablero[i * columnas:(i + 1) * columnas]
        mensaje += "".join([f"||{emote}||" for emote in linea]) + "\n"

    await message.reply(mensaje)
