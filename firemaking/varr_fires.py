import datetime
import random

# run to 3212,3428,0 or 3212,3429,0
# begin loop
# before lighting fire check to make sure there is not a fire on tile
# if there is a fire, hop worlds
# light fire
# when out. bank
# tele back
# repeat loop
import osrs

log_id = '1517'
lit_fire_id = '26185'
tinderbox_id = '590'
varrock_tele_tab_id = '8007'
bank_booth_id = '34810'
bank_booth_tile = '3186,3436,0'
varrock_center_tile_1 = '3212,3428,0'
varrock_center_tile_2 = '3212,3429,0'
varrock_tele_widget_id = '218,21'
start_tiles = [varrock_center_tile_1, varrock_center_tile_2]
usa_world_list = [
    '305',
    '306',
    '307',
    '313',
    '314',
    '315',
    '319',
    '320',
    '321',
    '322',
    '323',
    '324',
    '329',
    '331',
]


def hop():
    world = random.randint(0, len(usa_world_list) - 1)
    osrs.keeb.press_key('enter')
    osrs.keeb.write('::hop {}'.format(usa_world_list[world]))
    osrs.keeb.press_key('enter')
    osrs.clock.random_sleep(15, 20)
    osrs.keeb.press_key('esc')
    osrs.clock.sleep_one_tick()


def tele_to_varrock_fountain(qh):
    varrock_tele_tab = qh.get_inventory(varrock_tele_tab_id)
    if not varrock_tele_tab:
        exit('out of varrock tele tabs')
    osrs.move.click(varrock_tele_tab)


def tele_to_varrock_fountain_v2(qh):
    while True:
        osrs.keeb.press_key('f6')
        osrs.clock.sleep_one_tick()
        qh.query_backend()
        tele_button = qh.get_widgets(varrock_tele_widget_id)
        if tele_button:
            osrs.move.click(tele_button)
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('esc')
            return


def walk_to_start(qh, tile):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    print(last_click)
    start_time = datetime.datetime.now()
    while True:
        qh.query_backend()
        curr_loc = qh.get_player_world_location()
        if curr_loc and \
                curr_loc['x'] == int(tile[:4]) and \
                curr_loc['y'] == int(tile[5:9]):
            break
        elif qh.get_tiles(tile) and (datetime.datetime.now() - last_click).total_seconds() > 4:
            osrs.move.click(qh.get_tiles(tile))
            last_click = datetime.datetime.now()
        elif (datetime.datetime.now() - start_time).total_seconds() > 15:
            tele_to_varrock_fountain_v2(qh)
            start_time = datetime.datetime.now()

def light_fires(qh):
    while True:
        qh.query_backend()
        prev_xp = qh.get_skills('firemaking')
        log = qh.get_inventory(log_id)
        if not log:
            print('no logs left')
            print(qh.get_inventory(log_id))
            print(log)
            break
        while True:
            curr_loc = qh.get_player_world_location()
            qh.set_game_objects({'{},{},0'.format(curr_loc['x'], curr_loc['y'])}, {lit_fire_id})
            qh.query_backend()
            fire = qh.get_game_objects(lit_fire_id)
            hopped = False
            if len(fire) > 0:
                for fire_instance in fire:
                    if 'x_coord' in fire_instance \
                            and fire_instance['x_coord'] == curr_loc['x'] \
                            and fire_instance['y_coord'] == curr_loc['y']:
                        hopped = True
                        hop()
                        break
            if hopped:
                break
            tinderbox = qh.get_inventory(tinderbox_id)
            if not tinderbox:
                exit('no tinderbox')
            osrs.move.click(tinderbox)
            osrs.move.click(log)
            burnt = False
            start_time = datetime.datetime.now()
            while True:
                qh.query_backend()
                fm_data = qh.get_skills('firemaking')
                if 'xp' in fm_data and 'xp' in prev_xp and fm_data['xp'] != prev_xp['xp']:
                    burnt = True
                    break
                elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                    break
            if burnt:
                break


def bank(qh):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_bank():
            logs = qh.get_bank(log_id)
            if not logs:
                exit('out of logs to burn')
            osrs.move.click(logs)
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('esc')
            break
        elif len(qh.get_game_objects(bank_booth_id)) > 0 \
                and (datetime.datetime.now() - last_click).total_seconds() > 7:
            booth = qh.get_game_objects(bank_booth_id)[0]
            osrs.move.click(booth)
            last_click = datetime.datetime.now()


def main():
    global iters
    iters = 0
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_tiles({varrock_center_tile_1, varrock_center_tile_2})
    qh.set_skills({'firemaking'})
    qh.set_game_objects({bank_booth_tile}, {bank_booth_id})
    qh.set_bank()
    qh.set_widgets({varrock_tele_widget_id})
    while True:
        qh.query_backend()
        iters += 1
        tile = start_tiles[iters % 2]
        tele_to_varrock_fountain_v2(qh)
        walk_to_start(qh, tile)
        light_fires(qh)
        bank(qh)
        osrs.game.break_manager_v3({'intensity': 'low', 'login': False, 'logout': False})


main()
