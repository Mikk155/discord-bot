from plugins.main import *

hooks = [
    Hooks.on_message
];

RegisterHooks( plugin_name='fix_instagram', hook_list=hooks );

async def on_message( message: discord.Message ):

    if 'www.instagram.com' in message.content:

        author = message.author.mention;

        formatted = message.content.replace( 'www.instagram.com', 'www.ddinstagram.com' );

        await message.channel.send(  '{}: {}'.format( author, formatted ) );

        await message.delete();

        return ReturnCode.Handled;
