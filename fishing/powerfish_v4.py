import datetime

import osrs

fish_to_catch = 'salmon'

fish_spot_ids = {
    'shrimp': [
        1514, 1517, 1518,
        1521, 1523, 1524,
        1525, 1528, 1530,
        1544, 3913, 7155,
        7459, 7462, 7467,
        7469, 7947, 10513,
        12778
    ],
    'lobster': [
        1510, 1519, 1522,
        2146,
        3914, 5820, 7199,
        7460, 7465, 7470,
        7946, 9173, 9174,
        10515, 10635, 12777
    ],
    'shark': [
        1511, 1520, 3419,
        3915, 4476, 4477,
        5233, 5234, 5821,
        7200, 7461, 7466,
        8525, 8526, 8527,
        9171, 9172, 10514,
        12775, 12776
    ],
    'monkfish': [
        4316
    ],
    'salmon': [
        394, 1506, 1507,
        1508, 1509, 1513,
        1515, 1516, 1526,
        1527, 3417, 3418,
        7463, 7464, 7468,
        8524, 12774
    ],
    'lava_eel': [4928, 6784],
    'barbarian': [
        1542, 7323
    ],
    'anglerfish': [6825],
    'minnow': [7730, 7731, 7732, 7733],
    'internal_eel': [7676],
    'sacred_eel': [6488],
    'cave_eel': [1497, 1498, 1499, 1500],
    'slimy_eel': [2653, 2654, 2655],
    'karambwan': [4712, 4713],
    'karambwanji': [4710],
    'dark_crab': [1535, 1536]
}

fish_to_drop = [
    osrs.item_ids.RAW_SHRIMPS,
    osrs.item_ids.RAW_ANCHOVIES,
    osrs.item_ids.RAW_SARDINE,
    osrs.item_ids.RAW_HERRING,
    osrs.item_ids.RAW_LOBSTER,
    osrs.item_ids.RAW_TUNA,
    osrs.item_ids.RAW_SWORDFISH,
    osrs.item_ids.RAW_SHARK,
    osrs.item_ids.RAW_BASS,
    osrs.item_ids.RAW_MONKFISH,
    osrs.item_ids.RAW_SALMON,
    osrs.item_ids.RAW_TROUT,
    osrs.item_ids.RAW_PIKE,
    osrs.item_ids.RAW_LAVA_EEL,
    osrs.item_ids.LEAPING_STURGEON,
    osrs.item_ids.LEAPING_SALMON,
    osrs.item_ids.LEAPING_TROUT,
    osrs.item_ids.RAW_ANGLERFISH,
    osrs.item_ids.INFERNAL_EEL,
    osrs.item_ids.RAW_KARAMBWAN,
    osrs.item_ids.RAW_KARAMBWANJI,
    osrs.item_ids.SACRED_EEL,
    osrs.item_ids.RAW_CAVE_EEL,
    osrs.item_ids.RAW_SLIMY_EEL,
    osrs.item_ids.RAW_DARK_CRAB,
]


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_npcs(list(map(str, fish_spot_ids[fish_to_catch])))
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'low',
            'login': False,
            'logout': False
        })
        qh.query_backend()
        spots = qh.get_npcs()
        if qh.get_inventory() and len(qh.get_inventory()) == 28:
            osrs.inv.power_drop_v2(qh, fish_to_drop)
        elif not qh.get_interating_with() and spots:
            sorted_spots = sorted(spots, key=lambda spot: spot['dist'])
            if len(sorted_spots) > 0:
                osrs.move.fast_click(sorted_spots[0])
        elif qh.get_interating_with():
            osrs.dev.logger.info('Currently fishing.')

main()