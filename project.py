# Multiple utilities
from utils.Path import Path;
from utils.datetime import Days;
from utils.Regex import RegexPattern;
from utils.Dictionary import Dictionary;
from utils.fmt import fmt;
from utils.jsonc import jsonc;
from utils.RGB import RGB;

# Various libraries used by the main code itself
import pytz;
import emoji as EMOJI;
import random;
import discord;
from datetime import datetime, timedelta;
from discord import app_commands;

from src.Plugin import Plugin;

from src.constants import *

global g_DiscordLogger;
from src.Logger import g_DiscordLogger, ToLoggerLevel;

global g_Sentences;
from src.Sentences import g_Sentences;

global g_Cache;
from src.CacheManager import g_Cache;

global g_ConfigContext;
from src.ConfigContext import g_ConfigContext;

global bot;
from src.Bot import bot

global g_PluginManager;
from src.PluginManager import g_PluginManager
