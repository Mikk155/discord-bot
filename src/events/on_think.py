from src.main import *;

from discord.ext.tasks import loop as Loop
@Loop( seconds = 1.0, reconnect=True, name="on_think" )
async def on_think():

    await bot.wait_until_ready()

    g_Cache.UpdateCache();

    from datetime import datetime;

    now: datetime = datetime.now();

    await g_PluginManager.CallFunction( "OnThink", now );
