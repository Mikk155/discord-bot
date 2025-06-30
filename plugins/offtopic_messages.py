from src.main import *
from src.PluginManager import Plugin;

class offtopic_messages( Plugin ):

    @property
    def GetDescription(self):
        return "Remove off-topic messages on specific channels";

    async def OnMessage(self, message):

        if message.author.id == bot.user.id:
            return True;

        # LP Memes
        if message.channel.id == 1343244435583926323:

            Elements = len( message.embeds ) + len( message.attachments );

            if Elements == 0 and not message.author.guild_permissions.administrator:

                response = await message.reply( f"This channel is for memes only. Please forward your target message and reply somewhere else",\
                                        silent=True, delete_after=10 );

                await message.delete(); # -TODO Does the bot really not log deleted messages?
                # May need an utility to call OnMessageDelete passing the bot as the deleter.

                return False;

        elif message.channel.id == 1118352656096829530:

            await message.delete(); #-TODO Ditto

            return False;

        return True;
