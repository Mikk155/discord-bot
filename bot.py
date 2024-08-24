from plugins.main import *

# Initialise plugins
def PluginsInit():

    modulos_path = os.path.join( abs, "plugins" );

    for file in os.listdir( modulos_path ):

        if file.endswith( ".py" ) and not file.endswith( 'main.py' ):
            print(file)

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

    print('We have logged in as {0.user}'.format( bot ) )

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

    if message.content.startswith( config[ "prefix" ] ):

        message.content = message.content[ len( config[ "prefix" ] ) : ];


        if message.content == 'help':

            st: str #TODO

        else:

            await HookManager.CallHook( 'on_command', message );

    else:

        await HookManager.CallHook( 'on_message', message );



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



TOKEN = open( '{}\\token.txt'.format( abs ), 'r' ).readline();

if not TOKEN:

    raise Exception( 'Can not open token.txt!' );

bot.run( TOKEN );
