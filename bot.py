"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from src.main import *

#=======================================================================================
# on_start
#=======================================================================================

async def on_start():

    if not DEVELOPER():

        bot.m_Logger.info(
            "object.initialized",
            [
                f'{__name__}(bot.py)'
            ],
            dev=True
        );

    try:

        await g_PluginManager.callhook( Hooks.on_start );

    except Exception as e:

        bot.m_Logger.error( e );

    if os.getenv( 'github' ):

        print( "Run from {}".format( os.getenv( 'github' ) ) );

        await bot.close();

        exit(0);

    bot.__on_start_called__ = True;

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_ready
#=======================================================================================

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    bot.m_Logger.info(
        'bot.on.ready',
        [
            bot.user.name,
            bot.user.discriminator
        ],
        dev=True
    );

    if not bot.__on_start_called__:

        await on_start();

    try:

        await g_PluginManager.callhook( Hooks.on_ready );

    except Exception as e:

        bot.m_Logger.error( e );

    if not on_think.is_running():

        on_think.start()

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_message
#=======================================================================================

@bot.event
async def on_message( message: discord.Message ):

    #=======================================================================================
    # on_mention
    #=======================================================================================

    if message.mentions and len( message.mentions ) > 0:

        try:

            await g_PluginManager.callhook( "on_mention", message, message.mentions, guild=message.guild );

        except Exception as e:

            bot.m_Logger.error( e );

    #=======================================================================================
    # END
    #=======================================================================================

    #=======================================================================================
    # on_reply
    #=======================================================================================

    if message.reference and message.reference.message_id:

        try:

            replied_message = await message.channel.fetch_message( message.reference.message_id );

            if replied_message:

                try:
    
                    await g_PluginManager.callhook( "on_reply", message, replied_message, guild=message.guild );

                except Exception as e:

                    bot.m_Logger.error( e );

        except discord.NotFound:

            pass;

    #=======================================================================================
    # END
    #=======================================================================================

    #=======================================================================================
    # on_link
    #=======================================================================================

    if 'https://' in message.content or 'www.' in message.content:

        contents = message.content.split();

        urls=[]

        for c in contents:

            if c.startswith( 'https://' ) or c.startswith( 'www.' ):

                urls.append( c );

        if len( urls ) > 0:

            try:

                await g_PluginManager.callhook( "on_link", message, urls, guild=message.guild );

            except Exception as e:

                bot.m_Logger.error( e );

    #=======================================================================================
    # END
    #=======================================================================================

    try:

        await g_PluginManager.callhook( 'on_message', message, guild=message.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_member_join
#=======================================================================================

@bot.event
async def on_member_join( member : discord.Member ):

    try:

        await g_PluginManager.callhook( 'on_member_join', member, guild=member.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_member_remove
#=======================================================================================

@bot.event
async def on_member_remove( member : discord.Member ):

    try:

        await g_PluginManager.callhook( 'on_member_remove', member, guild=member.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_message_delete
#=======================================================================================

@bot.event
async def on_message_delete( message: discord.Message ):

    try:

        await g_PluginManager.callhook( 'on_message_delete', message, guild=message.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_message_edit
#=======================================================================================

@bot.event
async def on_message_edit( before: discord.Message, after: discord.Message ):

    try:

        await g_PluginManager.callhook( 'on_message_edit', before, after, guild=before.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_reaction_add
#=======================================================================================

@bot.event
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):

    try:

        await g_PluginManager.callhook( 'on_reaction_add', reaction, user, guild=reaction.message.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_reaction_remove
#=======================================================================================

@bot.event
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):

    try:

        await g_PluginManager.callhook( 'on_reaction_remove', reaction, user, guild=reaction.message.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_typing
#=======================================================================================

@bot.event
async def on_typing( channel: discord.TextChannel | discord.GroupChannel | discord.DMChannel, user: discord.Member | discord.User, when: datetime.datetime ):
    
    try:

        await g_PluginManager.callhook( 'on_typing', channel, user, when, guild=channel.guild );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_think
#=======================================================================================

@tasks.loop( seconds = 10.0, name=Hooks.on_think )
async def on_think():

    await bot.wait_until_ready()

    g_Cache.__update__();

    async_think = []

    for plugin in g_PluginManager.fnMethods[ Hooks.on_think ]:

        try:

            if not plugin in g_PluginManager.module_cache:
                continue;

            module = g_PluginManager.module_cache[ plugin ];

            hook = getattr( module, Hooks.on_think );

            if not hook in async_think:

                async_think.append( hook() );

        except Exception as e:

            __attribute__ = ''

            if str(e).find( 'has no attribute' ) != -1:

                g_PluginManager.module_cache.pop( plugin );

                from src.CSentences import g_Sentences

                __attribute__ = g_Sentences.get( 'plugin_manager.callhook.attribute' )

            g_PluginManager.m_Logger.error(
                'plugin_manager.callhook.exception',
                [
                    plugin,
                    Hooks.on_think,
                    e,
                    __attribute__
                ],
                dev=True
            );

    try:

        if g_DelayedLog.should_print():

            async_think.append( g_DelayedLog.print_server(bot) );

        await bot.wait_until_ready();

        if async_think:

            await asyncio.gather( *async_think );

    except Exception as e:

        bot.m_Logger.error( e );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# Initialize the plugin manager
#=======================================================================================

g_PluginManager.initialize();

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# plugin_info command
#=======================================================================================

my_plugin_choices = []

for k, v in g_PluginManager.plugins.items():

    my_plugin_choices.append( app_commands.Choice( name=k, value=v[ "name" ] if v else "" ) );

print( my_plugin_choices );

@bot.tree.command()
@app_commands.guild_only()
@app_commands.choices( plugin = my_plugin_choices )
@app_commands.describe( plugin='Plugin' )
async def plugin_info( interaction: discord.Interaction, plugin: app_commands.Choice[str] ):
    """Show plugins information"""

    await interaction.response.defer( thinking=True );

    try:

        if plugin.name in g_PluginManager.plugins:

            info = g_PluginManager.plugins[ plugin.name ];

            embed = discord.Embed( title = plugin.name, color = 16711680 );

            if info:

                embed.title = info[ "name" ];

                embed.description = info[ "description" ];

                embed.add_field( inline = True,
                    name = g_Sentences.get( "status", interaction.guild_id ),
                    value = '✅ ' + g_Sentences.get( "enabled", interaction.guild_id )
                );

                embed.add_field( inline = True,
                    name = g_Sentences.get( "plugin_manager.author", interaction.guild_id ),
                    value = info[ "author" ]
                );

                embed.add_field( inline = True,
                    name = g_Sentences.get( "plugin_manager.contact", interaction.guild_id ),
                    value = info[ "contact" ]
                );

                if "hooks" in info and len( info[ "hooks" ] ) > 0:

                    embed.add_field( inline = True,
                        name = "Hooks",
                        value = '``{}``'.format( info[ "hooks" ] )
                    );

            else:

                embed.title = plugin.name;

                embed.description = '❌ ' + g_Sentences.get( "disabled", interaction.guild_id );

            await interaction.followup.send( embed=embed );

        else:

            await interaction.followup.send( g_Format.brackets( g_Sentences.get( "file.not.exists", interaction.guild_id ), [ plugin.name ] ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# run bot
#=======================================================================================

def get_token() -> str:

    __token__: list[str] = [ INVALID_INDEX(), INVALID_INDEX() ];

    if os.getenv( 'github' ):

        __token__[0] = os.getenv( 'token' );

    else:

        tokens: str = g_Path.join( 'tokens.txt' );

        if os.path.exists( tokens ):

            __token__ = open( tokens, 'r' ).readlines();

        else:

            bot.m_Logger.critical( "file.not.exists", [ tokens ] );

            exit(0)

    token = __token__[ 1 if DEVELOPER() else 0 ];

    if not isinstance( token, str ):

        token = str(token);

    return token;

try:

    bot.run( token = get_token(), reconnect = True );

except Exception as e:

    bot.m_Logger.critical( e );

#=======================================================================================
# END
#=======================================================================================
