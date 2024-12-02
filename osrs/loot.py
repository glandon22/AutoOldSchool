import datetime
import pyautogui
import osrs.util
from osrs import queryHelper, item_ids, dev


class LootConfig:
    def __init__(self, item_id, priority, stackable=False, min_quantity=1, alch=False, consume=False):
        self.item_id = item_id
        self.priority = priority
        self.stackable = stackable
        self.min_quantity = min_quantity
        self.alch = alch
        self.consume = consume

    def asdict(self):
        return {
            'item_id': self.item_id,
            'priority': self.priority,
            'stackable': self.stackable,
            'min_quantity': self.min_quantity,
            'alch': self.alch
        }


class InvConfig:
    def __init__(self, item_id, eval_function, left_click=True):
        self.item_id = item_id
        self.eval_function = eval_function
        self.left_click = left_click

    def asdict(self):
        return {
            'item_id': self.item_id,
            'eval_function': self.eval_function,
            'left_click': self.left_click
        }


def wait_for_item_in_inv(prev_inv, qh1):
    prev_loc = None
    time_on_same_tile = datetime.datetime.now()
    while True:
        qh1.query_backend()
        if qh1.get_inventory() != prev_inv:
            print('got item')
            return True
        elif (datetime.datetime.now() - time_on_same_tile).total_seconds() > 1.5:
            print('err: timeout getting item')
            return False
        elif qh1.get_player_world_location() != prev_loc:
            prev_loc = qh1.get_player_world_location()
            time_on_same_tile = datetime.datetime.now()


def monkfish_eval(loot_priority):
    if loot_priority > 5:
        return True
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'hitpoints'})
    qh.query_backend()
    if qh.get_skills('hitpoints')['level'] - qh.get_skills('hitpoints')['boostedLevel'] > 12:
        return True
    return False


def shark_eval(loot_priority):
    if loot_priority > 6:
        return True
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'hitpoints'})
    qh.query_backend()
    if qh.get_skills('hitpoints')['level'] - qh.get_skills('hitpoints')['boostedLevel'] > 15:
        return True
    return False


def karambwan_eval(loot_priority):
    if loot_priority > 10:
        return True
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'hitpoints'})
    qh.query_backend()
    if qh.get_skills('hitpoints')['level'] - qh.get_skills('hitpoints')['boostedLevel'] >= 18:
        return True
    return False


def in_pile(target_item, ground_items):
    count = 0
    for item in ground_items:
        if item['x_coord'] == target_item['x_coord'] and item['y_coord'] == target_item['y_coord']:
            count += 1
            if count > 1:
                return True
    return False


class Loot:
    config = {}
    inv_config = {}
    high_alch_widget_id = '218,44'

    def __init__(self):
        self.add_items(self.default_config())
        self.add_inv_config_items(self.default_inv_config())

    def add_inv_config_item(self, config: InvConfig):
        self.inv_config[config.asdict()['item_id']] = config.asdict()

    def add_inv_config_items(self, items: list[InvConfig]):
        if type(items) is not list:
            dev.logger.warn('Tried to add loot inv config items but input was not a list.')
            return False

        for item in items:
            self.inv_config[item.asdict()['item_id']] = item.asdict()

    def add_items(self, items: list[LootConfig]):
        if type(items) is not list:
            dev.logger.warn('Tried to add loot config items but input was not a list.')
            return False

        for item in items:
            self.add_item(item)

    def add_item(self, config: LootConfig):
        self.config[config.asdict()['item_id']] = config.asdict()

    def clear_config(self):
        self.config = {}

    def retrieve_loot(
            self, dist=10, min_val_to_loot_other_players=100,
            loot_area=None, disable_alchs=False
    ):
        '''

        :param dist:
        :param min_val_to_loot_other_players: minimum loot value to allow looting of other players drops. this makes
        me look more bot like and has me running all over the place
        :return:
        '''
        time_since_last_loot = datetime.datetime.now()
        while True:
            if (datetime.datetime.now() - time_since_last_loot).total_seconds() > 15:
                dev.logger.warn('Looter timed out trying to get an item.')
                return False
            found_loot = False
            qh = queryHelper.QueryHelper()
            qh.set_player_world_location()
            qh.set_inventory()
            qh.query_backend()
            qh.set_canvas()
            qh.set_objects_v2('ground_items', set())
            qh.set_widgets({self.high_alch_widget_id})
            qh.query_backend()
            if not qh.get_objects_v2('ground_items'):
                return True
            sorted_items = sorted(qh.get_objects_v2('ground_items'), key=lambda obj: obj['dist'])
            for item in sorted_items:
                # dont pick up items i havent specified
                if item['id'] not in self.config or (
                    item['ownership'] != 1 and self.config[item['id']]['priority'] < min_val_to_loot_other_players
                ):
                    continue
                elif loot_area and not (
                        loot_area['x_min'] <= item['x_coord'] <= loot_area['x_max']
                        and loot_area['y_min'] <= item['y_coord'] <= loot_area['y_max']
                ):
                    osrs.dev.logger.warn('Item on the ground but it is outside of my configured looting zone.')
                    continue
                item_config = self.config[item['id']]
                # dont pick up small amouts of something, i.e. coins
                if item['quantity'] < item_config['min_quantity']:
                    continue
                if qh.get_inventory() and len(qh.get_inventory()) == 28:
                    space_made = self.handle_full_inv(qh, item_config)
                    if not space_made:
                        return False

                found_loot = True
                prev_inv = qh.get_inventory()
                # i want to implement this
                # but could just left clicking loot on floor
                # cause problems if monsters are on top?
                '''if in_pile(item, qh.get_ground_items()):
                    osrs.move.right_click_v4(item, 'Take')
                else:
                    osrs.move.fast_click(item)'''
                res = osrs.move.right_click_v6(item, 'Take', qh.get_canvas())
                if res:
                    qh1 = osrs.queryHelper.QueryHelper()
                    qh1.set_inventory()
                    qh1.set_player_world_location()

                    received_item = wait_for_item_in_inv(prev_inv, qh1)
                    if received_item:
                        time_since_last_loot = datetime.datetime.now()
                if item_config.get('alch') and not disable_alchs:
                    self.alch(item, qh)
                break
            if not found_loot:
                return True

    def alch(self, item, qh):
        qh.query_backend()
        if not qh.get_inventory(osrs.item_ids.NATURE_RUNE):
            osrs.dev.logger.warn("Tried to alch something with no nature runes - aborting!")
            return
        if qh.get_inventory(item['id']):
            osrs.keeb.press_key('f6')
            osrs.clock.sleep_one_tick()
            qh.query_backend()
            osrs.move.click(qh.get_widgets(self.high_alch_widget_id))
            osrs.clock.random_sleep(0.2, 0.3)
            qh.query_backend()
            if qh.get_inventory(item['id']):
                osrs.move.click(qh.get_inventory(item['id']))
            else:
                osrs.move.click({'x': pyautogui.position().x, 'y': pyautogui.position().y})
            osrs.clock.random_sleep(0.2, 0.3)
            osrs.keeb.press_key('esc')

    def handle_full_inv(self, qh, loot_item_config):
        if qh.get_inventory(loot_item_config['item_id']) and loot_item_config['stackable']:
            osrs.dev.logger.info('inv is full but item is stackable and in inv, no need to drop anything.')
            return True
        # check if item is stackable and in inv, if so exit true
        for item in qh.get_inventory():
            if item['id'] not in self.inv_config:
                continue
            item_config = self.inv_config[item['id']]
            # this item can be eaten, drank, or dropped
            if item_config['eval_function'] and item_config['eval_function'](loot_item_config['priority']):
                if item_config['left_click']:
                    osrs.move.click(item)
                else:
                    osrs.move.right_click_v4(item, 'Drop', in_inv=True)

                wait_time = datetime.datetime.now()
                while True:
                    qh.query_backend()
                    if len(qh.get_inventory()) < 28:
                        return True
                    elif (datetime.datetime.now() - wait_time).total_seconds() > 2:
                        break
        return False

    def default_config(self):
        config = [
            # Alchable Armor and Weapons
            ## Addy
            LootConfig(osrs.item_ids.ADAMANT_2H_SWORD, 3, alch=True),
            LootConfig(osrs.item_ids.ADAMANT_PLATEBODY, 4, alch=True),
            ## Rune
            LootConfig(osrs.item_ids.RUNE_AXE, 2, alch=True),
            LootConfig(osrs.item_ids.RUNE_WARHAMMER, 24, alch=True),
            LootConfig(osrs.item_ids.RUNE_LONGSWORD, 18, alch=True),
            LootConfig(osrs.item_ids.RUNE_MACE, 8, alch=True),
            LootConfig(osrs.item_ids.RUNE_CHAINBODY, 29, alch=True),
            LootConfig(osrs.item_ids.RUNE_SCIMITAR, 15, alch=True),
            LootConfig(osrs.item_ids.RUNE_FULL_HELM, 20, alch=True),
            LootConfig(osrs.item_ids.RUNE_SPEAR, 11, alch=True),
            LootConfig(osrs.item_ids.RUNE_SQ_SHIELD, 22, alch=True),
            LootConfig(osrs.item_ids.RUNE_KITESHIELD, 31, alch=True),
            LootConfig(osrs.item_ids.RUNITE_LIMBS, 11, alch=True),
            LootConfig(osrs.item_ids.RUNE_MED_HELM, 11, alch=True),
            LootConfig(osrs.item_ids.RUNE_DAGGER, 4, alch=True),
            LootConfig(osrs.item_ids.RUNE_BATTLEAXE, 24, alch=True),
            LootConfig(osrs.item_ids.RUNE_2H_SWORD, 24, alch=True),
            LootConfig(osrs.item_ids.RUNE_PLATELEGS, 24, alch=True),
            LootConfig(osrs.item_ids.RUNE_PLATEBODY, 40, alch=True),
            LootConfig(osrs.item_ids.RUNE_KNIFEP_5660, 6, alch=True, min_quantity=25),
            LootConfig(osrs.item_ids.RUNE_KNIFEP_5667, 12, stackable=True, min_quantity=25),
            ## Dragon
            LootConfig(osrs.item_ids.DRAGON_BOOTS, 59),
            LootConfig(osrs.item_ids.DRAGON_CHAINBODY, 198),
            LootConfig(osrs.item_ids.DRAGON_KNIFE, 400),
            LootConfig(osrs.item_ids.DRAGON_THROWNAXE, 26),
            LootConfig(osrs.item_ids.DRAGON_HARPOON, 1900),
            LootConfig(osrs.item_ids.DRAGON_SWORD, 70),
            LootConfig(osrs.item_ids.DRAGON_MACE, 35, alch=True),
            LootConfig(osrs.item_ids.DRAGON_DAGGER, 17, alch=True),
            LootConfig(osrs.item_ids.DRAGON_LONGSWORD, 60, alch=True),
            LootConfig(osrs.item_ids.DRAGON_BATTLEAXE, 119, alch=True),
            LootConfig(osrs.item_ids.DRAGON_SPEAR, 37, alch=True),
            LootConfig(osrs.item_ids.DRAGON_MED_HELM, 58, alch=True),
            LootConfig(osrs.item_ids.DRAGON_PLATELEGS, 161, alch=True),
            LootConfig(osrs.item_ids.DRAGON_PLATESKIRT, 161, alch=True),
            LootConfig(osrs.item_ids.DRAGON_SCIMITAR, 59, alch=True),
            LootConfig(osrs.item_ids.DRAGON_CHAINBODY, 190),
            ## Staves and Such
            LootConfig(osrs.item_ids.KRAKEN_TENTACLE, 838),
            LootConfig(osrs.item_ids.DUST_BATTLESTAFF, 9),
            LootConfig(osrs.item_ids.TRIDENT_OF_THE_SEAS_FULL, 676),
            LootConfig(osrs.item_ids.FIRE_BATTLESTAFF, 9, alch=True),
            LootConfig(osrs.item_ids.EARTH_BATTLESTAFF, 9, alch=True),
            LootConfig(osrs.item_ids.LAVA_BATTLESTAFF, 9, alch=True),
            LootConfig(osrs.item_ids.AIR_BATTLESTAFF, 9, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_EARTH_STAFF, 25, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_WATER_STAFF, 25, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_AIR_STAFF, 25, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_FIRE_STAFF, 25, alch=True),
            LootConfig(osrs.item_ids.SMOKE_BATTLESTAFF, 1200),
            LootConfig(osrs.item_ids.ANCIENT_STAFF, 80),
            ## Misc Alchable Weapons and Armor
            LootConfig(osrs.item_ids.LEAFBLADED_BATTLEAXE, 58, alch=True),
            LootConfig(osrs.item_ids.LEAFBLADED_SWORD, 40, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_ROBE_BOTTOM_LIGHT, 48, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_ROBE_TOP_LIGHT, 71, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_ROBE_BOTTOM_DARK, 48, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_ROBE_TOP_DARK, 79, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_ROBE_TOP, 71, alch=True),
            LootConfig(osrs.item_ids.MYSTIC_ROBE_BOTTOM, 47, alch=True),
            LootConfig(osrs.item_ids.BATTLESTAFF + 1, 8, stackable=True),
            LootConfig(osrs.item_ids.RED_DHIDE_BODY, 6, alch=True),
            LootConfig(osrs.item_ids.GREEN_DHIDE_BODY, 4, alch=True),
            LootConfig(osrs.item_ids.GREEN_DHIDE_CHAPS, 2, alch=True),
            LootConfig(osrs.item_ids.OCCULT_NECKLACE, 800,),

            LootConfig(osrs.item_ids.GRANITE_MAUL, 300),

            # Elemental Runes
            LootConfig(osrs.item_ids.FIRE_RUNE, 1, stackable=True, min_quantity=250),
            LootConfig(osrs.item_ids.AIR_RUNE, 1, stackable=True, min_quantity=250),
            LootConfig(osrs.item_ids.EARTH_RUNE, 1, stackable=True, min_quantity=250),
            LootConfig(osrs.item_ids.WATER_RUNE, 1, stackable=True, min_quantity=250),

            # Combat Runes and Odd Runes
            LootConfig(osrs.item_ids.BLOOD_RUNE, 3, stackable=True, min_quantity=6),
            LootConfig(osrs.item_ids.DEATH_RUNE, 3, stackable=True, min_quantity=6),
            LootConfig(osrs.item_ids.SOUL_RUNE, 3, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.NATURE_RUNE, 3, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.LAW_RUNE, 3, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.CHAOS_RUNE, 3, stackable=True, min_quantity=15),
            LootConfig(osrs.item_ids.DUST_RUNE, 3, stackable=True, min_quantity=200),
            LootConfig(osrs.item_ids.MUD_RUNE, 3, stackable=True, min_quantity=200),
            LootConfig(osrs.item_ids.SMOKE_RUNE, 3, stackable=True, min_quantity=100),
            LootConfig(osrs.item_ids.WRATH_RUNE, 9, stackable=True, min_quantity=30),

            # Catacombs Drops
            LootConfig(osrs.item_ids.ANCIENT_SHARD, 9, stackable=True),
            LootConfig(osrs.item_ids.DARK_TOTEM_TOP, 9),
            LootConfig(osrs.item_ids.DARK_TOTEM_BASE, 9),
            LootConfig(osrs.item_ids.DARK_TOTEM_MIDDLE, 9),

            # Misc
            LootConfig(osrs.item_ids.COINS_995, 6, stackable=True, min_quantity=1000),
            LootConfig(osrs.item_ids.PAPAYA_FRUIT + 1, 6, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.COCONUT + 1, 6, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.BIG_BONES + 1, 6, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.CRYSTAL_SHARD, 10, stackable=True),
            LootConfig(osrs.item_ids.DRACONIC_VISAGE, 3167),
            LootConfig(osrs.item_ids.SMOULDERING_STONE, 3600),
            LootConfig(osrs.item_ids.WATER_ORB + 1, 5, min_quantity=4, stackable=True),
            LootConfig(osrs.item_ids.CRYSTAL_KEY, 20),
            LootConfig(osrs.item_ids.JAR_OF_DIRT, 24),
            LootConfig(osrs.item_ids.JAR_OF_SMOKE, 58),
            LootConfig(osrs.item_ids.DRAGONSTONE_RING, 11, alch=True),
            LootConfig(osrs.item_ids.OAK_PLANK + 1, 5, stackable=True, min_quantity=2),
            LootConfig(osrs.item_ids.RAW_SHARK + 1, 10, stackable=True, min_quantity=2),
            LootConfig(osrs.item_ids.RAW_MONKFISH + 1, 8, stackable=True, min_quantity=7),
            LootConfig(osrs.item_ids.RUNE_ARROW, 8, stackable=True, min_quantity=50),
            LootConfig(osrs.item_ids.MOLTEN_GLASS + 1, 5, stackable=True, min_quantity=50),
            LootConfig(osrs.item_ids.MAGIC_LOGS + 1, 5, stackable=True, min_quantity=5),
            LootConfig(osrs.item_ids.DIAMOND + 1, 5, stackable=True, min_quantity=3),
            LootConfig(osrs.item_ids.ONYX_BOLT_TIPS, 5, stackable=True),
            LootConfig(osrs.item_ids.MARK_OF_GRACE, 11, stackable=True),

            # Seeds
            LootConfig(osrs.item_ids.SNAPDRAGON_SEED, 36, stackable=True),
            LootConfig(osrs.item_ids.SNAPE_GRASS_SEED, 12, stackable=True, min_quantity=3),
            LootConfig(osrs.item_ids.CADANTINE_SEED, 11, stackable=True),
            LootConfig(osrs.item_ids.RANARR_SEED, 25, stackable=True),
            LootConfig(osrs.item_ids.TORSTOL_SEED, 4, stackable=True),
            LootConfig(osrs.item_ids.MAGIC_SEED, 64, stackable=True),
            LootConfig(osrs.item_ids.YEW_SEED, 23, stackable=True),
            LootConfig(osrs.item_ids.SPIRIT_SEED, 100, stackable=True),
            LootConfig(osrs.item_ids.PALM_TREE_SEED, 28, stackable=True),
            LootConfig(osrs.item_ids.DRAGONFRUIT_TREE_SEED, 186, stackable=True),
            LootConfig(osrs.item_ids.CELASTRUS_SEED, 65, stackable=True),
            LootConfig(osrs.item_ids.REDWOOD_TREE_SEED, 23, stackable=True),

            # Bars and Ores
            LootConfig(osrs.item_ids.MITHRIL_BAR + 1, 4, stackable=True, min_quantity=5),
            LootConfig(osrs.item_ids.ADAMANTITE_BAR + 1, 8, stackable=True, min_quantity=3),
            LootConfig(osrs.item_ids.RUNITE_ORE, 11),
            LootConfig(osrs.item_ids.ADAMANTITE_ORE + 1, 5, min_quantity=5),
            LootConfig(osrs.item_ids.RUNITE_BAR, 11),
            LootConfig(osrs.item_ids.RUNITE_BAR + 1, 11, stackable=True),
            LootConfig(osrs.item_ids.GOLD_ORE + 1, 2, stackable=True, min_quantity=10),
            LootConfig(osrs.item_ids.COAL + 1, 5, stackable=True, min_quantity=30),

            # Herbs
            LootConfig(osrs.item_ids.GRIMY_SNAPDRAGON + 1, 5, stackable=True, min_quantity=2),
            LootConfig(osrs.item_ids.GRIMY_TOADFLAX + 1, 5, stackable=True, min_quantity=2),
            LootConfig(osrs.item_ids.GRIMY_TORSTOL + 1, 5, stackable=True, min_quantity=2),
            LootConfig(osrs.item_ids.GRIMY_RANARR_WEED + 1, 7, stackable=True),

            # Potions
            LootConfig(osrs.item_ids.SANFEW_SERUM4, 22),
            LootConfig(osrs.item_ids.PRAYER_POTION4, 11),

            # Food
            LootConfig(osrs.item_ids.SHARK, 1),
            LootConfig(osrs.item_ids.UGTHANKI_KEBAB, 1),
            LootConfig(osrs.item_ids.TUNA_POTATO, 1),


            LootConfig(osrs.item_ids.DRAGON_DEFENDER, 1),
            LootConfig(osrs.item_ids.RIGHT_SKULL_HALF, 1),
            LootConfig(osrs.item_ids.BOTTOM_OF_SCEPTRE, 1),
            LootConfig(osrs.item_ids.TOP_OF_SCEPTRE, 1),
            LootConfig(osrs.item_ids.LEFT_SKULL_HALF, 1),
            LootConfig(osrs.item_ids.CRYSTAL_SHARD, 1),
            LootConfig(osrs.item_ids.CRYSTAL_SHARDS, 1),
            LootConfig(osrs.item_ids.ENHANCED_CRYSTAL_TELEPORT_SEED, 1),
            LootConfig(osrs.item_ids.SOUL_FRAGMENT, 1),
            LootConfig(osrs.item_ids.SOUL_FRAGMENT_25201, 1),

            ## Vorkath
            LootConfig(osrs.item_ids.SUPERIOR_DRAGON_BONES, 20),
            LootConfig(osrs.item_ids.DRAGON_BONES + 1, 62, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.BLUE_DRAGONHIDE + 1, 48, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.GREEN_DRAGONHIDE + 1, 38, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.RED_DRAGONHIDE + 1, 56, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.BLACK_DRAGONHIDE + 1, 68, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.DRAGON_BOLTS_UNF, 47, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.DRAGON_DART_TIP, 21, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.RUNE_DART_TIP, 93, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.DRAGONSTONE_BOLT_TIPS, 10, min_quantity=2, stackable=True),
            LootConfig(osrs.item_ids.ONYX_BOLT_TIPS, 10, stackable=True),
            LootConfig(osrs.item_ids.DRAGON_ARROWTIPS, 35, stackable=True),
            LootConfig(osrs.item_ids.MANTA_RAY + 1, 66, stackable=True, min_quantity=2),
            LootConfig(osrs.item_ids.DRAGONSTONE + 1, 22, stackable=True),
            LootConfig(osrs.item_ids.VORKATHS_HEAD, 101),
            LootConfig(osrs.item_ids.VORKATHS_HEAD_21907, 101),
            LootConfig(osrs.item_ids.VORKATHS_HEAD_21912, 101),
            LootConfig(osrs.item_ids.VORKATHS_HEAD, 101),
            LootConfig(osrs.item_ids.DRAGONBONE_NECKLACE, 67),
            LootConfig(osrs.item_ids.JAR_OF_DECAY, 111),
            LootConfig(osrs.item_ids.SKELETAL_VISAGE, 12695),

            LootConfig(osrs.item_ids.WARRIOR_HELM, 17),


            LootConfig(osrs.item_ids.BRIMSTONE_KEY, 100, stackable=True),
            LootConfig(osrs.item_ids.BRINE_SABRE, 300),
            LootConfig(osrs.item_ids.KURASK_HEAD, 8),


            ## LEAGUES JUNK
            LootConfig(osrs.item_ids.SCROLL_BOX_EASY, 4, stackable=True),
            LootConfig(osrs.item_ids.PURE_ESSENCE + 1, 2, stackable=True),
            LootConfig(osrs.item_ids.GIANT_KEY, 2, stackable=True),
            LootConfig(osrs.item_ids.MOSSY_KEY, 2, stackable=True),
            LootConfig(osrs.item_ids.BIG_BONES, 2,),
            LootConfig(osrs.item_ids.BLACK_MASK, priority=10),
            LootConfig(osrs.item_ids.BLACK_MASK_10, priority=10),
            LootConfig(osrs.item_ids.LIMPWURT_SEED, 4, stackable=True),
        ]
        return config

    def default_inv_config(self):
        config = [
            InvConfig(osrs.item_ids.MONKFISH, osrs.loot.monkfish_eval),
            InvConfig(osrs.item_ids.SHARK, osrs.loot.shark_eval),
            InvConfig(osrs.item_ids.COOKED_KARAMBWAN, osrs.loot.karambwan_eval)
        ]

        return config
