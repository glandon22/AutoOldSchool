import datetime
import random

import osrs

deposit_sack_id = '27431'
water_bucket_id = '5598'


equipment = [
    {'id': osrs.item_ids.GRACEFUL_TOP, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_HOOD, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_LEGS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.GRICOLLERS_CAN,
    osrs.item_ids.SEED_DIBBER,
    osrs.item_ids.SPADE
]

# These are the tiles I click to run to the start of the farming run
raw_path_to_start = [
    [1813,3500,0],
    [1813,3493,0],
    [1814,3488,0]
]

raw_farming_spots = [
    [1815,3490,0],
    [1812,3490,0],
    [1815,3493,0],
    [1812,3493,0],
    [1815,3496,0],
    [1812,3496,0],
    [1815,3499,0],
    [1812,3499,0],
    [1812,3505,0],
    [1812,3508,0],
    [1812,3511,0],
    [1812,3514,0],
    [1815,3512,0],
    [1815,3509,0],
    [1815,3506,0],
    [1815,3503,0],
    [1820,3497,0],
    [1820,3494,0],
    [1820,3491,0],
    [1820,3488,0],
]

failed_state_ids = [
    '27408',
    '27411',
    '27414',
    '27416'
]

bolo_seed = osrs.item_ids.BOLOGANO_SEED
EMPTY_PATCH = '27383'

UNWATERED_SEED_STAGE_1 = '27395'
WATERED_STAGE_1 = '27396'

UNWATERED_SEED_STAGE_2 = '27398'
WATERED_STAGE_2 = '27399'

UNWATERED_SEED_STAGE_3 = '27401'
WATERED_STAGE_3 = '27402'

HEALTHY_STAGE_4 = '27404'

gricollers_can_id = '13353'

script_config = {

    'intensity': 'high',
    'logout': False,
    'login': False,
}

# there are water buckets at each corner, so make sure i found the right bucket that is the western corner
def determine_correct_water_bucket(objects):
#qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, water_bucket_id)[0]
    for bucket in objects[water_bucket_id]:
        for sack in objects[deposit_sack_id]:
            if sack['x_coord'] - bucket['x_coord'] == 0 and sack['y_coord'] - bucket['y_coord'] == 2:
                return bucket


def translate_tiles():
    instanced_farming_spots = []
    instance_path_to_start = []
    qh = osrs.queryHelper.QueryHelper()
    # Figure out my current tile now that I am in an instance, in order to translate
    # what tiles the patches are on in the instance.
    qh.set_player_world_location()
    qh.set_objects_v2('game', {5598})
    qh.query_backend()
    # This water bucket is my anchor point
    water_bucket = osrs.util.find_closest_target_in_game(
        qh.get_objects_v2('game', 5598), qh.get_player_world_location()
    )
    x_diff = water_bucket['x_coord'] - 1809
    y_diff = water_bucket['y_coord'] - 3500
    # Update the farming patch tiles now that I know where my instance has spawned on the world map
    for spot in raw_farming_spots:
        instanced_farming_spots.append(
            [str(spot[0] + x_diff), str(spot[1] + y_diff), '0']
        )

    # Also translate the running path tiles that i need to start the run
    for spot in raw_path_to_start:
        instance_path_to_start.append(
            f'{str(spot[0] + x_diff)},{str(spot[1] + y_diff)},0'
        )

    return [water_bucket, instance_path_to_start, instanced_farming_spots]


def plant_handler(current_state, desired_state, instanced_farming_spots):
    for i, spot in enumerate(instanced_farming_spots):
        print(f'Looking for spot: {i}. current state: {current_state}. desired state: {desired_state}')
        last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
        last_seed_click = datetime.datetime.now() - datetime.timedelta(hours=1)
        objects_to_search = {current_state, desired_state, UNWATERED_SEED_STAGE_1}.union(set(failed_state_ids))
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        qh.set_objects(
            {','.join(spot)},
            objects_to_search,
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        while True:
            qh.query_backend()
            print(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
            # I'm planting the seed, so need to click gricollers can first.
            if desired_state == WATERED_STAGE_1:
                if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, UNWATERED_SEED_STAGE_1) and \
                        (datetime.datetime.now() - last_click).total_seconds() > 4:
                    print('clicking to water seed.')
                    osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, UNWATERED_SEED_STAGE_1)[0])
                    osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, UNWATERED_SEED_STAGE_1)[0])
                    last_click = datetime.datetime.now()
                elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, current_state) and \
                        (datetime.datetime.now() - last_seed_click).total_seconds() > 4:
                    print('clicking to plant seed.')
                    logo_seed = qh.get_inventory(bolo_seed)
                    if not logo_seed:
                        exit('out of logovano seeds')
                    osrs.move.click(logo_seed)
                    osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, current_state)[0])
                    last_seed_click = datetime.datetime.now()
            else:
                if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, current_state) and \
                        (datetime.datetime.now() - last_click).total_seconds() > 4:
                    print('clicking to water a plant')
                    osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, current_state)[0])
                    osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, current_state)[0])
                    last_click = datetime.datetime.now()

            if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, desired_state):
                print('found our desired state.')
                break


def run_to_start(instance_path_to_start, trips):
    if trips % 3 == 0:
        osrs.move.spam_click(instance_path_to_start[0], 1)
        osrs.move.spam_click(instance_path_to_start[1], 2)
    return osrs.move.spam_click(instance_path_to_start[2], 4)


def fill_can(water_bucket, trips):
    # only fill up every three trips
    if trips % 3 != 0:
        return
    while True:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        qh.set_objects(
            {f'{water_bucket["x_coord"]},{water_bucket["y_coord"]},0'},
            {water_bucket_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        if qh.get_inventory(gricollers_can_id) and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, water_bucket_id):
            osrs.move.click(qh.get_inventory(gricollers_can_id))
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, water_bucket_id)[0])
            osrs.clock.random_sleep(10, 10.1)
            return


def get_seeds():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_widgets({osrs.widget_ids.chat_input_request_widget})
    qh.query_backend()
    if qh.get_widgets(osrs.widget_ids.chat_input_request_widget):
        osrs.keeb.write('10k')
        osrs.keeb.press_key('enter')
        osrs.clock.sleep_one_tick()
        return True
    elif qh.get_chat_options('Bologano', fuzzy=True):
        osrs.keeb.write(str(qh.get_chat_options('Bologano', fuzzy=True)))


def start():
    osrs.game.slow_lumb_tele()
    osrs.move.go_to_loc(3208, 3211)
    osrs.move.interact_with_object_v3(
        14880, obj_type='ground', coord_type='y', coord_value=9000,
        greater_than=True, right_click_option='Climb-down', timeout=8
    )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'tithe', 'items': equipment}]
    })
    osrs.game.tele_home()
    osrs.game.click_restore_pool()
    osrs.game.tele_home_fairy_ring('akr')
    osrs.move.go_to_loc(1798, 3503)
    osrs.move.interact_with_object_v3(
        27430, right_click_option='Search', timeout=10,
        custom_exit_function=get_seeds
    )
    osrs.move.interact_with_object_v3(27445, obj_type='wall', coord_type='x', coord_value=5000, greater_than=True)


def get_boxes():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['6920'])
    qh.set_widgets({'236,7,4'})
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_widgets('236,7,4'):
            res = osrs.move.right_click_v6(
                qh.get_widgets('236,7,4'),
                'Buy-50',
                qh.get_canvas(),
                in_inv=True
            )
            if res:
                osrs.keeb.press_key('esc')
                osrs.keeb.press_key('esc')
                return
        elif qh.get_npcs():
            osrs.move.right_click_v6(
                qh.get_npcs()[0],
                'Rewards',
                qh.get_canvas(),
                in_inv=True
            )


def send_herbs_to_bank():
    start = datetime.datetime.now()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if not qh.get_inventory(osrs.item_ids.HERB_BOX):
            return

        elif (datetime.datetime.now() - start).total_seconds() > 300:
            return
        else:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.HERB_BOX),
                'Bank-all',
                qh.get_canvas(),
                in_inv=True
            )


def collect_rewards(qh):
    qh.query_backend()
    if qh.get_widgets('241,6'):
        parsed = int(qh.get_widgets('241,6')['text'].split(': ')[1])
        if parsed > 1900:
            osrs.move.interact_with_object_v3(
                27445, obj_type='wall', coord_type='x', coord_value=5000, greater_than=False
            )
            get_boxes()
            osrs.clock.random_sleep(1, 1.1)
            send_herbs_to_bank()
            osrs.move.interact_with_object_v3(
                27430, right_click_option='Search', timeout=10,
                custom_exit_function=get_seeds
            )
            osrs.move.interact_with_object_v3(
                27445, obj_type='wall', coord_type='x', coord_value=5000, greater_than=True
            )


def main(endless_loop=True):
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    start()
    trips = 0
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({'241,6'})
    while True:
        qh.query_backend()
        water_bucket, instance_path_to_start, instanced_farming_spots = translate_tiles()
        run_to_start(instance_path_to_start, trips)
        osrs.inv.power_drop_v2(qh, [osrs.item_ids.GRICOLLERS_FERTILISER])
        plant_handler(EMPTY_PATCH, WATERED_STAGE_1, instanced_farming_spots)
        plant_handler(UNWATERED_SEED_STAGE_2, WATERED_STAGE_2, instanced_farming_spots)
        plant_handler(UNWATERED_SEED_STAGE_3, WATERED_STAGE_3, instanced_farming_spots)
        plant_handler(HEALTHY_STAGE_4, EMPTY_PATCH, instanced_farming_spots)
        fill_can(water_bucket, trips)
        trips += 1
        osrs.move.interact_with_object_v3(
            {27431, 27432}, custom_exit_function=osrs.inv.not_in_inv_check,
            custom_exit_function_arg=osrs.item_ids.BOLOGANO_FRUIT
        )
        break_info = osrs.game.break_manager_v4(script_config)
        if iter_count == 0:
            return
        elif 'took_break' in break_info and break_info['took_break']:
            iter_count -= 1
        collect_rewards(qh)

