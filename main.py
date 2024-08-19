import os
import sys
import discord
import asyncio
import random
from discord.ext import commands, tasks

abs = os.path.abspath( "" );

modulos : dict = {};

from walter.config import config

class gpGlobals:

    time = 0
    '''Current time of think.
    This increases in 1 each second.
    '''

    debug = True if len(sys.argv) > 1 and sys.argv[1] else False
    '''
    Returns **True** If the bot has been run by ``test.bat``
    '''

    Logger = True
    '''
    Set to *True* for getting loggers
    '''

def Logger( string: str, arguments : list[str] = [], cut_not_matched : bool = False, not_matched_trim : bool = False ):

    for __arg__ in arguments:
        string = string.replace( "{}", str( __arg__ ), 1 )

    if cut_not_matched:
        __replace__ = '{} ' if not_matched_trim else '{}'
        string.replace( __replace__, '' )

    if gpGlobals.Logger:
        print( string )

bot = commands.Bot( command_prefix = config[ "prefix" ], intents = discord.Intents.all() );

@bot.event
async def on_member_join( member : discord.Member ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_member_join( member );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_member_join', e ] );

@bot.event
async def on_member_remove( member : discord.Member ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_member_remove( member );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_member_remove', e ] );

@bot.event
async def on_message( message: discord.Message ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_message( message );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_message', e ] );

@bot.event
async def on_message_delete( message: discord.Message ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_message_delete( message );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_member_join' ] );

@bot.event
async def on_message_edit( before: discord.Message, after: discord.Message ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_message_edit( before, after );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_message_edit', e ] );

@bot.event
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_reaction_add( reaction, user );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_member_join' ] );

@bot.event
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):
    for name, modulo in modulos.items():
        try:
            await modulo.on_reaction_remove( reaction, user );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_reaction_remove', e ] );

@tasks.loop( seconds = 1 )
async def on_think():

    await bot.wait_until_ready()

    global gpGlobals
    gpGlobals.time += 1

    for name, modulo in modulos.items():
        try:
            await modulo.on_think( gpGlobals.time );
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_think', e ] );

@bot.event
async def on_ready():

    from walter.hooking import init as init_hooking
    init_hooking();

    print( f'Loaded { len( modulos ) } module{ "s" if len( modulos ) > 1 else "" }' );

    print('We have logged in as {0.user}'.format( bot ) )

    for name, modulo in modulos.items():
        try:
            await modulo.on_ready()
        except Exception as e:
            if str(e).find( 'has no attribute' ) == -1:
                Logger( "Exception in {} at {}: {}", [ name, 'on_ready', e ] );

    on_think.start()

from walter.token import TOKEN

bot.run( TOKEN )