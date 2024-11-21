import random

import osrs
import slayer

import slayer.transport_functions as transport_functions

varrock_tele_widget_id = '218,23'


skip_config = {
    'cave kraken': {
        'areas': ['']
    },
    'cave horror': {
        'areas': ['']
    },
    'waterfiends': {
        'areas': ['']
    },
    'adamant dragons': {
        'areas': ['']
    },
    'bronze dragons': {
        'areas': ['Catacombs of Kourend']
    },
    'iron dragons': {
        'areas': ['Catacombs of Kourend']
    },
    'blue dragons': {
        'areas': ['Catacombs of Kourend']
    },
    'black dragons': {
        'areas': ["Evil Chicken's Lair", 'Catacombs of Kourend']
    },
    'nechryael': {
        'areas': ['Catacombs of Kourend']
    },
    'greater demons': {
        'areas': ['Catacombs of Kourend']
    },
    'dust devils': {
        'areas': ['Catacombs of Kourend']
    },
    'black demons': {
        'areas': ['Catacombs of Kourend']
    },
    'steel dragons': {
        'areas': ['Catacombs of Kourend']
    },
    'bloodveld': {
        'areas': ['Meiyerditch Laboratories']
    },
    'ankou': {
        'areas': ['Stronghold of Security']
    },
    'abyssal demons': {
        'areas': ['Catacombs of Kourend', 'Abyss']
    },
}


def skip_task(npc='duradel'):
    task_widget = '426,12,6'
    cancel_widget = '426,26,1'
    confirm_widget = '426,8'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([npc])
    qh.set_slayer()
    qh.set_canvas()
    qh.set_widgets({task_widget, cancel_widget, confirm_widget})
    while True:
        qh.query_backend()
        if (
                qh.get_slayer()
                and (
                        qh.get_slayer()['monster'].lower() not in skip_config
                        or (
                                '' not in skip_config[qh.get_slayer()['monster'].lower()]['areas']
                                and qh.get_slayer()['area'] not in skip_config[qh.get_slayer()['monster'].lower()]['areas']
                        )
                )
        ):
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('esc')
            break
        elif not qh.get_slayer() and qh.get_npcs_by_name():
            osrs.move.interact_with_npc(
                ['8623'], right_click_option='Assignment', timeout=7, exit_on_dialogue=True
            )
        elif qh.get_widgets(confirm_widget) and not qh.get_widgets(confirm_widget)['isHidden']:
            osrs.move.click(qh.get_widgets(confirm_widget))
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('esc')
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


def start_function(am_skipping=False):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_slayer()
    qh.query_backend()
    if not osrs.bank.banking_handler({}, check_bank_in_sight=True):
        osrs.game.slow_lumb_tele()
        osrs.move.go_to_loc(3208, 3211)
        osrs.move.interact_with_object_v3(
            14880, obj_type='ground', coord_type='y', coord_value=9000,
            greater_than=True, right_click_option='Climb-down', timeout=8
        )
    if not qh.get_slayer() or am_skipping:
        osrs.bank.banking_handler({
            'dump_inv': True,
            'search': [{
                'query': 'slayer', 'items': [
                    osrs.item_ids.RUNE_POUCH, osrs.item_ids.KARAMJA_GLOVES_3,
                    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'}
                ]
            }]
        })


def quick_skip():
    #transport_functions.duradel()
    start_function(am_skipping=True)
    transport_functions.konar()
    skip_task('konar quo maten')
    osrs.game.cast_spell(varrock_tele_widget_id)


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
                if area in ['Catacombs of Kourend']:
                    quick_skip()
                    continue
                if area in ['', 'Isle of Souls Dungeon']:
                    slayer.iron_dragons_v2.main()
                if area in ['Brimhaven Dungeon']:
                    slayer.iron_dragons_v2.brimhaven()
            if slayer_task == 'Bronze Dragons':
                if area in ['Catacombs of Kourend']:
                    quick_skip()
                    continue
                if area in ['', 'Brimhaven Dungeon']:
                    slayer.bronze.brimhaven()
            # Verified
            elif slayer_task == 'Kalphite':
                slayer.kalphite.main()
            # Verified
            elif slayer_task == 'Trolls':
                if area in ['', 'South of Mount Quidamortem']:
                    slayer.trolls.main()
                elif area == 'Keldagrim':
                    slayer.trolls.kelda()
            # Verified
            elif slayer_task == 'Blue Dragons':
                if area in ['Catacombs of Kourend']:
                    quick_skip()
                    continue
                slayer.blue_dragons_v2.main()
            # Verified
            elif slayer_task == 'Black Dragons':
                if area in ["Evil Chicken's Lair", 'Catacombs of Kourend']:
                    quick_skip()
                slayer.black_dragons_v2.main()
            # Verified
            elif slayer_task == 'Greater Demons':
                if area in ['Isle of Souls Dungeon']:
                    slayer.greater_demons.main()
                elif area in ['Brimhaven Dungeon', '']:
                    slayer.greater_demons.brim()
                elif area in ['Chasm of Fire']:
                    slayer.greater_demons.chasm()
                elif area in ['Catacombs of Kourend']:
                    quick_skip()
            # Verified
            elif slayer_task == 'Fire Giants':
                if area in ['Catacombs of Kourend', '']:
                    slayer.fire_giants_catacombs.main()
                if area in ['Isle of Souls Dungeon']:
                    slayer.fire_giants.main()
                if area in ['Karuulm Slayer Dungeon']:
                    slayer.fire_giants_catacombs.karuulm()
                if area in ['Brimhaven Dungeon']:
                    slayer.fire_giants_catacombs.brimhaven()
                if area in ['Stronghold Slayer Dungeon']:
                    slayer.fire_giants_catacombs.stronghold()
            # Verified
            elif slayer_task == 'Dagannoth':
                if area in ['', 'Waterbirth Island']:
                    slayer.dagganoth.main()
                elif area == 'Catacombs of Kourend':
                    slayer.dagannoth_catacombs.main()
                elif area == 'Lighthouse':
                    slayer.dagannoth_catacombs.lighthouse()
            # Verified
            elif slayer_task == 'Hellhounds':
                if area == 'Catacombs of Kourend':
                    slayer.hellhounds.catacombs()
                elif area in ['', 'Taverley Dungeon']:
                    slayer.hellhounds.main()
                elif area == 'Stronghold Slayer Dungeon':
                    slayer.hellhounds.stronghold()
            # cok, t d, and b d verified
            elif slayer_task == 'Black Demons':
                if area == 'Catacombs of Kourend':
                    quick_skip()
                    continue
                if area in ['', 'Taverley Dungeon']:
                    slayer.black_demons.main()
                if area == 'Brimhaven Dungeon':
                    slayer.black_demons.brim()
                if area == 'Chasm of Fire':
                    slayer.black_demons.chasm()
            # Verified
            elif slayer_task == 'Turoth':
                slayer.turoth.main()
            # Verified
            elif slayer_task == 'Bloodveld':
                if area in ['', 'Stronghold Slayer Dungeon']:
                    slayer.bloodvelds.main()
                elif area == 'Catacombs of Kourend':
                    slayer.mutated_bloodveld.main()
                elif area == 'Slayer Tower':
                    slayer.bloodvelds.mory()
                elif area == 'Meiyerditch Laboratories':
                    quick_skip()
                    continue
            # Verified
            elif slayer_task == 'Ankou':
                if area == 'Stronghold of Security':
                    quick_skip()
                    continue
                slayer.ankou.main(area)
            # Verified
            elif slayer_task == 'Wyrms':
                slayer.wyrms.main()
            # Verified
            elif slayer_task == 'Aberrant Spectres':
                slayer.aberrant_spectres.main(area)
            # Verified
            elif slayer_task == 'Dust Devils':
                if area in ['Catacombs of Kourend']:
                    quick_skip()
                    continue
                slayer.dust_devils.main()
            # Verified
            elif slayer_task == 'Steel Dragons':
                if area in ['Catacombs of Kourend']:
                    quick_skip()
                    continue
                slayer.steel_dragons.main()
            # Verified
            elif slayer_task == 'Spiritual Creatures':
                slayer.spiritual_creatures.main()
            # Verified
            elif slayer_task == 'Kurask':
                slayer.kurask.main(area)
            # Verified
            elif slayer_task == 'Mutated Zygomites':
                if area in ['', 'Zanaris']:
                    slayer.mutated_zygomite.main()
                elif area == 'Fossil Island':
                    slayer.mutated_zygomite.fossil_island()
            elif slayer_task == 'Gargoyles':
                slayer.gargoyles.main()
            elif slayer_task == 'Suqahs':
                slayer.suqah.main()
            elif slayer_task == 'Nechryael':
                if area in ['Catacombs of Kourend']:
                    quick_skip()
                    continue
                slayer.nechs.main()
            elif slayer_task == 'Drakes':
                slayer.drakes.main()
            elif slayer_task == 'Abyssal Demons':
                if area in ['Catacombs of Kourend', 'Abyss']:
                    quick_skip()
                slayer.abby_demon.main(area)
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
            elif slayer_task == 'Skeletal Wyverns':
                slayer.skeletal_wyverns.main()
            elif slayer_task == 'Brine Rats':
                slayer.brine.main()
            elif slayer_task == 'Jellies':
                if area in ['', 'Catacombs of Kourend']:
                    slayer.jellies.main()
                elif area == 'Fremennik Slayer Dungeon':
                    slayer.jellies.frem()
            elif slayer_task == 'Basilisks':
                if area in ['', 'Catacombs of Kourend']:
                    slayer.jellies.main()
            else:
                print(f'Can not parse {slayer_task}')
                print('slay: ', qh.get_slayer())
                return
        else:
            quick_skip()
            iter_count -= 1
            if iter_count == 0:
                osrs.dev.logger.debug("Completed iterations for slayer script.")
                return

main()