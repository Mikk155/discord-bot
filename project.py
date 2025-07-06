'''
MIT License

Copyright (c) 2025 Mikk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
'''

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
