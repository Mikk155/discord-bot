# Walter

Walter has a hooking system, Create your modules in ``modulos\`` to do your stuff

# hooks

```python
from __main__ import bot
async def on_ready():
async def on_think( time: int ):
async def on_member_join( member : discord.Member ):
async def on_member_remove( member : discord.Member ):
async def on_message( message: discord.Message ):
async def on_message_delete( message: discord.Message ):
async def on_message_edit( before: discord.Message, after: discord.Message ):
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):
```
