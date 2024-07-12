'''
notes
run to 2414,3060,0
cave entrance is 30176 - > y over 9k
right click run to 2381,9452
click wall id 535
right click run to 2367,9447

check for another player before doing anything! also check for a player after hopping worlds!

npc name: thermonuclear smoke devil

keep redemption up all times
super restore sip when pray is zero
loot stuff and alch
'''
import datetime

import osrs


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
    qh.set_active_prayers()
    qh.set_widgets(osrs.combat_utils.pot_handler_required_prayer_widgets)
    qh.set_npcs_by_name(['thermonuclear smoke devil'])
    last_player_sighting = datetime.datetime.now()
    while True:
        qh.query_backend()
        osrs.combat_utils.pot_handler(qh, {})
        osrs.combat_utils.prayer_handler(qh, ['redemption'])
        # remove myself from the players list
        filtered_players = [] if not qh.get_players() else list(filter(lambda player: player.lower() != 'greazydonkey', qh.get_players()))
        if not filtered_players:
            last_player_sighting = datetime.datetime.now()
        else:
            print('p', filtered_players)

        if not qh.get_interating_with() and not qh.get_npcs_by_name():
            # check if there is another player here
            if (datetime.datetime.now() - last_player_sighting).total_seconds() > 5 and filtered_players:
                osrs.game.hop_worlds(lambda: osrs.clock.random_sleep(10.2, 10.3))
            loot_handler.retrieve_loot(10)
        elif not qh.get_interating_with() and qh.get_npcs_by_name():
            thermy = qh.get_npcs_by_name()[0]
            if 'interacting' in thermy and thermy['interacting'] == 'GreazyDonkey':
                print('thermy is attacking me, letting auto retaliate get me back in combat')
            elif thermy['health'] != 0 and not filtered_players:
                osrs.move.fast_click(thermy)

main()

