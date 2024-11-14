import random

import osrs
import slayer

import slayer.transport_functions as transport_functions

varrock_tele_widget_id = '218,23'


def skip_task():
    skip_list = [
        'cave kraken',
        'cave horror',
        'cave horrors',
        'waterfiends',
        #'dagannoth',
        'adamant dragons'
    ]
    task_widget = '426,12,6'
    cancel_widget = '426,26,1'
    confirm_widget = '426,8'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['duradel'])
    qh.set_slayer()
    qh.set_canvas()
    qh.set_widgets({task_widget, cancel_widget, confirm_widget})
    while True:
        while True:
            qh.query_backend()
            if qh.get_slayer() and qh.get_slayer()['monster']:
                print('got a new task in skip')
                break
            elif qh.get_npcs_by_name():
                closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
                if closest:
                    osrs.move.fast_click(closest)
        while True:
            qh.query_backend()
            if qh.get_slayer():
                if qh.get_slayer()['monster'].lower() not in skip_list:
                    return
                else:
                    break
        while True:
            qh.query_backend()
            if not qh.get_slayer():
                osrs.clock.sleep_one_tick()
                osrs.keeb.press_key('esc')
                break
            elif qh.get_widgets(confirm_widget) and not qh.get_widgets(confirm_widget)['isHidden']:
                osrs.move.click(qh.get_widgets(confirm_widget))
                osrs.clock.sleep_one_tick()
            elif qh.get_widgets(cancel_widget) and not qh.get_widgets(cancel_widget)['isHidden']:
                osrs.move.click(qh.get_widgets(cancel_widget))
                osrs.clock.sleep_one_tick()
            elif qh.get_widgets(task_widget) and not qh.get_widgets(task_widget)['isHidden']:
                osrs.move.click(qh.get_widgets(task_widget))
                osrs.clock.sleep_one_tick()
            elif qh.get_npcs_by_name():
                osrs.move.right_click_v6(
                    qh.get_npcs_by_name()[0],
                    'Rewards',
                    qh.get_canvas(),
                    in_inv=True
                )


def start_function():
    if not osrs.bank.banking_handler({}, check_bank_in_sight=True):
        osrs.game.slow_lumb_tele()
        osrs.move.go_to_loc(3208, 3211)
        osrs.move.interact_with_object_v3(
            14880, obj_type='ground', coord_type='y', coord_value=9000,
            greater_than=True, right_click_option='Climb-down', timeout=8
        )
    osrs.bank.banking_handler({
        'dump_inv': True,
        'search': [{'query': 'slayer', 'items': [osrs.item_ids.RUNE_POUCH, osrs.item_ids.KARAMJA_GLOVES_3]}]
    })


def main(endless_loop=True):
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    qh = osrs.queryHelper.QueryHelper()
    qh.set_slayer()
    qh.set_inventory()
    qh.set_chat_options()
    qh.set_player_world_location()
    start_function()
    while True:
        qh.query_backend()
        slayer_task = qh.get_slayer() and 'monster' in qh.get_slayer() and qh.get_slayer()['monster']
        area = qh.get_slayer() and 'area' in qh.get_slayer() and qh.get_slayer()['area']
        if slayer_task:
            # Verified
            if slayer_task == 'Iron Dragons':
                slayer.iron_dragons_v2.main()
            # Verified
            elif slayer_task == 'Kalphite':
                slayer.kalphite.main()
            # Verified
            elif slayer_task == 'Trolls':
                # this task is constantly misclicking on trees. need to do this in a different location
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
                slayer.dagganoth.main()
                #slayer.dagannoth_catacombs.main()
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
                #slayer.mutated_bloodveld.main()
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
                slayer.kurask.main(area)
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
            elif slayer_task == 'Waterfiends':
                slayer.waterfiends.main()
            elif slayer_task == 'Smoke Devils':
                #slayer.thermonucler_smoke_devil.main()
                slayer.smoke_devil.main()
            elif slayer_task == 'Dark Beasts':
                slayer.dark_beast.main()
            elif slayer_task == 'Rune Dragons':
                slayer.rune_drags.main()
            elif slayer_task == 'Elves':
                slayer.elves.main()
            elif slayer_task == 'Araxytes':
                slayer.araxyte.main()
            elif slayer_task == 'Fossil Island Wyverns':
                slayer.fossil_island_wyvern.main()

            else:
                return print(f'Can not parse {slayer_task}')
        else:
            transport_functions.duradel()
            skip_task()
            osrs.game.cast_spell(varrock_tele_widget_id)
            iter_count -= 1
            if iter_count == 0:
                osrs.dev.logger.debug("Completed iterations for slayer script.")
                return

main()