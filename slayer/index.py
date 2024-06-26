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
                # slayer.brutal_blue_drag.main()
            # Verified
            elif slayer_task == 'Black Dragons':
                slayer.black_dragons_v2.main()
            # Verified
            elif slayer_task == 'Greater Demons':
                slayer.greater_demons.main()
            # Verified
            elif slayer_task == 'Fire Giants':
                # slayer.fire_giants.main()
                slayer.fire_giants_catacombs.main()
            # Verified
            elif slayer_task == 'Dagannoth':
                # slayer.dagganoth.main()
                slayer.dagannoth_catacombs.main()
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
                #slayer.bloodvelds.main()
                slayer.mutated_bloodveld.main()
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
            elif slayer_task == 'Gargoyles':
                slayer.gargoyles.main()
            elif slayer_task == 'Suqahs':
                slayer.suqah.main()
            elif slayer_task == 'Nechryael':
                slayer.nechs.main()
            elif slayer_task == 'Drakes':
                slayer.drakes.main()
            elif slayer_task == 'Abyssal Demons':
                slayer.abby_demon.main()
            elif slayer_task == 'Cave Kraken':
                slayer.kraken_boss.main()
            else:
                return print(f'Can not parse {slayer_task}')
        else:
            while True:
                qh.query_backend()
                # in varrock center
                if 3195 <= qh.get_player_world_location('x') <= 3226 and 3419 <= qh.get_player_world_location(
                        'y') <= 3438:
                    osrs.clock.sleep_one_tick()
                    osrs.clock.sleep_one_tick()
                    break
            transport_functions.duradel()
            osrs.game.cast_spell(varrock_tele_widget_id)


main()
