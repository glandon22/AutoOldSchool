# rubble to descend 43724 3634,9503,0
# large guardian remains 43719 3640,9498,0 not sure if this is an instance yet
# rubble to ascend 43726 3636,9503,0
# east big orb 43729 <- think this is always the same
# orb to leave 38044
import datetime

# active body portal 43709
# body altar 34765
# body exit portal 34753

# nature portal 43711
# altar 34768
# exit 34756

# mind portal 43705
# altar 34761
# exit 34749


# huge guardian remains 43720

# great guardin npc 11403

# rune deposit pool 43696

# workbench 43754

# widget container for portal orb thats 25 seconds 746,26
# 746,28 contains the text to find where it is

# open elemental altar 746,20
# open cata altar 746,23

# portal you can pass thru to start game 43700

from osrs_utils import general_utils

port = '56799'
frag_portal_dict = {
    'S': {'x': 3615, 'y': 9490, 'z': 0},
    'E': {'x': 3628, 'y': 9499, 'z': 0},
    'SE': {'x': 3623, 'y': 9495, 'z': 0},
    'SW': {'x': 3607, 'y': 9492, 'z': 0}
}


sprite_to_rift_obj_dict = {
    '4353': { # air
        'tile': '3617,9494,0',
        'id': '43701'
    },
    '4359' : { # cosmic
        'tile': '3621,9496,0',
        'id': '43710'
    },
    '4355' : { # water
        'tile': '3623,9500,0',
        'id': '43702'
    },
    '4356' : { # earth
        'tile': '3623,9505,0',
        'id': '43703'
    },
    '4361' : { # nat
        'tile': '3621,9509,0',
        'id': '43711'
    },
    '4357' : { # fire
        'tile': '3617,9511,0',
        'id': '43704'
    },
    '4364' : { # blood
        'tile': '3612,9511,0',
        'id': '43708'
    },
    '4362' : { # law
        'tile': '3609,9510,0',
        'id': '43712'
    },
    '4363' : { # death
        'tile': '3607,9506,0',
        'id': '43707'
    },
    '4360' : { # chaos
        'tile': '3607,9501,0',
        'id': '43706'
    },
    '4358' : { # body
        'tile': '3609,9497,0',
        'id': '43709'
    },
    '4354' : { # mind
        'tile': '3612,9495,0',
        'id': '43705'
    }
}

def in_main_arena():
    loc = general_utils.get_world_location(port)
    if loc and 'x' in loc and 3597 <= loc['x'] <= 3633 and 'y' in loc and 9484 <= loc['y'] <= 9519:
        return True
    else:
        return False


def run_to_large_remains():
    beginning = general_utils.get_widget('746,23')
    if beginning and 'spriteID' in beginning and beginning['spriteID'] == 4369:
        loc = general_utils.get_world_location(port)
        if 'x' in loc and loc['x'] <= 3633:
            # need my if clause here, search if guardian is asleep?
            obstacle = general_utils.get_ground_object('3634,9503,0', '43724', port)
            if bool(obstacle):
                general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
                general_utils.sleep_one_tick()
                general_utils.wait_until_stationary(port)
            else:
                general_utils.run_towards_square_v2('3626,9500,0', port)


def mine_large_remains():
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    if 'x' in loc and loc['x'] >= 3637 and \
            (not guardian_frags or guardian_frags and guardian_frags['quantity'] < 180) \
            and not general_utils.is_mining(port):
        rock = general_utils.get_game_object('3640,9498,0', '43719', port)
        if rock:
            general_utils.move_and_click(rock['x'], rock['y'], 3, 3)


def leave_large_remains_area():
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    beginning = general_utils.get_widget('746,23')
    if 'x' in loc and loc['x'] >= 3637 and \
            guardian_frags and guardian_frags['quantity'] > 180 \
            and beginning and 'spriteID' in beginning and beginning['spriteID'] != 4369:
        obstacle = general_utils.get_ground_object('3636,9503,0', '43726', port)
        if obstacle:
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.sleep_one_tick()


def frag_port_available():
    portal_text = general_utils.get_widget('746,28', port)
    loc = general_utils.get_world_location(port)
    if portal_text and loc and 'x' in loc and 3597 <= loc['x'] <= 3633:
        text_parts = portal_text['text'].split(' - ')
        if len(text_parts) >= 2 and text_parts[1] != '0:00':
            print('b', text_parts[0])
            general_utils.run_towards_square_v2(frag_portal_dict[text_parts[0]], port)
            orb = general_utils.get_surrounding_game_objects(10, ['43729'], port)
            if orb and '43729' in orb:
                general_utils.move_and_click(orb['43729']['x'], orb['43729']['y'], 1, 1)
                general_utils.sleep_one_tick()
                general_utils.wait_until_stationary(port)


def mine_huge_remains():
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    if loc and 'x' in loc and loc['x'] <= 3594 and len(inv) < 28 and not general_utils.is_mining(port):
        remains = general_utils.get_surrounding_game_objects(8, ['43720'], port)
        if remains and '43720' in remains:
            general_utils.move_and_click(remains['43720']['x'], remains['43720']['y'], 3, 3)


def leave_huge_remains():
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    if loc and 'x' in loc and loc['x'] <= 3594 and len(inv) == 28:
        remains = general_utils.get_surrounding_game_objects(8, ['38044'], port)
        if remains and '38044' in remains:
            general_utils.move_and_click(remains['38044']['x'], remains['38044']['y'], 3, 3)


def make_essence():
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if loc and 'x' in loc and 3597 <= loc['x'] <= 3633 and guardian_frags and not guardian_ess:
        work_table = general_utils.get_surrounding_game_objects(10, ['43754'], port)
        if not bool(work_table):

            general_utils.run_towards_square_v2({'x': 3615, 'y': 9492, 'z': 0}, port)
            work_table = general_utils.get_surrounding_game_objects(10, ['43754'], port)
        general_utils.move_and_click(work_table['43754']['x'], work_table['43754']['y'], 3, 3)
        if int(general_utils.get_target_obj(port)) == 43754:
            start_time = datetime.datetime.now()
            while True:
                curr_inv = general_utils.get_inv(port)
                if len(curr_inv) == 28 or \
                        not general_utils.is_item_in_inventory_v2(inv, 26878) or \
                        (datetime.datetime.now() - start_time).total_seconds() > 15:
                    break


def enter_active_rift():
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_main_arena() and guardian_ess:
        active_catalytic_rift = general_utils.get_widget('746,23')
        if active_catalytic_rift and 'spriteID' in active_catalytic_rift:
            rift_to_enter = sprite_to_rift_obj_dict[str(active_catalytic_rift['spriteID'])]
            print('ll', rift_to_enter)

general_utils.random_sleep(1, 2)
while True:
    run_to_large_remains()
    mine_large_remains()
    leave_large_remains_area()
    frag_port_available()
    mine_huge_remains()
    leave_huge_remains()
    make_essence()
# main game cooards: x: 3597 - 3633
# main game cooards: y - 9484 - 9519
# 26879 guardian essence
# elemental guardian stone 26881