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

from src.main import *;

from discord.ext.tasks import loop as Loop
@Loop( seconds = 1.0, reconnect=True, name="on_think" )
async def on_think():

    try:

        await bot.wait_until_ready()

        g_Cache.UpdateCache();

        if g_ConfigContext.log.IsActive:

            await g_DiscordLogger.SendAllMessages();

        from datetime import datetime;

        now: datetime = datetime.now();

        await g_PluginManager.CallFunction( "OnThink", now );

    except Exception as e:

        bot.HandleException( e, SendToDevs=True );
