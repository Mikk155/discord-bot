# Walter

```
pip install -r requirements.txt
```

Walter has a hooking system, Create your modules in ``plugins\`` to do your stuff

# hooking system

Import ``main``:
```python
from plugins.main import *
```

Initialise an array of Hooks:
```python
hooks = [
    Hooks.on_think
];
```

Register these hooks:
```python
Plugin( plugin_name='Activity', hook_list=hooks );
```
- Note: ``plugin_name`` is the plugin's filename.

Available hooks:
```python
async def on_ready():
async def on_think():
async def on_member_join( member : discord.Member ):
async def on_member_remove( member : discord.Member ):
async def on_message( message : discord.Message ):
async def on_message_delete( message : discord.Message ):
async def on_message_edit( Args : HookValue.message_delete ):
async def on_reaction_add( Args : HookValue.reaction ):
async def on_reaction_remove( Args : HookValue.reaction ):
```
