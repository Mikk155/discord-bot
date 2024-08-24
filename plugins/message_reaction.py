from plugins.main import *

hooks = [
    Hooks.on_message
];

RegisterHooks( plugin_name='message_reaction', hook_list=hooks );

async def on_message( message: discord.Message ):

    for keyword, emote in config[ "mention_reaction" ].items():

        if keyword in message.content.lower():

            await message.add_reaction( emote )
