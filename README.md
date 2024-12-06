# discord-bot

Template discord bot that supports a "Plugin" implementation with a hooking system

```
pip install -r requirements.txt
```

Create a file ``config.json`` in the workspace.

Open it and follow the schema instruction provided by this snippet:
```json
{
    "$schema": "schema.json"
}
```
You have ``./config_example.json`` for examples

After you have configured the bot you can run it in background with a .bat file:
```bat
start "" /B pythonw bot.py
```

Or either in developer mode:
```bat
@echo off

python bot.py -dev

pause
```
- developer mode will make the function [DEVELOPER()](src/constdef.py#L25) to return true

# Developing

Create your plugins in ``plugins/``

Import ``main``:
```python
from src.main import *
```

If you need any extra library to downoad create your own requirements at ``plugins/{your plugin name}_requirements.txt`` the bot will install them before it loads your plugin

### Pull requests are welcome and encouraged.
