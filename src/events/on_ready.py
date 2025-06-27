from src.main import *;

@bot.event
async def on_ready():

    await bot.wait_until_ready();

#            bot.user.name,
#            bot.user.discriminator

    if not bot.__on_start_called__:

        g_PluginManager.CallFunction( "OnBotStart" );

        bot.__on_start_called__ = True;

    else:

        g_PluginManager.CallFunction( "OnReconnect" );

    print( f"Connected as {bot.user.name}#{bot.user.discriminator}")
