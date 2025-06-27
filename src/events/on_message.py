from src.main import *;

@bot.event
async def on_message( message: discord.Message ):

    await g_PluginManager.CallFunction( "OnMessage", message, GuildID=message.guild.id );

    if g_ConfigContext.prefix is not None and message.content.startswith( g_ConfigContext.prefix ):

        arguments_string = message.content[ len(g_ConfigContext.prefix) : ];

        from shlex import split as SplitArgs;

        arguments = SplitArgs( arguments_string );

        command = arguments.pop(0);

        await g_PluginManager.CallFunction( "OnCommand", message, command, arguments, GuildID=message.guild.id );

    if message.mentions and len( message.mentions ) > 0:

        await g_PluginManager.CallFunction( "OnMention", message, message.mentions, GuildID=message.guild.id );

    if message.reference and message.reference.message_id:

        replied_message = await message.channel.fetch_message( message.reference.message_id );

        if replied_message:

            await g_PluginManager.CallFunction( "OnReply", message, replied_message, GuildID=message.guild.id );

    if 'https://' in message.content or 'www.' in message.content:

        urls: tuple[str] = ( url for url in message.content.split() if url.startswith( 'https://' ) or url.startswith( 'www.' ) );

        await g_PluginManager.CallFunction( "OnLink", message, urls, GuildID=message.guild.id );
