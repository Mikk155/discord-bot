from src.main import *;

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    if not bot.__on_start_called__:

        await g_PluginManager.CallFunction( "OnBotStart" );

        bot.__on_start_called__ = True;

        print( g_Sentences.get( "ready", bot.user.name, bot.user.discriminator ) );

    else:

        await g_PluginManager.CallFunction( "OnReconnect" );

    from src.events.on_think import on_think;

    if not on_think.is_running():

        on_think.start()
