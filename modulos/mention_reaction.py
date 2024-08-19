
from __main__ import config

import discord

async def on_message( message: discord.Message ):

    for keyword, emote in config[ "mention_reaction" ].items():

        if keyword in message.content.lower():

            await message.add_reaction( emote )
