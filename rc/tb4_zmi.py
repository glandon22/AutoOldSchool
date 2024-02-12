import datetime

import osrs

bank = '10355'
bank_tile = '3095,3491,0'

altar = '29631'
altar_tile = '3059,5578,0'
crystal_memories_id = '25104'
globetrotter_necklace_id = '28765'
pure_ess_id = '7936'

def open_bank_interface(qh: osrs.queryHelper.QueryHelper):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        bank_data = qh.get_bank()
        if bank_data:
            return
        elif (datetime.datetime.now() - last_click).total_seconds() > 7:
            closest = osrs.util.find_closest_target(qh.get_game_objects(bank))
            if closest and closest['x'] == None:
                continue
            osrs.move.click(closest)
            last_click = datetime.datetime.now()


def tele_to_zmi(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_inventory(crystal_memories_id):
            return osrs.move.click(qh.get_inventory(crystal_memories_id))


def make_runes(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_game_objects(altar):
            return osrs.move.click(qh.get_game_objects(altar)[0])


def tele_to_bank(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_inventory(globetrotter_necklace_id):
            return osrs.move.right_click_v3(qh.get_inventory(globetrotter_necklace_id), 'Last-destination')


def withdraw_items(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_bank():
            osrs.clock.sleep_one_tick()
            qh.query_backend()
            for item in [crystal_memories_id, globetrotter_necklace_id, pure_ess_id]:
                osrs.move.click(qh.get_bank(item))
            return


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_game_objects(
        {bank_tile, altar_tile},
        {bank, altar}
    )
    qh.set_equipment()
    qh.set_bank()
    while True:
        open_bank_interface(qh)
        osrs.bank.dump_items()
        osrs.clock.sleep_one_tick()
        withdraw_items(qh)
        osrs.keeb.press_key('esc')
        osrs.clock.random_sleep(0.1, 0.11)
        tele_to_zmi(qh)
        make_runes(qh)
        tele_to_bank(qh)

main()
