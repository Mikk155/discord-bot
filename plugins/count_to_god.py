from plugins.main import *

hooks = [
    Hooks.on_message,
    Hooks.on_ready
];

RegisterHooks( plugin_name='count_to_god', hook_list=hooks );

async def set_role( member: discord.Member ):

    if member:

        rol = discord.utils.get( bot.get_guild( config[ "mikkserver" ][ "ID" ] ).roles, name="The Cult Member" )

        if not rol in member.roles:

            await member.add_roles( rol )

            await bot.get_channel( config[ "mikkserver" ][ "USERS" ] ).send( f'{member.mention} is now a cult member <:elegant:1216204366349078631>\n' )


async def on_message( message: discord.Message ):

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

async def on_ready():

    if gpGlobals.developer:

        return

    channel = bot.get_channel( config[ "mikkserver"][ "COUNT_TO_GOD" ] )

    if not channel:

        return

    numero_anterior = None;

    async for old_message in channel.history( limit=5 ):

        if old_message.author == bot.user:
            numero_anterior = None;
            break;

        if numero_anterior:
            continue

        if not old_message.content[0].isdigit():
            continue

        numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

        if numero_anterior:

            numero_anterior = int(numero_anterior.group(1)) + 1

    if numero_anterior:

        await channel.send( f'{numero_anterior}')
