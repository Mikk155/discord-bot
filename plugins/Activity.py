"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from plugins.main import *

global Activity;

class Activity:
    data = gpUtils.jsonc( '{}Activity.json'.format( gpGlobals.absp() ) );
    interval = data[ "interval" ];
    name = data[ "name" ];
    states = data[ "state" ]
    time = 0;
    state = 1;
    type = data[ "type" ]

async def on_think():

    Think, Activity.time = gpGlobals.should_think( Activity.time, Activity.interval );

    if Think:

        Activity.state += 1;

        if Activity.state > len( Activity.data[ "state" ] ):
            Activity.state = 1;

        try:

            pActivity = discord.Activity(
                type = Activity.type,
                name = Activity.name,
                state = Activity.states[ Activity.state - 1 ],
            );

            await bot.change_presence( activity = pActivity );

        except:
            return Hook.Continue();

    return Hook.Continue();
