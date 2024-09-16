'''
run to 2216,2842,0
enter arena
wall obj 41200 on 2220,2842,0
both challenge eachother
widget id 492,6 to confirm game, both must click
determine side!!!
blue portal - 40460 'Leave'
    red portal - 40461

anchor 2135,2905
    red 2279, 2919

cap 2 2253, 2920
    red: 2161, 2903


red bandage table 40463
blue bandage table 40462
widget to take bandage 270,13

obelisk
40449 uncapped - blue capped 40450 - red capped 40451
'''
import datetime

import osrs
import osrs.queryHelper

red_table_id = 40463
blue_table_id = 40462
partner = 'UtahDogs'


def wait_for_game():
    osrs.dev.logger.info('Waiting to enter the game arena.')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') > 4000:
            osrs.dev.logger.info('I am in the game arena.')
            break


def in_game():
    osrs.dev.logger.info('Waiting to enter the game arena.')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('x') > 4000:
        osrs.dev.logger.info('I am in the game arena.')
        return True


def determine_side():
    osrs.dev.logger.info('Determining which side of the game arena I am on.')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {red_table_id, blue_table_id})
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game', red_table_id):
            osrs.dev.logger.info('I am playing as red.')
            return 'red'
        elif qh.get_objects_v2('game', blue_table_id):
            osrs.dev.logger.info('I am playing as blue.')
            return 'blue'


def determine_anchor(side):
    osrs.dev.logger.info('Determing anchor tile.')
    red_exit = 40457
    blue_exit = 40454
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {red_exit, blue_exit})
    while True:
        qh.query_backend()
        walls = qh.get_objects_v2('wall')
        if walls:
            # there are three portals on each side, we want to portal in the middle
            walls = sorted(walls, key=lambda wall_obj: wall_obj['x_coord'], reverse=side == 'red')
            anchor = {'x': walls[0]['x_coord'], 'y': walls[0]['y_coord']}
            osrs.dev.logger.info('Found anchor tile: %s', anchor)
            return anchor


def exit_starting_area(side, anchor):
    id_lookup = {
        'red': 40457,
        'blue': 40454
    }
    osrs.dev.logger.info('Exiting starting area on %s side', side)
    osrs.move.interact_with_object(
        id_lookup[side], 'x', anchor['x'], side == 'red', obj_type='wall', right_click_option='Pass',
        obj_tile={'x': anchor['x'], 'y': anchor['y'], 'z': 0}, timeout=7
    )


def kill_ghost():
    osrs.dev.logger.info('Searching  for a ghost to kill..')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['forgotten soul'])
    qh.set_interating_with()
    loot = osrs.loot.Loot()
    qh.set_inventory()
    while True:
        loot.retrieve_loot(10)
        qh.query_backend()
        if qh.get_inventory(
                [osrs.item_ids.ItemIDs.SOUL_FRAGMENT.value, osrs.item_ids.ItemIDs.SOUL_FRAGMENT_25201.value]
        ):
            osrs.dev.logger.info('I have a soul fragment.')
            return
        elif qh.get_npcs_by_name() and not qh.get_interating_with():
            osrs.dev.logger.info('Attacking a ghost.')
            c = osrs.util.find_closest_alive_npc(qh.get_npcs_by_name())
            if c:
                osrs.move.fast_click(c)
        elif qh.get_interating_with():
            osrs.dev.logger.info('In combat with a ghost.')
        osrs.keeb.press_key('space')


def run_to_ghosts(side, anchor):
    osrs.dev.logger.info('Running to kill a ghost.')
    side_lookup = {
        'blue': {
            'x': 20,
            'y': 21
        },
        'red': {
            'x': -24,
            'y': -21
        }
    }
    steps = osrs.move.run_towards_square(
        {'x': anchor['x'] + side_lookup[side]['x'], 'y': anchor['y'] + side_lookup[side]['y'], 'z': 0},
        steps_only=True
    )
    osrs.dev.logger.info('Generated a path to the ghosts.')
    osrs.move.fixed_follow_path(steps)
    osrs.dev.logger.info('Arrived at ghosts.')


def run_to_center(side, anchor):
    '''
    anchor 2135,2905
        red 2279, 2919
    center 2205, 2911
        red: 2208, 2911
    '''
    osrs.dev.logger.info('Running to capture central obelisk.')
    lookup = {
        'blue': {
            'x': 70,
            'y': 6
        },
        'red': {
            'x': -71,
            'y': -8
        }
    }
    steps = osrs.move.run_towards_square(
        {'x': anchor['x'] + lookup[side]['x'], 'y': anchor['y'] + lookup[side]['y'], 'z': 0},
        steps_only=True
    )
    osrs.dev.logger.info('Generated a path to the central obelisk.')
    osrs.move.fixed_follow_path(steps)
    osrs.dev.logger.info('Arrived at central obelisk.')


def start_game():
    osrs.move.go_to_loc(2219, 2842)
    osrs.move.interact_with_object(41200, 'x', 2220, True, obj_type='wall')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_players()
    qh.set_widgets({'492,6'})
    qh.set_canvas()
    last_challenge = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_accept = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if in_game():
            return
        elif qh.get_widgets('492,6'):
            if (datetime.datetime.now() - last_accept).total_seconds() > 5:
                osrs.move.click(qh.get_widgets('492,6'))
                last_accept = datetime.datetime.now()
        elif qh.get_players() and (datetime.datetime.now() - last_challenge).total_seconds() > 5:
            partner_loc = list(
                filter(
                    lambda player: player['name'].lower() == partner.lower() and 2220 <= player['worldPoint']['x'] <= 2229,
                    qh.get_players()
                )
            )
            if partner_loc:
                res = osrs.move.right_click_v6(
                    partner_loc[0],
                    'Challenge',
                    qh.get_canvas(),
                    in_inv=True
                )
                if res:
                    last_challenge = datetime.datetime.now()

def get_first_capture(side, anchor):
    lookup = {
        'red': {
            'x': -27,
            'y': 1,
            'id': 40455
        },
        'blue': {
            'x': 26,
            'y': -3,
            'id': 40453
        }
    }
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {lookup[side]['id']})
    steps = osrs.move.run_towards_square(
        {'x': anchor['x'] + lookup[side]['x'], 'y': anchor['y'] + lookup[side]['y'], 'z': 0},
        steps_only=True
    )
    osrs.dev.logger.info('Generated a path to the first cemetery.')
    osrs.move.fixed_follow_path(steps)
    osrs.dev.logger.info('Arrived at first cemetery, capturing.')
    osrs.dev.logger.info('Looking for id %s to verify capture.', lookup[side]['id'])
    while True:
        qh.query_backend()
        if qh.get_objects_v2('wall'):
            osrs.dev.logger.info('Captured cemetery 1.')
            return


def used_frags():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory([
        osrs.item_ids.ItemIDs.SOUL_FRAGMENT.value,
        osrs.item_ids.ItemIDs.SOUL_FRAGMENT_25201.value,
    ]):
        return True


def capture_center(side):
    lookup = {
        'red': {
            'id': 40451
        },
        'blue': {
            'id': 40450
        }
    }
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {lookup[side]['id']})
    osrs.dev.logger.info('Looking for id %s to verify capture.', lookup[side]['id'])
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game'):
            osrs.dev.logger.info('Captured central obelisk.')
            return


def get_second_capture(side, anchor):
    '''
    this isnt going to the right place. its too far above the cemetery
    anchor 2135,2905
        red 2279, 2919

    cap 2 2253, 2920
        red: 2161, 2903

        '''
    lookup = {
        'red': {
            'x': -118,
            'y': -16,
            'id': 40456
        },
        'blue': {
            'x': 118,
            'y': 15,
            'id': 40452
        }
    }
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {lookup[side]['id']})
    steps = osrs.move.run_towards_square(
        {'x': anchor['x'] + lookup[side]['x'], 'y': anchor['y'] + lookup[side]['y'], 'z': 0},
        steps_only=True
    )
    osrs.dev.logger.info('Generated a path to the first cemetery.')
    osrs.move.fixed_follow_path(steps)
    osrs.dev.logger.info('Arrived at first cemetery, capturing.')
    osrs.dev.logger.info('Looking for id %s to verify capture.', lookup[side]['id'])
    while True:
        qh.query_backend()
        if qh.get_objects_v2('wall'):
            osrs.dev.logger.info('Captured cemetery 1.')
            return


def main_active():
    while True:
        start_game()
        side = determine_side()
        anchor = determine_anchor(side)
        exit_starting_area(side, anchor)
        osrs.dev.logger.info('Exited starting area.')
        run_to_ghosts(side, anchor)
        kill_ghost()
        get_first_capture(side, anchor)
        run_to_center(side, anchor)
        # use soul frags on obelisk
        osrs.move.interact_with_object(
            40449, 'z', 3, True, custom_exit_function=used_frags
        )
        capture_center(side)
        get_second_capture(side, anchor)


def game_over(widgets):
    if not widgets or type(widgets) is not dict:
        return False
    for widget in widgets:
        osrs.dev.logger.info('Widget size: %s', widgets[widget]['xMax'] - widgets[widget]['xMin'])
        if widgets[widget]['xMax'] - widgets[widget]['xMin'] not in [0, 32]:
            return False
    return True


def leave_game():
    exit_portals = {}
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', exit_portals)


def main_passive():
    c1 = '375,28,0'
    c2 = '375,33,0'
    c3 = '375,38,0'
    bandage_tables = {40463, 40462}
    take_bandage_widget = '270,13'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({c1, c2, c3, take_bandage_widget})
    qh.set_objects_v2('game', bandage_tables)
    last_bandage_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        start_game()
        while True:
            qh.query_backend()
            if qh.get_widgets(take_bandage_widget):
                osrs.dev.logger.info('Being prompted to take a bandage.')
                osrs.keeb.press_key('space')
            elif qh.get_objects_v2('game') and (datetime.datetime.now() - last_bandage_click).total_seconds() > 15:
                osrs.dev.logger.info('Taking a bandage.')
                osrs.move.click(qh.get_objects_v2('game')[0])
                last_bandage_click = datetime.datetime.now()
            elif game_over(qh.get_widgets()):
                osrs.dev.logger.info('Active player captured both sides, forfeiting.')
                osrs.move.interact_with_multiple_objects(
                    {40460, 40461}, 'x', 4000, False, right_click_option='Leave',
                    pre_interact=lambda: osrs.keeb.write('1'), timeout=1
                )
                break


#main_active()
main_passive()