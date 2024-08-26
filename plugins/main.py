import os
import re
import sys
import time
import json
import random
import asyncio
import discord
import requests
import subprocess
import importlib
from git import Repo
import importlib.util
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

global gpGlobals
class gpGlobals:

    time = 0;
    '''Current time of think.
    This increases in 1 each second.
    '''

    developer = True if len( sys.argv ) > 1 and sys.argv[1] else False;
    '''
    Returns **True** If the bot has been run by ``test.bat``
    '''

    Logger = True
    '''
    Set to *True* for getting loggers
    '''

def get_time( seconds : int ) -> str:
    m = seconds // 60;
    sr = seconds % 60;
    return f"{m}m:{sr:02d}s";

def jsonc( obj : list[str] | str ) -> dict | list:
    __js_split__ = '';
    __lines__: list[str];
    if isinstance( obj, list ):
        __lines__ = obj;
    else:
        __lines__ = open( obj, 'r' ).readlines();
    for __line__ in __lines__:
        __line__ = __line__.strip();
        if __line__ and __line__ != '' and not __line__.startswith( '//' ):
            __js_split__ = f'{__js_split__}\n{__line__}';
    return json.loads( __js_split__ )

global abspath;
abspath = os.path.abspath( "" );

global config
config:dict = jsonc( '{}\\config.json'.format( abspath ) );

if not config:
    raise Exception( 'Can not open config.json!' )

global bot
bot: commands.Bot = commands.Bot( command_prefix = config[ "prefix" ], intents = discord.Intents.all() );

global modulos;
plugins : dict = {};

global commandos
commandos: dict = {};

def Logger( string: str, arguments : list[str] = [], cut_not_matched : bool = False, not_matched_trim : bool = False ):

    for __arg__ in arguments:
        string = string.replace( "{}", str( __arg__ ), 1 )

    if cut_not_matched:
        __replace__ = '{} ' if not_matched_trim else '{}'
        string.replace( __replace__, '' )

    if gpGlobals.Logger:
        print( string )

class ReturnCode:
    Handled = 1;
    '''Handles the hook and stop calling other plugins'''
    Continue = 0;
    '''Continue calling other hooks'''

class Hooks:
    '''
    Hooks supported for the bot
    '''
    on_ready = 'on_ready'
    on_think = 'on_think'
    on_member_join = 'on_member_join'
    on_member_remove = 'on_member_remove'
    on_message = 'on_message'
    on_message_delete = 'on_message_delete'
    on_message_edit = 'on_message_edit'
    on_reaction_add = 'on_reaction_add'
    on_reaction_remove = 'on_reaction_remove'
    on_command = 'on_command'

def RegisterHooks( plugin_name : str, hook_list : list[ Hooks ] ):
    plugins[ plugin_name ] =  hook_list;
    print( f'{plugin_name} Registered hooks: {hook_list}' );

class Commands:
    plugin : str = None
    '''Name of the plugin'''
    function : str = None
    information : str = None
    '''Information display for this command (help)'''
    command : str = None
    '''Command show and arguments (help)'''
    servers : list[int] = None
    '''Servers-only command, leave empty for global'''
    allowed : list[int] = None
    '''List of roles that are allowed to use this command, if None = everyone'''

def RegisterCommand( plugin_name : str, command_name : str, command_class : Commands ):
    command_class.plugin = plugin_name
    commandos[ command_name ] = command_class;
    print( f'{plugin_name} Registered command: {command_name}' );

class HookValue:
    class edited:
        before : discord.Message
        after : discord.Message
    class reaction:
        reaction : discord.Reaction
        user : discord.User

class HookManager:
    async def CallHook( hook_name, HookValue = None ):
        for plugin, hooks in plugins.items():
            if f'{hook_name}' in hooks:
                module = importlib.import_module( f'plugins.{plugin}' );
                hook = getattr( module, hook_name );
                try:
                    hook_code = await hook( HookValue ) if HookValue is not None else await hook();
                    if hook_code == ReturnCode.Handled:
                        break;
                except Exception as e:
                    print( 'Exception on plugin {} at function {} error: {}'.format( plugin, hook_name, e ) );
