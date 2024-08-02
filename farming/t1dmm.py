import datetime

import osrs

deposit_sack_id = '27431'
water_bucket_id = '5598'

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

LOGOVANO_SEED = '13423'
EMPTY_PATCH = '27383'

UNWATERED_SEED_STAGE_1 = '27384'
WATERED_STAGE_1 = '27385'

UNWATERED_SEED_STAGE_2 = '27387'
WATERED_STAGE_2 = '27388'

UNWATERED_SEED_STAGE_3 = '27390'
WATERED_STAGE_3 = '27391'

HEALTHY_STAGE_4 = '27393'

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
    qh.query_backend()
    t = osrs.util.generate_surrounding_tiles_from_point(15, qh.get_player_world_location())
    qh.set_objects(
        set(t),
        {water_bucket_id, deposit_sack_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.query_backend()
    # This water bucket is my anchor point
    water_bucket = determine_correct_water_bucket(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
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
                    logo_seed = qh.get_inventory(LOGOVANO_SEED)
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


def fill_watering_cans():
    while True:
        inv = osrs.inv.get_inv()
        not_full_can = osrs.inv.are_items_in_inventory_v2(inv, [5331, 5333, 5334, 5335, 5336, 5337, 5338, 5339])
        if not_full_can:
            osrs.move.move_and_click(not_full_can['x'], not_full_can['y'], 3, 3)
            water = osrs.server.get_surrounding_game_objects(10, ['5598'])
            if '5598' in water:
                osrs.move.move_and_click(water['5598']['x'], water['5598']['y'], 2, 2)
                osrs.clock.random_sleep(0.6, 0.7)
        else:
            break


def main():
    trips = 0
    while True:
        water_bucket, instance_path_to_start, instanced_farming_spots = translate_tiles()
        run_to_start(instance_path_to_start, trips)
        plant_handler(EMPTY_PATCH, WATERED_STAGE_1, instanced_farming_spots)
        plant_handler(UNWATERED_SEED_STAGE_2, WATERED_STAGE_2, instanced_farming_spots)
        plant_handler(UNWATERED_SEED_STAGE_3, WATERED_STAGE_3, instanced_farming_spots)
        plant_handler(HEALTHY_STAGE_4, EMPTY_PATCH, instanced_farming_spots)
        #fill_can(water_bucket, trips)
        fill_watering_cans()
        trips += 1
        osrs.game.break_manager_v4(script_config)


main()
