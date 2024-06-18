import datetime
import pyautogui
import osrs.util
from osrs import queryHelper, item_ids, dev

logger = dev.instantiate_logger()


class LootConfig:
    def __init__(self, item_id, priority, stackable=False, min_quantity=1, alch=False):
        self.item_id = item_id
        self.priority = priority
        self.stackable = stackable
        self.min_quantity = min_quantity
        self.alch = alch

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
            logger.warn('Tried to add loot inv config items but input was not a list.')
            return False

        for item in items:
            self.inv_config[item.asdict()['item_id']] = item.asdict()

    def add_items(self, items: list[LootConfig]):
        if type(items) is not list:
            logger.warn('Tried to add loot config items but input was not a list.')
            return False

        for item in items:
            self.add_item(item)

    def add_item(self, config: LootConfig):
        self.config[config.asdict()['item_id']] = config.asdict()

    def clear_config(self):
        self.config = {}

    def retrieve_loot(self, dist=10):
        time_since_last_loot = datetime.datetime.now()
        while True:
            if (datetime.datetime.now() - time_since_last_loot).total_seconds() > 15:
                logger.warn('Looter timed out trying to get an item.')
                return False
            found_loot = False
            qh = queryHelper.QueryHelper()
            qh.set_player_world_location()
            qh.set_inventory()
            qh.query_backend()
            tiles = osrs.util.generate_surrounding_tiles_from_point(dist, qh.get_player_world_location())
            qh.set_ground_items(tiles)
            qh.set_widgets({self.high_alch_widget_id})
            qh.query_backend()
            if not qh.get_ground_items():
                return True
            for item in qh.get_ground_items():
                # dont pick up items i havent specified
                if item['id'] not in self.config:
                    continue
                item_config = self.config[item['id']]
                # dont pick up small amouts of something, i.e. coins
                if item['quantity'] < item_config['min_quantity']:
                    continue
                if len(qh.get_inventory()) == 28:
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
                res = osrs.move.right_click_v5(item, 'Take')
                if res:
                    qh1 = osrs.queryHelper.QueryHelper()
                    qh1.set_inventory()
                    qh1.set_player_world_location()

                    received_item = wait_for_item_in_inv(prev_inv, qh1)
                    if received_item:
                        time_since_last_loot = datetime.datetime.now()
                if item_config.get('alch'):
                    self.alch(item, qh)
                break
            if not found_loot:
                return True

    def alch(self, item, qh):
        qh.query_backend()
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
            print('inv is full but item is stackable and in inv, no need to drop anything.')
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
            LootConfig(item_ids.ItemIDs.ADAMANT_2H_SWORD.value, 3, alch=True),
            ## Rune
            LootConfig(item_ids.ItemIDs.RUNE_AXE.value, 2, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_LONGSWORD.value, 18, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_MACE.value, 8, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_CHAINBODY.value, 29, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_SCIMITAR.value, 15, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_FULL_HELM.value, 20, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_SPEAR.value, 11, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_SQ_SHIELD.value, 22, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_KITESHIELD.value, 31, alch=True),
            LootConfig(item_ids.ItemIDs.RUNITE_LIMBS.value, 11, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_MED_HELM.value, 11, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_DAGGER.value, 4, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_BATTLEAXE.value, 24, alch=True),
            LootConfig(item_ids.ItemIDs.RUNE_2H_SWORD.value, 24, alch=True),
            ## Dragon
            LootConfig(item_ids.ItemIDs.DRAGON_BOOTS.value, 59),
            LootConfig(item_ids.ItemIDs.DRAGON_CHAINBODY.value, 198),
            LootConfig(item_ids.ItemIDs.DRAGON_KNIFE.value, 400),
            LootConfig(item_ids.ItemIDs.DRAGON_THROWNAXE.value, 26),
            LootConfig(item_ids.ItemIDs.DRAGON_HARPOON.value, 1900),
            LootConfig(item_ids.ItemIDs.DRAGON_SWORD.value, 70),
            LootConfig(item_ids.ItemIDs.DRAGON_DAGGER.value, 17, alch=True),
            LootConfig(item_ids.ItemIDs.DRAGON_SPEAR.value, 37, alch=True),
            LootConfig(item_ids.ItemIDs.DRAGON_MED_HELM.value, 58, alch=True),
            LootConfig(item_ids.ItemIDs.DRAGON_PLATELEGS.value, 161, alch=True),
            LootConfig(item_ids.ItemIDs.DRAGON_PLATESKIRT.value, 161, alch=True),
            ## Staves and Such
            LootConfig(item_ids.ItemIDs.DUST_BATTLESTAFF.value, 9),
            LootConfig(item_ids.ItemIDs.FIRE_BATTLESTAFF.value, 9, alch=True),
            LootConfig(item_ids.ItemIDs.EARTH_BATTLESTAFF.value, 9, alch=True),
            LootConfig(item_ids.ItemIDs.LAVA_BATTLESTAFF.value, 9, alch=True),
            LootConfig(item_ids.ItemIDs.AIR_BATTLESTAFF.value, 9, alch=True),
            LootConfig(item_ids.ItemIDs.MYSTIC_EARTH_STAFF.value, 25, alch=True),
            LootConfig(item_ids.ItemIDs.MYSTIC_AIR_STAFF.value, 25, alch=True),
            ## Misc Alchable Weapons and Armor
            LootConfig(item_ids.ItemIDs.LEAFBLADED_BATTLEAXE.value, 58, alch=True),
            LootConfig(item_ids.ItemIDs.LEAFBLADED_SWORD.value, 40, alch=True),
            LootConfig(item_ids.ItemIDs.MYSTIC_ROBE_BOTTOM_LIGHT.value, 48, alch=True),
            LootConfig(item_ids.ItemIDs.MYSTIC_ROBE_TOP_LIGHT.value, 71, alch=True),
            LootConfig(item_ids.ItemIDs.MYSTIC_ROBE_BOTTOM_DARK.value, 48, alch=True),

            # Elemental Runes
            LootConfig(item_ids.ItemIDs.FIRE_RUNE.value, 1, stackable=True, min_quantity=250),
            LootConfig(item_ids.ItemIDs.AIR_RUNE.value, 1, stackable=True, min_quantity=250),
            LootConfig(item_ids.ItemIDs.EARTH_RUNE.value, 1, stackable=True, min_quantity=250),
            LootConfig(item_ids.ItemIDs.WATER_RUNE.value, 1, stackable=True, min_quantity=250),

            # Combat Runes and Odd Runes
            LootConfig(item_ids.ItemIDs.BLOOD_RUNE.value, 3, stackable=True, min_quantity=6),
            LootConfig(item_ids.ItemIDs.SOUL_RUNE.value, 3, stackable=True, min_quantity=10),
            LootConfig(item_ids.ItemIDs.NATURE_RUNE.value, 3, stackable=True, min_quantity=10),
            LootConfig(item_ids.ItemIDs.LAW_RUNE.value, 3, stackable=True, min_quantity=10),
            LootConfig(item_ids.ItemIDs.CHAOS_RUNE.value, 3, stackable=True, min_quantity=15),
            LootConfig(item_ids.ItemIDs.DUST_RUNE.value, 3, stackable=True, min_quantity=200),
            LootConfig(item_ids.ItemIDs.MUD_RUNE.value, 3, stackable=True, min_quantity=200),

            # Catacombs Drops
            LootConfig(item_ids.ItemIDs.ANCIENT_SHARD.value, 9, stackable=True),
            LootConfig(item_ids.ItemIDs.DARK_TOTEM_TOP.value, 9),
            LootConfig(item_ids.ItemIDs.DARK_TOTEM_BASE.value, 9),
            LootConfig(item_ids.ItemIDs.DARK_TOTEM_MIDDLE.value, 9),

            # Misc
            LootConfig(item_ids.ItemIDs.COINS_995.value, 6, stackable=True, min_quantity=1000),
            LootConfig(item_ids.ItemIDs.PAPAYA_FRUIT.value + 1, 6, stackable=True, min_quantity=10),
            LootConfig(item_ids.ItemIDs.COCONUT.value + 1, 6, stackable=True, min_quantity=10),
            LootConfig(item_ids.ItemIDs.BIG_BONES.value + 1, 6, stackable=True, min_quantity=10),
            LootConfig(item_ids.ItemIDs.CRYSTAL_SHARD, 10, stackable=True),
            LootConfig(item_ids.ItemIDs.DRACONIC_VISAGE.value, 3167),
            LootConfig(item_ids.ItemIDs.SMOULDERING_STONE.value, 3600),

            # Seeds
            LootConfig(item_ids.ItemIDs.SNAPDRAGON_SEED.value, 36, stackable=True),
            LootConfig(item_ids.ItemIDs.SNAPE_GRASS_SEED.value, 12, stackable=True, min_quantity=3),
            LootConfig(item_ids.ItemIDs.CADANTINE_SEED.value, 11, stackable=True),
            LootConfig(item_ids.ItemIDs.RANARR_SEED.value, 25, stackable=True),

            # Bars and Ores
            LootConfig(item_ids.ItemIDs.MITHRIL_BAR.value + 1, 4, stackable=True, min_quantity=5),
            LootConfig(item_ids.ItemIDs.ADAMANTITE_BAR.value + 1, 8, stackable=True, min_quantity=3),
            LootConfig(item_ids.ItemIDs.RUNITE_BAR.value, 11),
            LootConfig(item_ids.ItemIDs.RUNITE_BAR.value + 1, 11, stackable=True),
        ]
        return config

    def default_inv_config(self):
        config = [
            InvConfig(osrs.item_ids.ItemIDs.MONKFISH.value, osrs.loot.monkfish_eval)
        ]

        return config
