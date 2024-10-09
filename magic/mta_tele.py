import datetime
import osrs
from osrs.util import find_closest_target_on_screen


def get_on_tile():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_mta_data()
    qh.set_player_world_location()
    qh.set_objects_v2('wall', {10755})
    qh.set_destination_tile()
    qh.set_npcs(['5979'])
    while True:
        qh.query_backend()
        if qh.get_mta_data() and 'teleTile' in qh.get_mta_data():
            qh.set_tiles({f"{qh.get_mta_data()['teleTile']['x']},{qh.get_mta_data()['teleTile']['y']},0"})
            if qh.get_player_world_location()['x'] == qh.get_mta_data()['teleTile']['x'] and \
                    qh.get_player_world_location()['y'] == qh.get_mta_data()['teleTile']['y']:
                break
            elif qh.get_destination_tile() and qh.get_destination_tile()['x'] == qh.get_mta_data()['teleTile']['x'] \
                    and qh.get_destination_tile()['y'] == qh.get_mta_data()['teleTile']['y']:
                osrs.dev.logger.info('headed to correct mta tele tile')
                continue
            elif qh.get_tiles(f"{qh.get_mta_data()['teleTile']['x']},{qh.get_mta_data()['teleTile']['y']},0"):
                osrs.move.fast_click_v2(
                    qh.get_tiles(f"{qh.get_mta_data()['teleTile']['x']},{qh.get_mta_data()['teleTile']['y']},0")
                )
            elif qh.get_objects_v2('wall', 10755):
                osrs.move.fast_click_v2(sorted(qh.get_objects_v2('wall', 10755), key=lambda wall: wall['dist'])[0])
        elif qh.get_objects_v2('wall', 10755):
            osrs.move.fast_click_v2(sorted(qh.get_objects_v2('wall', 10755), key=lambda wall: wall['dist'])[0])
        elif qh.get_npcs():
            osrs.move.fast_click_v2(qh.get_npcs()[0])


def open_spells():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['6777'])
    qh.set_widgets({'161,65', osrs.widget_ids.tele_grab_widget_id})
    if qh.get_widgets('161,65') and qh.get_widgets('161,65')['spriteID'] != 1027:
        osrs.keeb.press_key('f6')
    elif qh.get_widgets(osrs.widget_ids.tele_grab_widget_id):
        osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.tele_grab_widget_id))
# finished 6779 right clcik New-maze


def cast_on_guardian():
    osrs.dev.logger.info('casting')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['6777', '6778', '6779'])
    qh.set_widgets({'161,65', osrs.widget_ids.tele_grab_widget_id})
    qh.set_canvas()
    while True:
        get_on_tile()
        qh.query_backend()
        in_transit = list(filter(lambda npc: npc['id'] == 6778, qh.get_npcs()))
        finished = list(filter(lambda npc: npc['id'] == 6779, qh.get_npcs()))
        ready = list(filter(lambda npc: npc['id'] == 6777, qh.get_npcs()))
        if in_transit:
            return 1
        elif finished:
            return 2

        if qh.get_widgets('161,65') and qh.get_widgets('161,65')['spriteID'] != 1027:
            osrs.keeb.press_key('f6')
        elif qh.get_widgets(osrs.widget_ids.tele_grab_widget_id):
            osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.tele_grab_widget_id))
            if ready:
                c = find_closest_target_on_screen(ready)
                if c:
                    res = osrs.move.right_click_v6(c, 'Cast', qh.get_canvas(), in_inv=True)
                    if res:
                        osrs.clock.sleep_one_tick()
                        osrs.clock.sleep_one_tick()
                        continue
            #osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.tele_grab_widget_id))


def reset():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['6779'])
    qh.set_canvas()
    while True:
        qh.query_backend()
        finished = list(filter(lambda npc: npc['id'] == 6779, qh.get_npcs()))
        if finished:
            res = osrs.move.right_click_v6(
                finished[0], 'New-maze', qh.get_canvas(), in_inv=True
            )
            if res:
                osrs.clock.random_sleep(1.5, 2)
                return


def enter_room():
    osrs.dev.logger.info('entering in')
    osrs.move.interact_with_object_v3(23673, 'x', 4000, True)

def main():
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': enter_room,
            'logout': False
        })
        status = cast_on_guardian()
        if status == 2:
            reset()
enter_room()
main()
