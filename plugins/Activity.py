from plugins.main import *

hooks = [
    Hooks.on_think
];

RegisterHooks( plugin_name='Activity', hook_list=hooks );

Activity_Time = 0
Activity_Interval = config[ "Activity" ][ "IntervalUpdate" ]
Listening = config[ "Activity" ][ "Listening to" ]
State = config[ "Activity" ][ "State" ]
LastState = 1
LastListening = 1

async def on_think():

    global Activity_Time
    global Activity_Interval
    global Listening
    global LastListening
    global State
    global LastState

    if Activity_Time < gpGlobals.time:

        if LastState > len( State ):
            LastState = 1

        if LastListening > len( Listening ):
            LastListening = 1

        Activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=Listening[ LastListening - 1 ],
            state=State[ LastState - 1 ],
        )

        await bot.change_presence( activity = Activity )

        LastState += 1
        LastListening = +1

        Activity_Time = gpGlobals.time + Activity_Interval
