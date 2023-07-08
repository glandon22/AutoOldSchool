import osrs.server as server
import osrs.dev as dev
import osrs.inv as inv
import logging

logging.basicConfig(filename='test',
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

config = dev.load_yaml()


class QueryHelper:
    query = {}
    game_data = {}

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

    def get_player_world_location(self):
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
        print(self.query['widgets'])

    def get_widgets(self, widget=False):
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

    def get_game_objects(self, game_object=False):
        if game_object:
            if 'gameObjectsV2' in self.game_data and game_object in self.game_data['gameObjectsV2']:
                return self.game_data['gameObjectsV2'][game_object]
            else:
                return []
        return 'gameObjectsV2' in self.game_data and self.game_data['gameObjectsV2'] or []

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
                    else:
                        return False
            else:
                return False
        return 'equipmentInv' in self.game_data and self.game_data['equipmentInv']

    def query_backend(self):
        self.game_data = server.query_game_data(self.query, config['port'])
        return self.game_data
