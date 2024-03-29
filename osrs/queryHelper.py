import osrs.server as server
import osrs.dev as dev
import osrs.inv as inv
import osrs.util as util
import logging
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

    def set_interating_with(self):
        self.query['interactingWith'] = True

    def get_interating_with(self):
        return 'interactingWith' in self.game_data and self.game_data['interactingWith']

    def player_animation(self):
        self.query['playerAnimation'] = True

    def set_player_animation(self):
        self.query['playerAnimation'] = True

    def get_player_animation(self):
        return 'playerAnimation' in self.game_data and self.game_data['playerAnimation']

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
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']['']
        else:
            return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']

    def inventory(self):
        self.query['inv'] = True

    def set_inventory(self):
        self.query['inv'] = True

    def get_inventory(self, item=False):
        """

        :param item: None, String, List<String>
        No item returns the full inv, a string returns that item or False, a list of strings returns the first of
        those items to be found or False
        :return: {'x': 1738, 'y': 768, 'index': 0, 'id': 8007, 'quantity': 77} || False
        """
        if item:
            if 'inv' in self.game_data:
                if type(item) is list:
                    return inv.are_items_in_inventory_v2(self.game_data['inv'], item)
                else:
                    return inv.is_item_in_inventory_v2(self.game_data['inv'], item)
            else:
                return False
        else:
            return 'inv' in self.game_data and self.game_data['inv']

    def projectiles(self):
        self.query['projectiles'] = True

    def set_projectiles(self):
        self.query['projectiles'] = True

    def get_projectiles(self):
        return 'projectiles' in self.game_data and self.game_data['projectiles']

    def set_projectiles_v2(self):
        self.query['projectilesV2'] = True

    def get_projectiles_v2(self):
        return 'projectilesV2' in self.game_data and self.game_data['projectilesV2']

    def set_chat_options(self):
        self.query['chatOptions'] = True

    def get_chat_options(self):
        return 'chatOptions' in self.game_data and self.game_data['chatOptions']

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

    def npcs(self, ids):
        self.query['npcsID'] = ids

    def set_npcs(self, ids):
        self.query['npcsID'] = ids

    def get_npcs(self):
        return 'npcs' in self.game_data and self.game_data['npcs']

    def set_tiles(self, tiles):
        if type(tiles) is not set:
            raise Exception('tiles must be a set, {} is not a valid value.'.format(tiles))
        if 'tiles' in self.query:
            old_tiles = self.query['tiles']
            self.query['tiles'] = list(set(old_tiles).union(tiles))
        else:
            self.query['tiles'] = list(tiles)

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

    def get_deposit_box(self, item=False):
        """

        :param item: None, String, List<String>
        No item returns the full inv, a string returns that item or False, a list of strings returns the first of
        those items to be found or False
        :return: {'x': 1738, 'y': 768, 'index': 0, 'id': 8007, 'quantity': 77} || False
        """
        logging.info('getting deposit data.')
        if item:
            if 'depositBox' in self.game_data:
                if type(item) is list:
                    logging.info('got a list of items to search for: {}'.format(item))
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
        logging.info('getting bank data.')
        if item:
            if 'bankItems' in self.game_data:
                if type(item) is list:
                    logging.info('got a list of items to search for: {}'.format(item))
                    return inv.are_items_in_inventory_v2(self.game_data['bankItems'], item)
                else:
                    return inv.is_item_in_inventory_v2(self.game_data['bankItems'], item)
            else:
                return False
        else:
            return 'bankItems' in self.game_data and self.game_data['bankItems']

    def set_equipment(self):
        self.query['equipmentInv'] = True

    def get_equipment(self, item=False):
        if item:
            if 'equipmentInv' in self.game_data:
                for equipment in self.game_data['equipmentInv']:
                    if equipment['id'] == int(item):
                        return equipment
                return False
            else:
                return False
        return 'equipmentInv' in self.game_data and self.game_data['equipmentInv']

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

    def get_objects(self, object_type: ObjectTypes, game_object=False,):
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

    def clear_query(self):
        self.query = {}

    def query_backend(self):
        '''print("\t«{}»\tLine number in which the function is defined.".
              format(inspect.getsourcelines(self.query_backend)[1]))
        print("\t«{}»\tLine from which the function has been called.".
              format(inspect.stack()[1][2]))
        print("\t«{}»\tInvoking/calling function.".format(inspect.stack()[1][3]))'''
        self.game_data = server.query_game_data(self.query, config['port'])
        return self.game_data
