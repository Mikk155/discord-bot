from typing import *;
import discord;
from discord import app_commands;

from utils.Logger import Logger;
global g_Logger;
g_Logger: Logger = Logger( "Global" );

from utils.fmt import fmt;

from src.Sentences import g_Sentences;
from src.CacheManager import g_Cache;
from src.ConfigContext import g_ConfigContext;
from src.Bot import bot
from src.PluginManager import g_PluginManager;