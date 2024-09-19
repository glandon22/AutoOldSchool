import datetime

import osrs

'''
***USAGE***
1. Set rock_to_mine to whichever rock you want to mine
2. Position yourself near the rock you want to mine
3. Start script
'''

rock_to_mine = 'mith'

rock_map = {
    'copper': {10943, 11161},
    'tin': {11361, 11360, 11368, 11369},
    'iron': {11364, 11365},
    'coal': {11366, 11367},
    'mith': {11372, 11373},
    'addy': {11374, 11375},
    'rune': {11377, 11376},
    'silver': {11368, 11369},
    'gold': {11370, 11371},
}

ore_to_drop = [
    osrs.item_ids.TIN_ORE,
    osrs.item_ids.COPPER_ORE,
    osrs.item_ids.IRON_ORE,
    osrs.item_ids.SILVER_ORE,
    osrs.item_ids.GOLD_ORE,
    osrs.item_ids.COAL,
    osrs.item_ids.MITHRIL_ORE,
    osrs.item_ids.ADAMANTITE_ORE,
    osrs.item_ids.RUNITE_ORE,
]


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_is_mining()
    qh.set_objects_v2('game', rock_map[rock_to_mine])
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        rocks = qh.get_objects_v2('game')
        if qh.get_inventory(ore_to_drop):
            osrs.dev.logger.info('Ore in inventory, dropping.')
            osrs.inv.power_drop_v2(qh, ore_to_drop)
        elif qh.get_is_mining():
            osrs.dev.logger.info('Currently mining.')
            continue
        # dont click more than 1 tick
        elif rocks and (datetime.datetime.now() - last_click).total_seconds() > 0.61:
            osrs.dev.logger.info('Clicking a new rock to mine.')
            closest = osrs.util.find_closest_target_on_screen(rocks)
            if closest:
                osrs.move.fast_click_v2(closest)


main()
