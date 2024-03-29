import datetime
import osrs

BOWSTRING = 1777
# 66 yew long
# 70 mage long
# 62 maple long
# 64 maple short
UNSTRUNG_BOW = 66


def string():
    q = {
        'inv': True
    }
    data = osrs.server.query_game_data(q)
    for item in data["inv"]:
        if item["id"] == 1777:
            osrs.move.move_and_click(item["x"], item["y"], 8, 8)
            break
    for item in data["inv"]:
        if item["id"] == UNSTRUNG_BOW:
            osrs.move.move_and_click(item["x"], item["y"], 8, 8)
            break
    osrs.clock.random_sleep(.9, 1.2)
    osrs.keeb.keyboard.press(osrs.keeb.key.space)
    osrs.keeb.keyboard.release(osrs.keeb.key.space)


def click_banker():
    q = {
        'npcs': ['Banker']
    }
    data = osrs.server.query_game_data(q)
    if len(data["npcs"]) != 0:
        closest = osrs.util.find_closest_npc(data['npcs'])
        osrs.move.move_and_click(closest['x'], closest['y'], 5, 6)


def dump_inventory_in_bank():
    q = {
        'inv': True
    }
    data = osrs.server.query_game_data(q)
    if 'inv' in data and len(data['inv']) > 0:
        print('Dumping inventory.')
        q = {
            'dumpInvButton': True
        }
        while True:
            data = osrs.server.query_game_data(q)
            if 'dumpInvButton' in data:
                center = data['dumpInvButton']
                osrs.move.move_and_click(center['x'], center['y'], 10, 10)
                osrs.clock.random_sleep(.5, .6)
                break


def withdraw_materials():
    found_unstrung = False
    found_bowstring = False
    while True:
        data = osrs.bank.get_bank_data()
        for item in data:
            if item["id"] == UNSTRUNG_BOW:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                found_unstrung = True
            elif item["id"] == BOWSTRING:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                found_bowstring = True
        osrs.keeb.keyboard.press(osrs.keeb.key.esc)
        osrs.keeb.keyboard.release(osrs.keeb.key.esc)
        break
    if not found_bowstring or not found_unstrung:
        print(data)
        exit("no more unstrung bows or bowstrings")
    osrs.clock.random_sleep(0.9, 1.1)


def get_fletching_level():
    q = {
        'skills': ['fletching']
    }
    data = osrs.server.query_game_data(q)
    return data['skills']['fletching']['level']


def main():
    fletching_level = get_fletching_level()
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 53, 58, 345, 567, 'julenth', False)
        print('Clicking on banker.')
        click_banker()
        print('Waiting for bank interface to open.')
        osrs.clock.random_sleep(1.1, 1.3)
        dump_inventory_in_bank()
        print('Withdrawing fletching materials.')
        withdraw_materials()
        print('Stringing bows.')
        string()
        start_stringing = datetime.datetime.now()
        while True:
            # Throttle calls to the backend slightly
            osrs.clock.random_sleep(0.025, 0.026)
            q = {
                'skills': ['fletching'],
                'inv': True
            }
            data = osrs.server.query_game_data(q)
            if 'inv' in data and not osrs.inv.are_items_in_inventory(data['inv'], [BOWSTRING, UNSTRUNG_BOW]):
                print('Bag completed stringing.')
                break
            elif data['skills']['fletching']['level'] != fletching_level or \
                    (datetime.datetime.now() - start_stringing).total_seconds() > 17:
                print('Leveled fletching. Stringing again.')
                fletching_level = data['skills']['fletching']['level']
                start_stringing = datetime.datetime.now()
                string()


main()

