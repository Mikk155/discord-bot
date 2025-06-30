# Creating plugins

To create a plugin you need to create a single script in within `plugins/` 

Import all from src.main to get utilities

```py
from src.main import *
```

---

Create your class inheriting from `Plugin` is important for your class to be named the same as the file name.

```py
from src.PluginManager import Plugin;

class ping_counter( Plugin ):
```

---

Override `__init__` if you need to handle stuff.

###### Note: `__init__` is called way before the bot initializes.

```py
def __init__(self):
    '''Handle your stuff here'''
```

---

Override these for information

```py
@property
def GetName( self ):
    return "Ping counter";

@property
def GetDescription( self ):
    return "Keep track of users mentioning";

@property
def GetAuthorName( self ) -> str:
    return "Your name";

@property
def GetAuthorSite( self ) -> str:
    return "URL to contact you";
```

---

Override any method from the `Plugin` class to get their hooks

These hooks are of type boolean.

If the returned value is **False** the PluginSystem will stop the execution of subsequent plugins.

The order of it is just as how they're installed in the plugins.json file.

```py
async def OnMention(self, message, mentions):

    if mentions[0].bot:

        await message.reply( "Hello" );

        return False;

    return True;
```

---

Registering slash commands

```py
def OnPluginActivate(self):

    command = app_commands.Command(
        name="pings",
        description="Get the pings of a user",
        callback=self.command_pings,
    );

    command.guild_only = True;

    bot.tree.add_command( command );

def OnPluginDeactivate(self):

    bot.tree.remove_command( "pings" );

@app_commands.describe( member='Member' )
async def command_pings( self, interaction: discord.Interaction, member: discord.Member ):

    try:

        await self.GetPingCount( member, interaction );

    except Exception as e:

        from src.Bot import bot;

        if interaction.response.is_done():

            await interaction.followup.send( embeds=bot.HandleException( e, "ping_counter::command_pings", SendToDevs=True ) );

        else:

            await interaction.response.send_message( embeds=bot.HandleException( e, "ping_counter::command_pings", SendToDevs=True ) );
```

### NOTE:
> Slash commands are not hooked so you must try-catch exceptions on your own.
