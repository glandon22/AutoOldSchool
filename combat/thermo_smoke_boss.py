import datetime

import osrs


prayer_restoring_pot_list = [
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION3,
    osrs.item_ids.PRAYER_POTION2,
    osrs.item_ids.PRAYER_POTION1,
    osrs.item_ids.SUPER_RESTORE1,
    osrs.item_ids.SUPER_RESTORE2,
    osrs.item_ids.SUPER_RESTORE3,
    osrs.item_ids.SUPER_RESTORE4,
]


def end_trip(qh: osrs.queryHelper.QueryHelper):
    if not qh.get_slayer() or not qh.get_slayer()['monster']:
        osrs.dev.logger.info('task complete')
        return True
    elif not qh.get_inventory(prayer_restoring_pot_list):
        osrs.dev.logger.info('out of prayer pots and super restores')
        return True
    else:
        return False


def main():
    loot_handler = osrs.loot.Loot()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({
        'hitpoints',
        'prayer'
    })
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_players()
    qh.set_slayer()
    qh.set_active_prayers()
    qh.set_widgets(osrs.combat_utils.pot_handler_required_prayer_widgets)
    qh.set_npcs_by_name(['thermonuclear smoke devil'])
    last_player_sighting = datetime.datetime.now()
    while True:
        qh.query_backend()
        if end_trip(qh):
            return

        osrs.combat_utils.pot_handler(qh, {})
        osrs.combat_utils.prayer_handler(qh, ['redemption'])
        # remove myself from the players list
        filtered_players = [] if not qh.get_players() else list(filter(lambda player: player['name'].lower() != 'DJT Fan 14', qh.get_players()))
        if not filtered_players:
            last_player_sighting = datetime.datetime.now()
        else:
            print('p', filtered_players)
            # check if there is another player here
            # only hop if player has been around for more than 5 seconds, i am not interacting with thermy or thermy is
            # not attacking me
            if (datetime.datetime.now() - last_player_sighting).total_seconds() > 5 \
                    and filtered_players and not qh.get_interating_with() \
                    and (not qh.get_npcs_by_name()
                        or 'interacting' not in qh.get_npcs_by_name()[0]
                        or qh.get_npcs_by_name()[0]['interacting'].lower() != 'DJT Fan 14'
            ):
                osrs.game.hop_worlds(lambda: osrs.clock.random_sleep(10.2, 10.3))

        if not qh.get_interating_with() and not qh.get_npcs_by_name():
            loot_handler.retrieve_loot()
            osrs.game.break_manager_v4({
                'intensity': 'high',
                'login': False,
                'logout': lambda: osrs.clock.random_sleep(11, 14),
            })
        elif not qh.get_interating_with() and qh.get_npcs_by_name():
            thermy = qh.get_npcs_by_name()[0]
            if 'interacting' in thermy and thermy['interacting'] == 'DJT Fan 14':
                print('thermy is attacking me, letting auto retaliate get me back in combat')
            elif thermy['health'] != 0 and not filtered_players:
                osrs.move.fast_click(thermy)


