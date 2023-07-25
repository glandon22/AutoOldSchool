
import osrs
import datetime


def craft():
    data = osrs.server.get_skill_data('crafting')
    crafting_level = data['level']
    item_to_make = determine_item_to_make(crafting_level)
    inv = osrs.inv.get_inv()
    for item in inv:
        if item["id"] == 1785:
            osrs.move.move_and_click(item["x"], item["y"], 8, 8)
            break
    for item in inv:
        if item["id"] == 1775:
            osrs.move.move_and_click(item["x"], item["y"], 8, 8)
            break
    osrs.clock.random_sleep(.9, 1.2)
    osrs.keeb.keyboard.type(item_to_make)
    return crafting_level


def determine_item_to_make(lvl):
    if lvl < 4:
        return '1'
    elif lvl < 12:
        return '2'
    elif lvl < 33:
        return '3'
    elif lvl < 42:
        return '4'
    elif lvl < 46:
        return '5'
    elif lvl < 100:
        return '6'


def click_banker():
    q = {
        'npcs': ['Banker']
    }
    data = osrs.server.query_game_data(q)
    if len(data["npcs"]) != 0:
        closest = osrs.util.find_closest_npc(data['npcs'])
        osrs.move.move_and_click(closest['x'], closest['y'], 5, 6)


def main():
    start_time = datetime.datetime.now()
    while True:
        data = osrs.server.get_skill_data('crafting')
        crafting_level = data['level']
        click_banker()
        osrs.bank.wait_for_bank_interface()
        # dump everything other than my pipe
        inv = osrs.inv.get_inv()
        for item in inv:
            if item['id'] != 1785:
                osrs.move.move_and_click(item['x'], item['y'], 5, 5)
                break
        bank = osrs.bank.get_bank_data()
        found = False
        for item in bank:
            if item["id"] == 1775:
                found = True
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
        osrs.keeb.keyboard.press(osrs.keeb.Key.esc)
        osrs.keeb.keyboard.release(osrs.keeb.Key.esc)
        if not found:
            osrs.game.logout()
            print('out of glass')
            return

        osrs.clock.random_sleep(0.9, 1.1)
        craft()
        while True:
            data = osrs.server.get_player_info(8814)
            found = False
            for item in data["inv"]:
                if item["id"] == 1775:
                    found = True
                    break
            if not found:
                break
            elif data['craftingLevel'] != crafting_level:
                craft()
                crafting_level = data['craftingLevel']


def complete_inv_on_login(port):
    inv = osrs.inv.get_inv(port)
    glass = osrs.inv.is_item_in_inventory_v2(inv, 1775)
    if glass:
        craft()


def blow_glass(crafting_lvl):
    inv = osrs.inv.get_inv()
    have_molten_glass = osrs.inv.is_item_in_inventory_v2(inv, 1775)
    if not have_molten_glass:
        click_banker()
        osrs.bank.wait_for_bank_interface()
        found = True
        while found:
            found = False
            inv = osrs.inv.get_inv()
            for item in inv:
                if item['id'] != 1785:
                    osrs.move.move_and_click(item['x'], item['y'], 5, 5)
                    osrs.clock.random_sleep(0.6, 0.7)
                    found = True
                    break
        bank = osrs.bank.get_bank_data()
        found = False
        for item in bank:
            if item["id"] == 1775:
                found = True
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
        osrs.keeb.keyboard.press(osrs.keeb.Key.esc)
        osrs.keeb.keyboard.release(osrs.keeb.Key.esc)
        if not found:
            return print('out of glass')
        osrs.clock.random_sleep(0.8, 0.9)
        return craft()
    # handle leveling
    elif crafting_lvl != osrs.server.get_skill_data('crafting'):
        return craft()

main()
