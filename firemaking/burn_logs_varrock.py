import datetime

import osrs


def burn_logs(log):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_skills({'firemaking'})
    qh.set_player_animation()
    time_since_last_burn = datetime.datetime.now()
    last_xp_count = -1
    while True:
        qh.query_backend()
        if qh.get_player_animation() == 733:
            time_since_last_burn = datetime.datetime.now()

        if not qh.get_inventory(log) and qh.get_player_animation() != 733:
            return
        elif (datetime.datetime.now() - time_since_last_burn).total_seconds() > 12:
            osrs.game.hop_worlds(total_level_worlds=False)
            time_since_last_burn = datetime.datetime.now()
            last_xp_count = -1
        elif qh.get_skills('firemaking') and qh.get_skills('firemaking')['xp'] != last_xp_count:
            last_xp_count = qh.get_skills('firemaking')['xp']
            time_since_last_burn = datetime.datetime.now()
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.TINDERBOX.value))
            osrs.move.click(qh.get_inventory(log))
            osrs.clock.sleep_one_tick()


def main(goal_lvl, log):
    iterations = 0
    bank_config_initial = [
        osrs.item_ids.ItemIDs.TINDERBOX.value,
        {
            'id': [
                osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
            ],
            'quantity': 'All'
        },
        {
            'id': [
                log,
            ],
            'quantity': 'All'
        },
    ]
    bank_config_regular = [
        {
            'id': [
                log,
            ],
            'quantity': 'All'
        },
    ]
    osrs.bank.banking_handler({
        'dump_inv': True,
        'dump_equipment': True,
        'search': [{'query': '', 'items': bank_config_initial}]
    })
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'firemaking'})
    while True:
        qh.query_backend()
        iterations += 1
        osrs.move.tab_to_varrock()
        osrs.move.go_to_loc(3212, 3429 - (iterations % 2), exact_tile=True)
        burn_logs(log)
        qh.query_backend()
        if qh.get_skills('firemaking') and qh.get_skills('firemaking')['level'] >= goal_lvl:
            return
        osrs.bank.banking_handler({
            'dump_inv': False,
            'dump_equipment': False,
            'search': [{'query': '', 'items': bank_config_regular}]
        })