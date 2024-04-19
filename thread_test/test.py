import datetime

import osrs
from threading import Thread, Event

game_state = osrs.queryHelper.QueryHelper()


def hit_server(gs: osrs.queryHelper.QueryHelper):
    calls = 0
    latency = 0
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_npcs(['1325'])
    while True:
        s = datetime.datetime.now()
        gs.game_data = qh.query_backend()
        calls += 1
        latency += (datetime.datetime.now() - s).total_seconds()
        print(f'avg latency: {latency / calls}')
        if calls > 1000:
            exit()


t = Thread(target=hit_server, args=(game_state,))
t.start()

while True:
    if 'npcs' in game_state:
        continue


'''
IMPORTANT:
 this shows you the upper left most bound of the client on screen
 
 client.getCanvas().getLocationOnScreen()


'''