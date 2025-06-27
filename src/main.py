import discord

from utils.Logger import Logger;
global g_Logger;
g_Logger: Logger = Logger( "Global" );

from utils.fmt import fmt;

from src.CacheManager import g_Cache;
from src.ConfigContext import g_ConfigContext;
from src.PluginManager import g_PluginManager;
from src.Bot import bot
