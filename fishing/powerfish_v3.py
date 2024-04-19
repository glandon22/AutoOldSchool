import datetime
from threading import Thread
import osrs
import sys


fish_to_catch_config = {
    '1': 'shrimp',
    '2': 'salmon',
    '3': 'shark',
    '4': 'monkfish',
    '5': 'lobster',
    '6': 'tuna',
    '7': 'barbarian'
}

fish_to_catch = fish_to_catch_config['1']

if str(sys.argv[1]):
    fish_to_catch = str(sys.argv[1]).lower()

print('333', fish_to_catch, 'iiii', sys.argv[1])

fish_spot_ids = {
    'shrimp': [
        '1514',
        '1517',
        '1518',
        '1521',
        '1523',
        '1524',
        '1525',
        '1528',
        '1530',
        '1544',
        '3913',
        '7155',
        '7459',
        '7462',
        '7467',
        '7469',
        '7947',
        '10513'
    ],
    'salmon': [
        '394',
        '1506',
        '1507',
        '1508',
        '1509',
        '1513',
        '1515',
        '1516',
        '1526',
        '1527',
        '3417',
        '3418',
        '7463',
        '7464',
        '7468',
        '8524'
    ],
    'barbarian': ['1542']
}

fish_to_drop_ids = {
    'shrimp': [
        317, 321
    ],
    'salmon': [
        335,
        331
    ],
    'barbarian': [
            11328,
            11330,
            11332
        ]
}

game_state = osrs.queryHelper.QueryHelper()


def query_server(gs: osrs.queryHelper.QueryHelper):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_npcs(fish_spot_ids[fish_to_catch])
    qh.set_is_fishing()
    qh.set_canvas()
    while True:
        gs.game_data = qh.query_backend()


t = Thread(target=query_server, args=(game_state,))
t.start()


script_config = {
    'intensity': 'low',
    'login': lambda: osrs.clock.random_sleep(3, 4),
    'logout': False
}


def main():
    last_spot_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4(script_config)
        if game_state.get_inventory() and len(game_state.get_inventory()) == 28:
            # salmon + trout = 335, 331
            # shrimp anchovie 317, 321
            # leaping trout 11328
            osrs.inv.power_drop(game_state.get_inventory(), [], fish_to_drop_ids[fish_to_catch])
        elif game_state.get_is_fishing():
            print('Currently fishing.')
            continue
        elif not game_state.get_is_fishing() and (datetime.datetime.now() - last_spot_click).total_seconds() > 15:
            print('not fishing')
            c = osrs.util.find_closest_target(game_state.get_npcs())
            if c:
                last_spot_click = datetime.datetime.now()
                osrs.move.click(c)

main()
