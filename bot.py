from plugins.main import *

# Initialise plugins
def PluginsInit():

    modulos_path = os.path.join( abspath, "plugins" );

    for file in os.listdir( modulos_path ):

        if file.endswith( ".py" ) and not file.endswith( 'main.py' ):

            try:

                modulo:str = file[ : len(file) - 3 ];

                spec = importlib.util.spec_from_file_location( modulo, os.path.join( modulos_path, file ) );

                obj = importlib.util.module_from_spec( spec );

                spec.loader.exec_module( obj );

            except Exception as e:

                print( f"Error importing plugin {file}: {e}" );

PluginsInit();




# BOT Events
@bot.event

async def on_ready():

    await log_channel('We have logged in as {0.user}'.format( bot ) )

    await bot.wait_until_ready();

    print( f'Loaded { len( plugins ) } plugin{ "s" if len( plugins ) > 1 else "" }' );

    await HookManager.CallHook( 'on_ready' );

    on_think.start()


@bot.event

async def on_member_join( member : discord.Member ):

    await HookManager.CallHook( 'on_member_join', member );



@tasks.loop( seconds = 1 )

async def on_think():

    await bot.wait_until_ready();

    await HookManager.CallHook( 'on_think' );

    gpGlobals.time += 1;



@bot.event

async def on_member_remove( member : discord.Member ):

    await HookManager.CallHook( 'on_member_remove', member );



@bot.event

async def on_message( message: discord.Message ):

    await HookManager.CallHook( 'on_message', message );

    if message.content.startswith( config[ "prefix" ] ):

        message.content = message.content[ len( config[ "prefix" ] ) : ];

        if message.content == 'help':

            pages: list[discord.Embed] = []

            for cmd, data in commandos.items():

                data: Commands

                if data.servers and not message.guild.id in data.servers:
                    continue;

                if data.allowed:
                    if not any( role_id in [ role.id for role in message.author.roles ] for role_id in data.allowed ):
                        continue;

                embeed = discord.Embed( title='``{}{}``'.format( config[ "prefix" ], cmd ), description=data.information, color=discord.Color.blurple() );

                pages.append( embeed )

            help_msg: discord.Message = await message.reply( embed=pages[0] )

            await help_msg.add_reaction("◀️")
            await help_msg.add_reaction("▶️")

            def check( reaction, user ):
                return user == message.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == help_msg.id

            current_page = 0

            while True:

                try:

                    reaction, user = await bot.wait_for("reaction_add", timeout=70.0, check=check );

                    if str(reaction.emoji) == "▶️":
                        current_page += 1
                    elif str(reaction.emoji) == "◀️":
                        current_page -= 1

                    if current_page < 0:
                         current_page = len( pages ) - 1;
                    elif current_page > len( pages ) - 1:
                        current_page = 0;

                    await help_msg.edit( embed=pages[ current_page ] );
                    await help_msg.remove_reaction( reaction.emoji, user );

                except asyncio.TimeoutError:
                    await help_msg.delete();
                    break
        else:

            cmd = message.content.split()[0];

            args_str = message.content[ len( cmd ) : ];

            args_list = args_str.split( "," )
            args_dict = {}

            for i, arg in enumerate( args_list ):
                arg = arg.strip( ' ' );
                if len(arg) > 0:
                    if '=' in arg and arg[0] != '=' and arg[len(arg)-1] != '=':
                        dks = arg.split( '=', 1 );
                        args_dict[ dks[0] ] = dks[1];
                    else:
                        args_dict[ str( i ) ] = arg;

            if cmd in commandos:

                command : Commands = commandos[ cmd ];

                if command.servers and not message.guild.id in command.servers:
                    return;

                if command.allowed:
                    if not any( role_id in [ role.id for role in message.author.roles ] for role_id in command.allowed ):
                        await message.reply( f"{message.author.mention} This command is for specific roles only." );
                        return;

                module = importlib.import_module( f'plugins.{command.plugin}' );
                hook = getattr( module, command.function );

                try:
                    await hook( message, args_dict )
                except Exception as e:
                    await log_channel( 'Exception on plugin {} at function {} error: {}'.format( command.plugin, command.function, e ) );




@bot.event

async def on_message_delete( message: discord.Message ):

    await HookManager.CallHook( 'on_message_delete', message );



@bot.event

async def on_message_edit( before: discord.Message, after: discord.Message ):

    Args = HookValue();

    Args.edited.before = before;

    Args.edited.after = after;

    await HookManager.CallHook( 'on_message_edit', Args.edited );



@bot.event

async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):

    Args = HookValue();

    Args.reaction.reaction = reaction;

    Args.reaction.user = user;

    await HookManager.CallHook( 'on_reaction_add', Args.reaction );



@bot.event

async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):

    Args = HookValue();

    Args.reaction.reaction = reaction;

    Args.reaction.user = user;

    await HookManager.CallHook( 'on_reaction_remove', Args.reaction );



token_dev = 'test_' if gpGlobals.developer else '';

TOKEN = open( '{}\\{}token.txt'.format( abspath, token_dev ), 'r' ).readline();

if not TOKEN:

    raise Exception( 'Can not open token.txt!' );

bot.run( TOKEN );
