from plugins.main import *

hooks = [
    Hooks.on_message
];

RegisterHooks( plugin_name='fix_twitter', hook_list=hooks );

async def on_message( message: discord.Message ):

    if 'https://x.com/' in message.content:

        author = message.author.mention;

        formatted = message.content.replace( 'https://x.com/', 'https://fxtwitter.com/' );

        await message.channel.send(  '{}: {}'.format( author, formatted ) );

        await message.delete();

        return ReturnCode.Handled;
