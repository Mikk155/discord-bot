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
    Added = 1;
    Removed = 0;

class ServerBoostState:
    Suscription = 0;
    TierOne = 1;
    TierTwo = 2;
    TierThree = 3;

class BotLogMode:
    Nothing = 0;
    DeveloperChannel = ( 1 << 0 );
    ConsoleTerminal = ( 1 << 1 );
