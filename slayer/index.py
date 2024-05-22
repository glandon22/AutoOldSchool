import osrs
import slayer
from osrs.item_ids import ItemIDs
import transport_functions
varrock_tele_widget_id = '218,23'


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_slayer()
    qh.set_inventory()
    qh.set_chat_options()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        slayer_task = qh.get_slayer() and 'monster' in qh.get_slayer() and qh.get_slayer()['monster']
        if slayer_task:
            # Verified
            if slayer_task == 'Iron Dragons':
                slayer.iron_dragons_v2.main()
            # Verified
            elif slayer_task == 'Kalphite':
                slayer.kalphite.main()
            # Verified
            elif slayer_task == 'Trolls':
                slayer.trolls.main()
            # Verified
            elif slayer_task == 'Blue Dragons':
                slayer.blue_dragons_v2.main()
            # Verified
            elif slayer_task == 'Black Dragons':
                slayer.black_dragons_v2.main()
            # Verified
            elif slayer_task == 'Greater Demons':
                slayer.greater_demons.main()
            # Verified
            elif slayer_task == 'Fire Giants':
                slayer.fire_giants.main()
            # Verified
            elif slayer_task == 'Dagannoth':
                slayer.dagganoth.main()
            # Verified
            elif slayer_task == 'Hellhounds':
                slayer.hellhounds.main()
            # Verified
            elif slayer_task == 'Black Demons':
                slayer.black_demons.main()
            # Verified
            elif slayer_task == 'Turoth':
                slayer.turoth.main()
            # Verified
            elif slayer_task == 'Bloodveld':
                slayer.bloodvelds.main()
            # Verified
            elif slayer_task == 'Ankou':
                slayer.ankou.main()
            # Verified
            elif slayer_task == 'Wyrms':
                slayer.wyrms.main()
            # Verified
            elif slayer_task == 'Aberrant Spectres':
                slayer.aberrant_spectres.main()
            # Verified
            elif slayer_task == 'Dust Devils':
                slayer.dust_devils.main()
            # Verified
            elif slayer_task == 'Steel Dragons':
                slayer.steel_dragons.main()
            # Verified
            elif slayer_task == 'Spiritual Creatures':
                slayer.spiritual_creatures.main()
            # Verified
            elif slayer_task == 'Kurask':
                slayer.kurask.main()
            # Verified
            elif slayer_task == 'Mutated Zygomites':
                slayer.mutated_zygomite.main()
            else:
                return print(f'Can not parse {slayer_task}')
        else:
            while True:
                qh.query_backend()
                if 3195 <= qh.get_player_world_location('x') <= 3226:
                    osrs.clock.sleep_one_tick()
                    osrs.clock.sleep_one_tick()
                    break
            while True:
                qh.query_backend()
                slayer_ring = qh.get_inventory([
                    ItemIDs.SLAYER_RING_1.value,
                    ItemIDs.SLAYER_RING_2.value,
                    ItemIDs.SLAYER_RING_3.value,
                    ItemIDs.SLAYER_RING_4.value,
                    ItemIDs.SLAYER_RING_5.value,
                    ItemIDs.SLAYER_RING_6.value,
                    ItemIDs.SLAYER_RING_7.value,
                    ItemIDs.SLAYER_RING_8.value,
                ])
                if not slayer_ring:
                    return print('need new task, no slayer ring in inv')
                if osrs.move.right_click_v3(slayer_ring, 'Rub'):
                    osrs.clock.sleep_one_tick()
                    osrs.keeb.write('1')
                    osrs.clock.sleep_one_tick()
                    osrs.keeb.write('1')
                    break
            transport_functions.nieve()
            osrs.clock.sleep_one_tick()
            osrs.game.cast_spell(varrock_tele_widget_id)


main()
