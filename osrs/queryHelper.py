import osrs.game
import osrs.server as server
import osrs.dev as dev
import osrs.inv as inv
import osrs.util as util
from enum import Enum

config = dev.load_yaml()


class ObjectTypes(Enum):
    GAME = 'game'
    GROUND = 'ground'
    DECORATIVE = 'decorative'
    WALL = 'wall'


class QueryHelper:
    query = {}
    game_data = {}

    def __init__(self):
        # Always pull in the game canvas area
        self.query = {}
        self.game_data = {}

    def set_game_state(self):
        self.query['gameState'] = True

    def get_game_state(self):
        return 'gameState' in self.game_data and self.game_data['gameState']

    def set_game_cycle(self):
        self.query['gameCycle'] = True

    def get_game_cycle(self):
        return 'gameCycle' in self.game_data and self.game_data['gameCycle']

    def set_active_prayers(self):
        self.query['activePrayers'] = True

    def get_active_prayers(self):
        return 'activePrayers' in self.game_data and self.game_data['activePrayers']

    def set_destination_tile(self):
        self.query['destinationTile'] = True

    def get_destination_tile(self):
        return 'destinationTile' in self.game_data and self.game_data['destinationTile']

    def set_interating_with(self):
        self.query['interactingWith'] = True

    def get_interating_with(self):
        return 'interactingWith' in self.game_data and self.game_data['interactingWith']

    def set_detailed_interating_with(self):
        self.query['detailedInteracting'] = True

    def get_detailed_interating_with(self):
        return 'detailedInteracting' in self.game_data and self.game_data['detailedInteracting']

    def set_players(self):
        self.query['players'] = True

    def get_players(self, get_own_player=False):
        if get_own_player:
            players = self.game_data.get('players', [])
            myself = next((player for player in players if player['name'] == 'UtahDogs'), False)
            return myself if myself else False
        else:
            return self.game_data.get('players')

    def set_world(self):
        self.query['world'] = True

    def get_world(self):
        return 'world' in self.game_data and self.game_data['world']

    def player_animation(self):
        self.query['playerAnimation'] = True

    def set_player_animation(self):
        self.query['playerAnimation'] = True

    def get_player_animation(self):
        return 'playerAnimation' in self.game_data and self.game_data['playerAnimation']

    def set_right_click_menu(self):
        self.query['rightClickV2'] = True

    def get_right_click_menu(self):
        return 'rightClickV2' in self.game_data and self.game_data['rightClickV2']

    def player_world_location(self):
        self.query['playerWorldPoint'] = True

    def set_player_world_location(self):
        self.query['playerWorldPoint'] = True

    def get_player_world_location(self, coord=False):
        if not coord:
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']
        elif coord == 'x':
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']['x']
        elif coord == 'y':
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']['y']
        elif coord == 'z':
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']['z']
        else:
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']

    def set_inventory(self):
        self.query['inv'] = True

    def get_inventory(self, item=False, quantity=False):
        """

        :param item: None, String, List<String>
        No item returns the full inv, a string returns that item or False, a list of strings returns the first of
        those items to be found or False
        :return: {'x': 1738, 'y': 768, 'index': 0, 'id': 8007, 'quantity': 77} || False
        """
        if item:
            if 'inv' in self.game_data:
                if quantity:
                    return inv.get_item_quantity_in_inv(self.game_data['inv'], item)
                elif type(item) is list:
                    return inv.are_items_in_inventory_v2(self.game_data['inv'], item)
                else:
                    return inv.is_item_in_inventory_v2(self.game_data['inv'], item)
            else:
                return []
        else:
            return ('inv' in self.game_data and self.game_data['inv']) or []

    def set_shop_inventory(self):
        self.query['shopInv'] = True

    def get_shop_inventory(self, item=False, quantity=False):
        """

        :param item: None, String, List<String>
        No item returns the full inv, a string returns that item or False, a list of strings returns the first of
        those items to be found or False
        :return: {'x': 1738, 'y': 768, 'index': 0, 'id': 8007, 'quantity': 77} || False
        """
        if item:
            if 'shopInv' in self.game_data:
                if quantity:
                    return inv.get_item_quantity_in_inv(self.game_data['shopInv'], item)
                elif type(item) is list:
                    return inv.are_items_in_inventory_v2(self.game_data['shopInv'], item)
                else:
                    return inv.is_item_in_inventory_v2(self.game_data['shopInv'], item)
            else:
                return []
        else:
            return ('shopInv' in self.game_data and self.game_data['shopInv']) or []

    def projectiles(self):
        self.query['projectiles'] = True

    def set_projectiles(self):
        self.query['projectiles'] = True

    def get_projectiles(self):
        return 'projectiles' in self.game_data and self.game_data['projectiles']

    def set_projectiles_v2(self):
        self.query['projectilesV2'] = True

    def get_projectiles_v2(self):
        return ('projectilesV2' in self.game_data and self.game_data['projectilesV2']) or []

    def set_chat_options(self):
        self.query['chatOptions'] = True

    def get_chat_options(self, option=False, fuzzy=False):
        if not option or not ('chatOptions' in self.game_data and self.game_data['chatOptions']):
            return 'chatOptions' in self.game_data and self.game_data['chatOptions']
        for i, stored_option in enumerate(self.game_data['chatOptions']):
            if stored_option.lower() == option.lower() or (fuzzy and option.lower() in stored_option.lower()):
                return i
        return False

    def is_fishing(self):
        self.query['isFishing'] = True

    def set_is_fishing(self):
        self.query['isFishing'] = True

    def get_is_fishing(self):
        return 'isFishing' in self.game_data and self.game_data['isFishing']

    def is_mining(self):
        self.query['isMining'] = True

    def set_is_mining(self):
        self.query['isMining'] = True

    def get_is_mining(self):
        return 'isMining' in self.game_data and self.game_data['isMining']

    def widgets(self, widgets):
        if type(widgets) is not list:
            raise Exception('widgets must be a list, {} is not a valid value.'.format(widgets))
        if 'widgets' in self.query:
            self.query['widgets'] += widgets
        else:
            self.query['widgets'] = widgets

    def set_widgets(self, widgets):
        if type(widgets) is not set:
            raise Exception('widgets must be a set, {} is not a valid value.'.format(widgets))
        if 'widgets' in self.query:
            old_widgets = self.query['widgets']

            self.query['widgets'] = list(set(old_widgets).union(widgets))
        else:
            self.query['widgets'] = list(widgets)

    def get_widgets(self, widget=False):
        """

        :param widget: '608,11' || None
        :return: {'x': 576, 'y': 493, 'text': '', 'spriteID': -1, 'name': '', 'itemID': -1, 'xMin': 476, 'xMax': 676, 'yMin': 444, 'yMax': 496} || False
        """
        if widget:
            if 'widgets' in self.game_data and widget in self.game_data['widgets']:
                return self.game_data['widgets'][widget]
            else:
                return False
        return 'widgets' in self.game_data and self.game_data['widgets']

    def set_widgets_v2(self, widgets):
        if type(widgets) is not set:
            raise Exception('widgets must be a set, {} is not a valid value.'.format(widgets))
        if 'widgetsV2' in self.query:
            old_widgets = self.query['widgetsV2']

            self.query['widgetsV2'] = list(set(old_widgets).union(widgets))
        else:
            self.query['widgetsV2'] = list(widgets)

    def get_widgets_v2(self, widget=False):
        """

        :param widget: '608,11' || None
        :return: {'x': 576, 'y': 493, 'text': '', 'spriteID': -1, 'name': '', 'itemID': -1, 'xMin': 476, 'xMax': 676, 'yMin': 444, 'yMax': 496} || False
        """
        if widget:
            if 'widgets' in self.game_data and str(widget) in self.game_data['widgets']:
                return self.game_data['widgets'][str(widget)]
            else:
                return False
        return 'widgets' in self.game_data and self.game_data['widgets']

    def npcs(self, ids):
        self.query['npcsID'] = ids

    def set_npcs(self, ids):
        self.query['npcsID'] = ids

    def get_npcs(self, npc_id=None, interacting_with_me=False):
        if npc_id:
            if 'npcs' in self.game_data:
                for npc in self.game_data['npcs']:
                    if npc['id'] == npc_id \
                        and (
                            not interacting_with_me or
                            ('interacting' in npc and npc['interacting'].lower() == 'UtahDogs')
                    ):
                        return npc

            return False
        else:
            return 'npcs' in self.game_data and self.game_data['npcs']

    def set_npcs_by_name(self, ids):
        if type(ids) is not list:
            raise Exception('tiles must be a list, {} is not a valid value.'.format(ids))
        self.query['npcs'] = [i.upper() for i in ids]

    def get_npcs_by_name(self):
        """

        :return: [] OR  [{'x': 942, 'y': 439, 'name': 'Squire (Veteran)', 'id': 1773, 'dist': 3, 'graphic': -1, 'health': -1, 'scale': -1, 'x_coord': 2638, 'y_coord': 2656, 'compositionID': 1773}]

        """
        return 'npcs' in self.game_data and self.game_data['npcs']

    def set_var_player(self, ids):
        if type(ids) is not list:
            raise Exception('varp must be a list, {} is not a valid value.'.format(ids))
        self.query['varPlayer'] = ids

    def get_var_player(self, varp_id=False):
        """

        :param varp_id: None or String: '302'
        :return: 103 || False
        """
        if varp_id:
            if 'varPlayer' in self.game_data and varp_id in self.game_data['varPlayer']:
                return self.game_data['varPlayer'][varp_id]
            else:
                return False
        return 'varPlayer' in self.game_data and self.game_data['varPlayer']

    def set_tiles(self, tiles):
        if type(tiles) is not set:
            raise Exception('tiles must be a set, {} is not a valid value.'.format(tiles))
        if 'tiles' in self.query:
            old_tiles = self.query['tiles']
            self.query['tiles'] = list(set(old_tiles).union(tiles))
        else:
            self.query['tiles'] = list(tiles)

    def clear_tiles(self):
        self.query['tiles'] = []

    def get_tiles(self, tile=False):
        """

        :param tile: None or String: '3214,4355,3'
        :return: {'x': 960, 'y': 428} || False
        """
        if tile:
            if 'tiles' in self.game_data and tile in self.game_data['tiles']:
                return self.game_data['tiles'][tile]
            else:
                return False
        return 'tiles' in self.game_data and self.game_data['tiles']

    def set_varbit(self, varbit):
        self.query['varBit'] = varbit

    def get_varbit(self):
        return 'varBit' in self.game_data and self.game_data['varBit']

    def set_varbits(self, varbits):
        self.query['varBits'] = varbits

    def get_varbits(self, varbit=False):
        if varbit:
            if 'varBits' in self.game_data and varbit in self.game_data['varBits']:
                return self.game_data['varBits'][varbit]
            else:
                return False
        return 'varBits' in self.game_data and self.game_data['varBits']

    def set_skills(self, skills):
        if type(skills) is not set:
            raise Exception('skills must be a set, {} is not a valid value.'.format(skills))
        if 'skills' in self.query:
            old_skills = self.query['skills']
            self.query['skills'] = list(set(old_skills).union(skills))
        else:
            self.query['skills'] = list(skills)

    def get_skills(self, skill=False):
        if skill:
            if 'skills' in self.game_data and skill in self.game_data['skills']:
                return self.game_data['skills'][skill]
            else:
                return False
        return 'skills' in self.game_data and self.game_data['skills']

    def set_game_objects(self, tiles, objects):
        if type(tiles) is not set:
            raise Exception('tiles must be a set, {} is not a valid value.'.format(tiles))
        if type(objects) is not set:
            raise Exception('objects must be a set, {} is not a valid value.'.format(objects))
        # dont keep adding the same tiles/ objects to the query over and over
        # for a long running script, this could be thousands of dupes
        if 'gameObjectsV2' in self.query:
            old_tiles = self.query['gameObjectsV2']['tiles']
            old_objects = self.query['gameObjectsV2']['objects']
            self.query['gameObjectsV2']['tiles'] = list(set(old_tiles).union(tiles))
            self.query['gameObjectsV2']['objects'] = list(set(old_objects).union(objects))
        else:
            self.query['gameObjectsV2'] = {'tiles': list(tiles), 'objects': list(objects)}

    # Sometimes this ends up being a huge array of tiles which the server cant handle,
    # add the ability to clear out old tiles if that happens
    def clear_game_objects(self):
        self.query.get('gameObjectsV2', None)

    def get_game_objects(self, game_object=False):
        """

        :param game_object: string - '30920'
        :return: [{'x': 836, 'y': 189, 'dist': 13, 'x_coord': 3765, 'y_coord': 3880, 'id': 30920}] || []
        """
        if game_object:
            if 'gameObjectsV2' in self.game_data and game_object in self.game_data['gameObjectsV2']:
                return self.game_data['gameObjectsV2'][game_object]
            else:
                return []
        return 'gameObjectsV2' in self.game_data and self.game_data['gameObjectsV2'] or []

    def set_wall_objects(self, tiles, objects):
        if type(tiles) is not set:
            raise Exception('tiles must be a set, {} is not a valid value.'.format(tiles))
        if type(objects) is not set:
            raise Exception('objects must be a set, {} is not a valid value.'.format(objects))
        # dont keep adding the same tiles/ objects to the query over and over
        # for a long running script, this could be thousands of dupes
        if 'gameObjectsV2' in self.query:
            old_tiles = self.query['wallObjectsV2']['tiles']
            old_objects = self.query['wallObjectsV2']['objects']
            self.query['wallObjectsV2']['tiles'] = list(set(old_tiles).union(tiles))
            self.query['wallObjectsV2']['objects'] = list(set(old_objects).union(objects))
        else:
            self.query['wallObjectsV2'] = {'tiles': list(tiles), 'objects': list(objects)}

    def get_wall_objects(self, game_object=False):
        if game_object:
            if 'wallObjectsV2' in self.game_data and game_object in self.game_data['wallObjectsV2']:
                return self.game_data['wallObjectsV2'][game_object]
            else:
                return []
        return 'wallObjectsV2' in self.game_data and self.game_data['wallObjectsV2'] or []

    def set_deposit_box(self):
        self.query['depositBox'] = True

    def set_script_stats(self, fields):
        self.query['scriptStats'] = {
            #'Next Break: ': osrs.game.config['timings']['break_start'],
            #'Break End: ': osrs.game.config['timings']['break_end'],
            **fields
        }

    def get_deposit_box(self, item=False):
        """

        :param item: None, String, List<String>
        No item returns the full inv, a string returns that item or False, a list of strings returns the first of
        those items to be found or False
        :return: {'x': 1738, 'y': 768, 'index': 0, 'id': 8007, 'quantity': 77} || False
        """
        if item:
            if 'depositBox' in self.game_data:
                if type(item) is list:
                    return inv.are_items_in_inventory_v2(self.game_data['depositBox'], item)
                else:
                    return inv.is_item_in_inventory_v2(self.game_data['depositBox'], item)
            else:
                return False
        else:
            return 'depositBox' in self.game_data and self.game_data['depositBox']

    def set_bank(self):
        self.query['bank'] = True

    def get_bank(self, item=False):
        """

        :param item: None, String, List<String>
        No item returns the full inv, a string returns that item or False, a list of strings returns the first of
        those items to be found or False
        :return: {'x': 1738, 'y': 768, 'index': 0, 'id': 8007, 'quantity': 77} || False
        """
        if item:
            if 'bankItems' in self.game_data:
                if type(item) is list:
                    return inv.are_items_in_inventory_v2(self.game_data['bankItems'], item)
                else:
                    return inv.is_item_in_inventory_v2(self.game_data['bankItems'], item)
            else:
                return False
        else:
            return 'bankItems' in self.game_data and self.game_data['bankItems']

    def set_equipment(self):
        self.query['equipment'] = True

    def get_equipment(self, item=False):
        if item:
            if 'equipment' in self.game_data:
                for equipment in self.game_data['equipment']:
                    if equipment:
                        return True
                return False
            else:
                return False
        return 'equipment' in self.game_data \
               and self.game_data['equipment']

    def set_canvas(self):
        self.query['canvas'] = True

    def get_canvas(self):
        return 'canvas' in self.game_data and self.game_data['canvas']

    def set_surrounding_ground_items(self, distance, loc):
        tiles = util.generate_surrounding_tiles_from_point(distance, loc)
        items = []
        for tile in tiles:
            items.append({
                'tile': tile,
                'object': '20997'
            })
        self.query['allGroundItems'] = items

    def get_surrounding_ground_items(self):
        return 'allGroundItems' in self.game_data and self.game_data['allGroundItems']

    def set_objects(self, tiles, objects, object_type: ObjectTypes):
        search_value = f'{object_type}ObjectsV2'
        if type(tiles) is not set:
            raise Exception('tiles must be a set, {} is not a valid value.'.format(tiles))
        if type(objects) is not set:
            raise Exception('objects must be a set, {} is not a valid value.'.format(objects))
        # dont keep adding the same tiles/ objects to the query over and over
        # for a long running script, this could be thousands of dupes
        if search_value in self.query:
            old_tiles = self.query[search_value]['tiles']
            old_objects = self.query[search_value]['objects']
            self.query[search_value]['tiles'] = list(set(old_tiles).union(tiles))
            self.query[search_value]['objects'] = list(set(old_objects).union(objects))
        else:
            self.query[search_value] = {'tiles': list(tiles), 'objects': list(objects)}

    # Sometimes this ends up being a huge array of tiles which the server cant handle,
    # add the ability to clear out old tiles if that happens
    def clear_objects(self, object_type: ObjectTypes):
        value = f'type{object_type}ObjectsV2'
        self.query.get(value, None)

    def get_objects(self, object_type: ObjectTypes, game_object=False, ):
        """

        :param object_type: ObjectTypes - 'wall'
        :param game_object: string - '30920'
        :return: [{'x': 836, 'y': 189, 'dist': 13, 'x_coord': 3765, 'y_coord': 3880, 'id': 30920}] || []
        """
        search_value = f'{object_type}ObjectsV2'
        if game_object:
            if search_value in self.game_data and game_object in self.game_data[search_value]:
                return self.game_data[search_value][game_object]
            else:
                return []
        return search_value in self.game_data and self.game_data[search_value] or []

    def set_herbiboar(self):
        self.query['herbiboar'] = True

    def get_herbiboar(self):
        return 'herbiboar' in self.game_data and self.game_data['herbiboar']

    def set_slayer(self):
        self.query['slayer'] = True

    def get_slayer(self):
        """

        :return: {'area': '', 'amount': '35', 'monster': 'Iron Dragons'}
        """

        return 'slayer' in self.game_data and self.game_data['slayer']
        #return {'area': '', 'amount': '89', 'monster': 'Wyrms'}

    def set_spot_anims(self):
        self.query['spotAnims'] = True

    def get_spot_anims(self):
        """
        :return: False :: [1845, 1846]
        """

        return 'spotAnims' in self.game_data and self.game_data['spotAnims']

    def set_target_obj(self):
        self.query['getTargetObj'] = True

    def get_target_obj(self):
        return 'targetObj' in self.game_data and self.game_data['targetObj']

    def set_ground_items(self, tiles):
        items = []
        for tile in tiles:
            items.append({
                'tile': tile,
                'object': '20997'
            })
        self.query['groundItemsV2'] = items

    def get_ground_items(self):
        return 'groundItemsV2' in self.game_data and self.game_data['groundItemsV2']

    def clear_query(self):
        self.query = {}

    def set_objects_v2(self, object_type: str, objects, dist=-1):
        object_type = object_type.lower()
        if type(objects) is not set:
            raise Exception('objects must be a set, {} is not a valid value.'.format(objects))
        # dont keep adding the same tiles/ objects to the query over and over
        # for a long running script, this could be thousands of dupes
        if 'allObjects' in self.query:
            self.query['allObjects'][object_type] = list(
                set(
                    self.query['allObjects'][object_type]).union(
                    set(
                        # coerce any strings to ints
                        map(int, objects)
                    )
                )
            )
        else:
            self.query['allObjects'] = {
                'game': [],
                'wall': [],
                'decorative': [],
                'ground': [],
                'ground_items': [],
                'graphics': [],
                'dist': dist
            }
            self.query['allObjects'][object_type] = list(objects)

    def get_objects_v2(self, object_type: str, game_object=False, dist=104):
        """

        :param object_type: 'wall' || 'game' || 'ground' || 'decorative' || 'ground_items' || 'graphics'
        :param game_object: string - '30920'
        :return: [{'x': 836, 'y': 189, 'dist': 13, 'x_coord': 3765, 'y_coord': 3880, 'id': 30920}] || []
        """
        object_type = object_type.lower()
        if 'allObjects' not in self.game_data:
            return []

        selected_object_type = self.game_data['allObjects'][object_type]
        if game_object:
            selected_object_type = list(
                filter(
                    lambda obj: obj['id'] == int(game_object) and obj['dist'] <= dist, selected_object_type
                )
            )
        if selected_object_type and len(selected_object_type) > 0:
            return selected_object_type
        else:
            return []

    def set_yaw(self, value):
        self.query['setYaw'] = value

    def set_mta_data(self):
        self.query['mta'] = True

    def get_mta_data(self):
        return 'mta' in self.game_data and self.game_data['mta']

    def query_backend(self):
        '''print("\t«{}»\tLine number in which the function is defined.".
              format(inspect.getsourcelines(self.query_backend)[1]))
        print("\t«{}»\tLine from which the function has been called.".
              format(inspect.stack()[1][2]))
        print("\t«{}»\tInvoking/calling function.".format(inspect.stack()[1][3]))'''
        self.game_data = server.query_game_data(self.query, config['port'])
        return self.game_data
