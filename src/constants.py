from typing import *

class HexColor:
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

class Days:
    MONDAY = 1;
    TUESDAY = 2;
    WEDNESDAY = 3;
    THURSDAY = 4;
    FRIDAY = 5;
    SATURDAY = 6;
    SUNDAY = 7;

    Map: dict[ str, int ] = {
        'MONDAY': 1,
        'TUESDAY': 2,
        'WEDNESDAY': 3,
        'THURSDAY': 4,
        'FRIDAY': 5,
        'SATURDAY': 6,
        'SUNDAY': 7,
    };

    Array: list[ str ] = [
        'MONDAY',
        'TUESDAY',
        'WEDNESDAY',
        'THURSDAY',
        'FRIDAY',
        'SATURDAY',
        'SUNDAY',
    ];

    @staticmethod
    def FromString( day: str ) -> int:
        return Days.Map.get( day.upper(), None );

    @staticmethod
    def FromInt( day: int ) -> int:
        return Days.Array[ day - 1 ] if day <= len(Days.Array) else None;

global __RegexMessageReference__;
__RegexMessageReference__ = None;

from re import Pattern;
def RegexMessageReference() -> Pattern[str]:
    global __RegexMessageReference__;
    if __RegexMessageReference__ is None:
        import re;
        __RegexMessageReference__ = re.compile( r"https:\/\/(?:canary\.|ptb\.)?discord(?:app)?\.com\/channels\/(\d+)\/(\d+)\/(\d+)" );
    return __RegexMessageReference__;

class ReactionState:
    Added: Literal[1] = 1;
    Removed: Literal[2] = 0;

class ServerBoostState:
    Suscription: Literal[0] = 0;
    TierOne: Literal[1] = 1;
    TierTwo: Literal[2] = 2;
    TierThree: Literal[3] = 3;

class TemporalCache:
    NoExists: Literal[0] = 0;
    '''Temporal variable exists: ( NoExists, None, None )'''
    Expired: Literal[1] = 1;
    '''Temporal variable exists but it has expired and has just been removed from the cache: ( Expired, datetime, data? )'''
    Exists: Literal[2] = 2;
    '''Temporal variable exists and still has a time ahead to expire: ( Exists, datetime, data? )'''
