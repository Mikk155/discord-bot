
from __main__ import bot, config, gpGlobals

import discord
import asyncio
import re

async def check_count( message: discord.Message ):

    if message.author.bot:
        return

    channel = bot.get_channel( config[ "mikkserver"][ "COUNT_TO_GOD" ] )

    if not channel or message.channel is not channel:
        return

    numero_actual = re.search( r'\b(\d+)\b', message.content )

    if numero_actual:

        numero_actual = int( numero_actual.group(1) )

    else:

        await message.delete()

        botmsg = await message.channel.send( f'{message.author.mention} Only counting on this channel!' )

        await asyncio.sleep( 5 )

        if botmsg:

            await botmsg.delete()

        return

    async for old_message in message.channel.history( limit=10, before=message.created_at ):

        if old_message.author == bot.user and not old_message.content[0].isdigit():

            continue

        numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

        if numero_anterior:

            numero_anterior = int(numero_anterior.group(1))

            break

    if numero_actual <= numero_anterior or numero_actual > numero_anterior + 1:

        if message:

            await message.delete()

        botmsg = await message.channel.send( f'{message.author.mention}, do you know how to count? :face_with_raised_eyebrow:' )

        await asyncio.sleep( 5 )

        if botmsg:

            await botmsg.delete()

async def on_message( message: discord.Message ):

    await check_count( message )

async def on_message_edit( before: discord.Message, after: discord.Message ):

    await check_count( after )

async def on_ready():

    if gpGlobals.Logger:

        return

    channel = bot.get_channel( config[ "mikkserver"][ "COUNT_TO_GOD" ] )

    if not channel:

        return

    async for old_message in channel.history( limit=10 ):

        if old_message.author == bot.user and not old_message.content[0].isdigit():

            continue

        numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

        if numero_anterior:

            numero_anterior = int(numero_anterior.group(1)) + 1

            break

    if numero_anterior:

        await channel.send( f'{numero_anterior}')
