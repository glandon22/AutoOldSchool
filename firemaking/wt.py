import random
from datetime import datetime, timedelta

import osrs

# added 733 bc it is when i am lighting the brazier, this prevents me chopping logs and interrupting that action
expected_animations = [
    879, 877, 875, 873, 871, 869, 867, 8303, 2846, 24, 2117, 7264, 8324, 8778, 10071, 733
]

warmth_widget_id = '396,20'
wintertodt_status_widget_id = '396,26'
food = osrs.item_ids.CAKE
brazier = 29314
unlit_brazier = 29312
broken_brazier = 29313
tree = 29311
falling_snow_attack = 26690

food_ids = [
    osrs.item_ids.CAKE,
    osrs.item_ids._23_CAKE,
    osrs.item_ids.SLICE_OF_CAKE,
]


equipment = [
    {'id': osrs.item_ids.PYROMANCER_GARB, 'consume': 'Wear'},
    {'id': osrs.item_ids.PYROMANCER_ROBE, 'consume': 'Wear'},
    {'id': osrs.item_ids.PYROMANCER_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.HITPOINTS_CAPET, 'consume': 'Wear'},
    {'id': osrs.item_ids.PYROMANCER_HOOD, 'consume': 'Wear'},
    {'id': osrs.item_ids.WARM_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_AXE, 'consume': 'Wield'},
    {'id': [
            osrs.item_ids.GAMES_NECKLACE1,
            osrs.item_ids.GAMES_NECKLACE2,
            osrs.item_ids.GAMES_NECKLACE3,
            osrs.item_ids.GAMES_NECKLACE4,
            osrs.item_ids.GAMES_NECKLACE5,
            osrs.item_ids.GAMES_NECKLACE6,
            osrs.item_ids.GAMES_NECKLACE7,
            osrs.item_ids.GAMES_NECKLACE8,
        ],
        'consume': 'Wear'
    },
    {'id': osrs.item_ids.HAMMER},
    {'id': osrs.item_ids.TINDERBOX},
    {'id': osrs.item_ids.CAKE},
    {'id': osrs.item_ids.CAKE},
    {'id': osrs.item_ids.CAKE},
]


def start_function():
    osrs.game.slow_lumb_tele()
    osrs.move.go_to_loc(3208, 3211)
    osrs.move.interact_with_object_v3(
        14880, obj_type='ground', coord_type='y', coord_value=9000,
        greater_than=True, right_click_option='Climb-down', timeout=8
    )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'wt', 'items': equipment}]
    })
    osrs.game.games_tele('Wintertodt Camp')
    osrs.move.go_to_loc(1630, 3960)
    osrs.game.hop_worlds(to_world='307')
    osrs.move.interact_with_object_v3(
        29322, coord_type='y', coord_value=3968, greater_than=True
    )


def game_state_parser(qh: osrs.queryHelper.QueryHelper):
    status = {
        'warmth': None,
        'wintertodt': None,
        'next_game_in': None
    }
    if qh.get_widgets(warmth_widget_id) \
            and qh.get_widgets(warmth_widget_id)['text'] \
            and '%' in qh.get_widgets(warmth_widget_id)['text']:
        status['warmth'] = int(qh.get_widgets(warmth_widget_id)['text'].split(' ')[2][:-1])
    if qh.get_widgets(wintertodt_status_widget_id) \
            and qh.get_widgets(wintertodt_status_widget_id)['text']:
        # game active
        if '%' in qh.get_widgets(wintertodt_status_widget_id)['text']:
            status['wintertodt'] = int(qh.get_widgets(wintertodt_status_widget_id)['text'].split(' ')[2][:-1])
        # game is on break
        elif 'returns' in qh.get_widgets(wintertodt_status_widget_id)['text']:
            status['next_game_in'] = qh.get_widgets(wintertodt_status_widget_id)['text']
    return status


def leave():
    osrs.move.go_to_loc(1629, 3973)
    osrs.move.interact_with_object_v3(
        29322, coord_type='y', coord_value=3967, greater_than=False,
        pre_interact=lambda: osrs.keeb.write('1'), timeout=0.3
    )


def resupply():
    leave()
    osrs.move.go_to_loc(1635, 3944)
    osrs.bank.banking_handler({
        'dump_inv': True,
        'search': [
            {
                'query': 'wt', 'items': [
                food,
                food,
                food,
                food,
                osrs.item_ids.HAMMER,
                osrs.item_ids.TINDERBOX,
            ]
            }
        ]
    })
    osrs.move.go_to_loc(1630, 3960)
    osrs.move.interact_with_object_v3(
        29322, coord_type='y', coord_value=3968, greater_than=True
    )


def load_brazier(qh: osrs.queryHelper.QueryHelper):
    last_loading_anim = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        under_falling_snow = list(
            filter(
                lambda snow: snow['x_coord'] == qh.get_player_world_location('x') and snow['y_coord'] == qh.get_player_world_location('y'),
                qh.get_objects_v2('game', falling_snow_attack)
            )
        )
        target_brazier = list(
            filter(lambda brz: brz['x_coord'] == 1621 and brz['y_coord'] == 3998,
                   qh.get_objects_v2('game', brazier))
        )
        broken = list(
            filter(lambda brz: brz['x_coord'] == 1621 and brz['y_coord'] == 3998,
                   qh.get_objects_v2('game', broken_brazier))
        )
        unlit = list(
            filter(lambda brz: brz['x_coord'] == 1621 and brz['y_coord'] == 3998,
                   qh.get_objects_v2('game', unlit_brazier))
        )

        game_status = game_state_parser(qh)
        if game_status['next_game_in']:
            osrs.dev.logger.info('Game ended while loading brazier.')
            return
        elif game_status['warmth'] and game_status['warmth'] <= 40:
            food_to_eat = qh.get_inventory(food_ids)
            if not food_to_eat:
                osrs.dev.logger.warning('In game with low warmth but Im out of food - resupplying.')
                return resupply()
            else:
                osrs.move.fast_click_v2(food_to_eat)
                osrs.clock.sleep_one_tick()
        elif not qh.get_inventory(osrs.item_ids.BRUMA_ROOT):
            osrs.dev.logger.info('Finished loading bruma roots into brazier.')
            return
        # a falling snow attack is about to hit me
        elif under_falling_snow:
            osrs.dev.logger.warning('About to get hit with a snow attack - running away!')
            return osrs.move.go_to_loc(1622, 3988, exact_tile=True)
        elif unlit:
            osrs.move.fast_click_v2(unlit[0])
        elif broken:
            osrs.move.fast_click_v2(broken[0])
        elif (datetime.now() - last_loading_anim).total_seconds() > 1.5 and target_brazier:
            '''fed = osrs.move.right_click_v6(
                qh.get_objects_v2('game', brazier)[0],
                'Feed',
                qh.get_canvas()
            )
            if fed:
                last_loading_anim = datetime.now()'''
            osrs.move.fast_click_v2(target_brazier[0])
            last_loading_anim = datetime.now()
        elif qh.get_player_animation() == 832:
            last_loading_anim = datetime.now()


def main(endless_loop=True):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({wintertodt_status_widget_id, warmth_widget_id})
    qh.set_player_animation()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_player_world_location()
    qh.set_objects_v2('game', {tree, brazier, unlit_brazier, broken_brazier, falling_snow_attack})
    # number of times to run this script
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    start_function()
    while True:
        qh.query_backend()
        game_status = game_state_parser(qh)
        if game_status['next_game_in']:
            break_info = osrs.game.break_manager_v4({
                'intensity': 'high',
                'login': False,
                'logout': False
            })
            if iter_count == 0:
                return
            elif 'took_break' in break_info and break_info['took_break']:
                iter_count -= 1

            if osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), food_ids) < 2:
                osrs.dev.logger.info("game is paused - need to resupply.")
                resupply()
            elif '0:00' in game_status['next_game_in'] and qh.get_objects_v2('game', unlit_brazier):
                osrs.move.fast_click_v2(qh.get_objects_v2('game', unlit_brazier)[0])
            else:
                osrs.move.go_to_loc(1621, 3996)
                osrs.dev.logger.info("waiting for next game to start.")
        elif game_status['warmth'] and game_status['warmth'] <= 40:
            food_to_eat = qh.get_inventory(food_ids)
            if not food_to_eat:
                osrs.dev.logger.warning('In game with low warmth but Im out of food - resupplying.')
                resupply()
            else:
                osrs.move.fast_click_v2(food_to_eat)
                osrs.clock.sleep_one_tick()
        elif len(qh.get_inventory()) == 28:
            osrs.dev.logger.info("Full inv - loading brazier")
            load_brazier(qh)
        elif game_status['wintertodt'] and game_status['wintertodt'] <= 8:
            osrs.dev.logger.info("Game is almost over - loading brazier")
            load_brazier(qh)
        elif qh.get_player_animation() not in expected_animations and qh.get_objects_v2('game', tree):
            osrs.move.go_to_loc(1622, 3988, exact_tile=True)
            osrs.move.right_click_v6(
                qh.get_objects_v2('game', tree)[0],
                'Chop',
                qh.get_canvas()
            )

