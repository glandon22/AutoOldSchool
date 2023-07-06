import datetime

import osrs


def main():
    item_locs = {
        'first': None,
        'second': None,
        'third': None
    }
    saved_spot = {
        'spot': None,
        'updated': datetime.datetime.now() - datetime.timedelta(hours=1)
    }
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_npcs(['1542'])
    qh.set_is_fishing()
    qh.query_backend()
    for item in qh.get_inventory():
        if item['index'] == 0:
            item_locs['first'] = {'x': item['x'], 'y': item['y']}
            item_locs['second'] = {'x': item['x'], 'y': item['y'] + 36}
            item_locs['third'] = {'x': item['x'], 'y': item['y'] + 72}
    while True:
        qh.query_backend()
        closest_fishing_spot = qh.get_npcs()
        closest_fishing_spot = osrs.util.find_closest_target(closest_fishing_spot)
        if closest_fishing_spot and closest_fishing_spot['dist'] == 1:
            print('here', closest_fishing_spot, saved_spot['spot'])
            print((datetime.datetime.now() - saved_spot['updated']).total_seconds() > 1)
            if saved_spot['spot'] \
                    and saved_spot['spot']['x'] == closest_fishing_spot['x'] \
                    and saved_spot['spot']['y'] == closest_fishing_spot['y']:
                if (datetime.datetime.now() - saved_spot['updated']).total_seconds() > 1:
                    osrs.move.click(item_locs['first'])
                    osrs.clock.random_sleep(0.75, 0.81)
                    osrs.move.click(item_locs['second'])
                    osrs.move.click(item_locs['third'])
                    for i in range(2, 4):
                        osrs.move.fast_click(closest_fishing_spot)
            else:
                saved_spot['spot'] = closest_fishing_spot
                saved_spot['updated'] = datetime.datetime.now()
        elif closest_fishing_spot and closest_fishing_spot['dist'] > 1:
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            while True:
                qh.query_backend()
                if qh.get_is_fishing():
                    break
                elif (datetime.datetime.now() - last_click).total_seconds() > 8:
                    closest_fishing_spot = qh.get_npcs()
                    closest_fishing_spot = osrs.util.find_closest_target(closest_fishing_spot)
                    osrs.move.click(closest_fishing_spot)
                    last_click = datetime.datetime.now()
                    saved_spot['spot'] = closest_fishing_spot
                    saved_spot['updated'] = last_click

main()
