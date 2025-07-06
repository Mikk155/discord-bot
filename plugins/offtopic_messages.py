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

from project import *

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
