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

def DEVELOPER() -> bool:

    '''
    Returns whatever the bot has been run with the ``-dev`` argument
    '''

    from sys import argv;

    return ( '-dev' in argv );

def HOOK_CONTINUE() -> int:

    '''
    Returns the hook as "continue" status
    '''

    return 0;

def HOOK_HANDLED() -> int:

    '''
    Returns the hook as "handled" and next hooks from plugins in the list bellow this won't be called
    '''

    return 1;


def INVALID_INDEX() -> int:

    '''
    Returns an invalid index for integer comparations
    '''

    return -1;

def CHARACTER_LIMIT() -> int:
    '''
    Returns the Discord's character limits per discord.Message's content
    '''

    return 2000;

from src.main import discord
def IS_OWNER( user: discord.User | discord.Member | int ) -> bool:
    '''
    Returns whatever this user is the owner of this app
    '''

    from src.CConfigSystem import g_Config;

    if isinstance( user, int ):

        return ( g_Config.configuration[ "owner" ] == user );

    return ( user and g_Config.configuration[ "owner" ] == user-id );

def COMMON_TIMEZONES() -> list:

    '''
    Returns a list of common timezones
    '''

    return [
        "UTC",
        "America/Argentina/Cordoba",
        "America/Lima",
        "America/New_York",
        "America/Los_Angeles",
        "America/Mexico_City",
        "Europe/London",
        "Europe/Paris",
        "Europe/Berlin",
        "Europe/Moscow",
        "Asia/Shanghai",
        "Asia/Tokyo",
        "Asia/Kolkata",
        "Asia/Dubai",
        "Africa/Johannesburg",
        "Australia/Sydney",
        "America/Sao_Paulo",
        "Pacific/Auckland",
        "Pacific/Honolulu",
        "Asia/Singapore",
        "America/Toronto",
        "Asia/Seoul",
        "America/Bogota",
        "Asia/Jakarta",
        "Europe/Istanbul"
    ];

LUNES       = 1
MARTES      = 2
MIERCOLES   = 3
JUEVES      = 4
VIERNES     = 5
SABADO      = 6
DOMINGO     = 7
MONDAY      = 1
TUESDAY     = 2
WEDNESDAY   = 3
THURSDAY    = 4
FRIDAY      = 5
SATURDAY    = 6
SUNDAY      = 7
