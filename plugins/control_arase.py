from src.main import *
from src.PluginManager import Plugin;

class control_arase( Plugin ):

    @property
    def GetDescription(self):
        return "Control arase";

    control_yourself = (
        'mommy',
        'mama',
        'sex',
        'gf',
        'feet',
        'armpit',
    );

    mimir_texts = (
        "What the fuck arase go to sleep",
        "Go to fucking sleep arase",
        "Ok but go to sleep",
        "when sleeping",
        "Mimir time mf",
        "You ain't going to find a girlfriend at this time,"
        "Reminder para arase to fucking sleep early"
    );

    async def OnMessage(self, message):

        if message.author.id == bot.user.id:
            return True;

        if message.author.id in [ 768337526888726548, 1312014737449549826 ]:
        
            if g_Cache.GetTemporal( "control_arase_mimido" )[0] != TemporalCache.Exists:

                hour = datetime.now( pytz.timezone( "Asia/Kuala_Lumpur" ) ).hour;

                if hour <= 5:

                    if random.randint( 0, 1 ) == 1:

                        g_Cache.SetTemporal( "control_arase_mimido", timedelta( hours = ( 6 - hour ) ) );

                        user = await bot.fetch_user( 438449162527440896 ); # Kez

                        webhook = await bot.webhook( message.channel );

                        if hour == 0:
                            hour = f' It\'s 12 PM.';
                        else:
                            hour = f' It\'s {hour} AM.';

                        mimir_text = self.mimir_texts[ random.randint( 0, len(self.mimir_texts) - 1 ) ] + hour;

                        await webhook.send( content=f'{mimir_text} [a mimir](https://cdn.discordapp.com/attachments/847485688282480640/1376229990378508398/a_mimir.mp4?ex=6834918e&is=6833400e&hm=ea97d291d22f7a0dbc723032baee9ce6d4e195e112913df24b786cfb9e697e2a&)', username='KEZÆIV', avatar_url=user.avatar.url if user.avatar else None );

            if g_Cache.GetTemporal( "control_arase_horny" )[0] != TemporalCache.Exists:

                content = message.content.lower();

                if any( word for word in self.control_yourself if word in content ):

                    cache = g_Cache.Get();

                    number = cache.get( "times", 0 );

                    number += 1;

                    cache[ "times" ] = number;

                    user = await bot.fetch_user( 121735805369581570 ); # Kern

                    webhook = await bot.webhook( message.channel );

                    await webhook.send( content=f'Control yourself. This is the {number}th time.', username='KernCore', avatar_url=user.avatar.url if user.avatar else None );

                    g_Cache.SetTemporal( "control_arase_horny", timedelta( hours = 1 ) );

        return True;
