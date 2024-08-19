async def on_message( message: discord.Message ):

    if 'https://x.com/' in message.content:

        twitter_url = message.content.split(' ')[-1]

        await message.reply( twitter_url.replace( 'x', 'fxtwitter', 1 ) )
        # await message.reply( twitter_url.replace( 'x', 'vxtwitter', 1 ) )
