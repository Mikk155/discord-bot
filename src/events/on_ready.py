'''
MIT License

Copyright (c) 2025 Mikk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
'''

from project import *;

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    if not bot.__on_start_called__ or bot.__on_start_called__ is False:
    #
        await g_PluginManager.CallFunction( "OnBotStart" );
        bot.__on_start_called__ = True;
        g_DiscordLogger.info( g_Sentences.get( "on_bot_start", bot.user.name, bot.user.discriminator ) );
    #
    else:
    #
        # -TODO Add timedelta?
        g_DiscordLogger.info( g_Sentences.get( "on_bot_reconnect" ) );
        await g_PluginManager.CallFunction( "OnReconnect" );
    #

    from src.events.on_think import on_think;

    if not on_think.is_running():
    #
        on_think.start();
    #
