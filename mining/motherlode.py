'''
query for i1 and i2 squares
q = {
    'tiles': ['3748,5655,0', '3737,5652,0']
}

query for game objects

'''
import keyboard

import osrs

ores = [
    453,  # coal
    444,  # gold
    447,  # mith
    449,  # addy
    451  # rune
]


def click_i1():
    q = {
        'tiles': ['3748,5655,0']
    }
    while True:
        data = osrs.server.query_game_data(q)
        if 'tiles' in data and '374856550' in data['tiles']:
            osrs.move.move_and_click(data['tiles']['374856550']['x'], data['tiles']['374856550']['y'], 7, 7)
            break


def walk_to_i2_sq():
    q = {
        'tiles': ['3737,5652,0']
    }
    while True:
        data = osrs.server.query_game_data(q)
        # since i am so zoomed out, things at the top of the screen arent fully loaded and may not be clickable
        # so, i wait until the square gets closer to assure that it is loaded
        if 'tiles' in data and '373756520' in data['tiles'] and data['tiles']['373756520']['y'] > 150:
            osrs.move.move_and_click(data['tiles']['373756520']['x'], data['tiles']['373756520']['y'], 7, 7)
            break


def navigate_rockfall():
    q = {
        'tiles': ['3727,5652,0']
    }
    data = osrs.server.query_game_data(q)
    rft = data['tiles']['372756520']
    osrs.move.move_and_click(rft['x'], rft['y'], 10, 10)
    # once rockfall is cleared, click on i2 square
    while True:
        q = {
            'tiles': [
                '3727,5652,0',  # rock fall tile
                '3737,5652,0',  # i2
            ],
            'gameObjects': [
                '26680'  # rock fall object
            ]
        }
        data = osrs.server.query_game_data(q)
        if '26680' not in data['gameObjects']:
            if '373756520' in data['tiles']:
                osrs.move.move_and_click(data['tiles']['373756520']['x'], data['tiles']['373756520']['y'], 6, 6)
                break
            else:
                rft = data['tiles']['372756520']
                osrs.move.move_and_click(rft['x'], rft['y'], 10, 10)


def pass_rockfall_to_mine_veins():
    saved_i2_coords = {
        'x': 0,
        'y': 0
    }
    q = {
        'tiles': ['3737,5652,0']
    }
    while True:
        data = osrs.server.query_game_data(q)
        curr_i2_coords = data['tiles']['373756520']
        if curr_i2_coords['x'] == saved_i2_coords['x']:
            break
        else:
            saved_i2_coords = {
                'x': curr_i2_coords['x'],
                'y': curr_i2_coords['y']
            }

    q = {
        'tiles': [
            '3727,5652,0'  # rock fall tile
        ]
    }
    data = osrs.server.query_game_data(q)
    rft = data['tiles']['372756520']
    osrs.move.move_and_click(rft['x'], rft['y'], 10, 10)
    # once rockfall is cleared, click on i2 square
    while True:
        q = {
            'gameObjects': [
                '26680'  # rock fall object
            ]
        }
        data = osrs.server.query_game_data(q)
        if '26680' not in data['gameObjects']:
            # need to figure out this query, in the wall object logic of the java code i also need to check to make sure i am looking for the object passed in not just ore veins
            q = {
                'wallObjects': [
                    {
                        'tile': '3720,5654,0',
                        'object': '26662'
                    }
                ]
            }
            if 'oreVeins' in data:
                data = osrs.server.get_player_info(2223)
                closest = osrs.util.find_closest_npc(data['oreVeins'])
                osrs.move.move_and_click(closest['x'], closest['y'], 6, 6)
                osrs.move.click_off_screen(click=False)
                break
            else:
                rft = data['rockfallTile']
                osrs.move.move_and_click(rft['x'], rft['y'], 10, 10)


def should_collect_ore(data):
    ore_in_inv = 0
    for item in data['inv']:
        if item['id'] == 12011:
            ore_in_inv += 1
    return ore_in_inv + data['oreCount'] > 80


def bank_and_return():
    # Click on square containing the rockfall
    navigate_rockfall()
    # after i2, click to i1
    click_i1()
    osrs.clock.random_sleep(0.9, 1.1)
    saved_ore_cart_coords = {
        'x': 0,
        'y': 0
    }
    # deposit pay dirt
    while True:
        data = osrs.server.get_player_info(2223)
        curr_ore_cart_coords = data['oreCart']
        if curr_ore_cart_coords['x'] == saved_ore_cart_coords['x']:
            osrs.move.move_and_click(curr_ore_cart_coords['x'], curr_ore_cart_coords['y'], 4, 4)
            break
        else:
            saved_ore_cart_coords = {
                'x': curr_ore_cart_coords['x'],
                'y': curr_ore_cart_coords['y']
            }
    should_collect_decision = should_collect_ore(data)
    # wait until everything is deposited
    while True:
        data = osrs.server.get_player_info(2223)
        pay_dirt_present = False
        for item in data['inv']:
            if item['id'] == 12011:
                pay_dirt_present = True
                break
        if not pay_dirt_present:
            break
    if should_collect_decision:
        #collect ore from ore sack until empty
        osrs.clock.random_sleep(0.7, 0.9)
        while True:
            while True:
                data = osrs.server.get_player_info(2223)
                if 'oreSack' in data:
                    osrs.move.move_and_click(data['oreSack']['x'], data['oreSack']['y'], 3, 3)
                    break
            while True:
                data = osrs.server.get_player_info(2223)
                if 'inv' in data and len(data['inv']) != 0 and 'bank' in data:
                    have_ore = False
                    for item in data['inv']:
                        if item['id'] in ores:
                            have_ore = True
                            break
                    if have_ore:
                        osrs.clock.random_sleep(0.7, 0.9)
                        data = osrs.server.get_player_info(2223)
                        osrs.move.move_and_click(data['bank']['x'],data['bank']['y'], 5, 5)
                        break
            osrs.bank.bank_dump_inv()
            data = osrs.server.get_player_info(2223)
            if data['oreCount'] == 0:
                break
        click_i1()
    # walk to i2
    osrs.clock.random_sleep(1.4, 1.8)
    walk_to_i2_sq()
    osrs.clock.random_sleep(1.7, 1.8)
    # pass the rock fall
    pass_rockfall_to_mine_veins()


def main():
    # the mining animation will go to false for two ticks even though im mining
    # so i need to make sure im actually not mining
    not_mining_count = 0
    while True:
        data = osrs.server.get_player_info(2223)
        if 'inv' in data and len(data['inv']) == 28:
            bank_and_return()
        elif not_mining_count > 5:
            closest = osrs.util.find_closest_npc(data['oreVeins'])
            osrs.move.move_and_click(closest['x'], closest['y'], 6, 6)
            osrs.move.click_off_screen(click=False)
            not_mining_count = 0
        elif not data['isMining']:
            not_mining_count += 1
        elif data['isMining']:
            not_mining_count = 0


#main()
navigate_rockfall()