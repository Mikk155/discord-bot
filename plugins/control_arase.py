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

class control_arase( Plugin ):

    @property
    def GetDescription(self):
        return "Control arase @kern @kez";

    async def OnMessage( self, message: discord.Message ) -> Hook:

        if message.author.id == bot.user.id:
            return Hook.Continue;

        if not message.author.id in [ 768337526888726548, 1312014737449549826 ]:
            return Hook.Continue;

        channel: discord.TextChannel = message.channel;

        if isinstance( channel, discord.GroupChannel ) or isinstance( channel, discord.DMChannel ):
            return Hook.Continue;

        cache: Dictionary = g_Cache.Plugin;

        if cache.IsEmpty:
        #
            cache[ "sleep_chance" ] = 5;
            cache[ "horny_times" ] = 0;
            cache[ "sleep_responses" ] = [
                "What the fuck arase go to sleep",
                "Go to fucking sleep arase",
                "Ok but go to sleep",
                "when sleeping",
                "Mimir time mf",
                "You ain't going to find a girlfriend at this time,"
                "Reminder para arase to fucking sleep early"
            ];
            cache[ "horny_responses" ] = [
                'mommy',
                'mama',
                'sex',
                'gf',
                'feet',
                'armpit'
            ];
        #

        if g_Cache.GetTemporal( "control_arase_mimido" )[0] != TemporalCache.Exists:
        #
            ChinchangTime: datetime = datetime.now( pytz.timezone( "Asia/Kuala_Lumpur" ) );
            hour: int = ChinchangTime.hour;

            if hour <= 5:
            #
                cache[ "sleep_chance" ] = cache[ "sleep_chance" ] - 1 if cache[ "sleep_chance" ] > 0 else 5;

                # Get a incremental chance
                if random.randint( 0, cache[ "sleep_chance" ] ) == 0:
                #
                    g_Cache.SetTemporal( "control_arase_mimido", timedelta( hours = ( 6 - hour ) ) );

                    user: discord.User = await bot.fetch_user( 438449162527440896 ); # Kez

                    webhook: discord.Webhook = await bot.webhook( message.channel );

                    MimirTexts: list[str] = cache[ "sleep_responses" ];

                    await webhook.send(
                        content='[a mimir](https://cdn.discordapp.com/attachments/847485688282480640/1376229990378508398/a_mimir.mp4?ex=6834918e&is=6833400e&hm=ea97d291d22f7a0dbc723032baee9ce6d4e195e112913df24b786cfb9e697e2a&)',
                        embed=discord.Embed(
                            color=RGB(90,30,10).hex,
                            title="A R A S E",
                            description=MimirTexts[ random.randint( 0, len(MimirTexts) - 1 ) ],
                            timestamp=ChinchangTime
                        ),
                        username='KEZÆIV',
                        avatar_url=user.avatar.url
                            if user.avatar
                            else None
                    );
                #
            #
        #

        if g_Cache.GetTemporal( "control_arase_horny" )[0] != TemporalCache.Exists:

            content: str = message.content.lower();

            if any( word for word in cache[ "horny_responses" ] if word in content ):

                cache[ "horny_times" ] += 1;

                user: discord.User = await bot.fetch_user( 121735805369581570 ); # Kern

                webhook: discord.Webhook = await bot.webhook( message.channel );

                await webhook.send(
                    content='Control yourself. This is the {}th time.'.format( cache[ "horny_times" ] ),
                    username='KernCore',
                    avatar_url=user.avatar.url if user.avatar else None
                );

                g_Cache.SetTemporal( "control_arase_horny", timedelta( hours = 1 ) );

        return Hook.Continue;
