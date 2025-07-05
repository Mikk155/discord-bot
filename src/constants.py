from typing import *
from enum import IntEnum

class HexColor(IntEnum):
    RED = 0xFF0000
    GREEN = 0x00FF00
    YELLOW = 0xFFFF00
    BLUE = 0x0000FF
    MAGENTA = 0xFF00FF
    CYAN = 0x00FFFF
    PURPLE = 0x800080;
    GRAY = 0x808080,;
    BLACK = 0x000000,;
    WHITE = 0xFFFFFF,;
    LIGHT_BLUE = 0x196990;

def CommonTimezones() -> tuple[str]:

    return (
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
    );

class ReactionState(IntEnum):
    Added: int = 1;
    Removed: int = 0;

class EmojiFlags(IntEnum):
    Unicode: int = ( 1 << 0 );
    ServerCustom: int = ( 1 << 1 );
    BotCanUse: int = ( 1 << 2 );
    '''Is a custom emoji from a server the bot is in and have access to'''

class ServerBoostState(IntEnum):
    Suscription: int = 0;
    TierOne: int = 1;
    TierTwo: int = 2;
    TierThree: int = 3;

class TemporalCache(IntEnum):
    NoExists: int = 0;
    '''Temporal variable exists: ( NoExists, None, None )'''
    Expired: int = 1;
    '''Temporal variable exists but it has expired and has just been removed from the cache: ( Expired, datetime, data? )'''
    Exists: int = 2;
    '''Temporal variable exists and still has a time ahead to expire: ( Exists, datetime, data? )'''

class LoggerLevel(IntEnum):

    AllLoggers: int = -1;
    Critical: int = ( 1 << 0 ); # critical is ignored and will always being enable
    Error: int = ( 1 << 1 ); # The same goes for error
    Warning: int = ( 1 << 2 );
    Information: int = ( 1 << 3 );
    Debug: int = ( 1 << 4 );
    Trace: int = ( 1 << 5 );

class LoggerFlags(IntEnum):
    Nothing: int = 0;
    PrintTerminal: int = ( 1 << 0 );
    PrintDiscord: int = ( 1 << 1 );
