import datetime
import random
import logging
import osrs
import sys

print(sys.argv)

bankers_ids = [
    '1633',
    '1613',
    '1634',
    '3089'
]

#POT = int(sys.argv[1])
#SECONDARY = int(sys.argv[2])

POT = 99
SECONDARY = 231

logging.info(f'pot and sec vals: {POT} : {SECONDARY}')


def open_bank_interface(qh: osrs.queryHelper.QueryHelper):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        bank_data = qh.get_bank()
        if bank_data:
            return
        elif (datetime.datetime.now() - last_click).total_seconds() > 7:
            closest = osrs.util.find_closest_target(qh.get_npcs())
            if not closest:
                continue
            osrs.move.click(closest)
            last_click = datetime.datetime.now()


def withdraw_materials_v2(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    if not qh.get_bank():
        return
    bstring = qh.get_bank(POT)
    uns = qh.get_bank(SECONDARY)
    if not bstring:
        exit('out of bstring')
    if not uns:
        exit('out of uns')
    osrs.move.click(bstring)
    osrs.move.click(uns)
    osrs.keeb.keyboard.press(osrs.keeb.key.esc)
    osrs.keeb.keyboard.release(osrs.keeb.key.esc)
    start_time = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_inventory(POT) and qh.get_inventory(SECONDARY):
            break
        elif (datetime.datetime.now() - start_time).total_seconds() > 5:
            break


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False
}


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_bank()
    qh.set_widgets({'233,0', '270,14'})
    qh.set_npcs(bankers_ids)
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        updated_config = osrs.game.break_manager_v3(script_config)
        qh.query_backend()
        bstring = qh.get_inventory(POT)
        bow = qh.get_inventory(SECONDARY)
        if not bow or not bstring:
            osrs.server.post_game_status('Out of supplies, opening bank.', updated_config)
            open_bank_interface(qh)
            osrs.server.post_game_status('Dumping inventory in bank.', updated_config)
            osrs.bank.dump_items()
            osrs.server.post_game_status('Withdrawing materials from bank.', updated_config)
            withdraw_materials_v2(qh)
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
        elif bstring and bow and (datetime.datetime.now() - last_click).total_seconds() > 25:
            osrs.server.post_game_status('Clicking bow string.', updated_config)
            osrs.move.click(bstring)
            osrs.server.post_game_status('Clicking bow.', updated_config)
            osrs.move.click(bow)
            wait_time = datetime.datetime.now()
            osrs.server.post_game_status('Waiting for fletching menu.', updated_config)
            while True:
                qh.query_backend()
                if qh.get_widgets('270,14'):
                    osrs.server.post_game_status('Starting to fletch bows.', updated_config)
                    osrs.keeb.keyboard.press(osrs.keeb.key.space)
                    osrs.keeb.keyboard.release(osrs.keeb.key.space)
                    last_click = datetime.datetime.now()
                    osrs.server.post_game_status('Fletching.', updated_config)
                    if random.randint(0, 2) == 1:
                        osrs.move.jiggle_mouse()
                    break
                elif (datetime.datetime.now() - wait_time).total_seconds() > 4:
                    break
        elif qh.get_widgets('233,0'):
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
main()
