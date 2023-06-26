import osrs.server as server
import osrs.dev as dev

config = dev.load_yaml()


class QueryHelper:
    query = {}
    game_data = {}

    def player_animation(self):
        self.query['playerAnimation'] = True

    def get_player_animation(self):
        return 'playerAnimation' in self.game_data and self.game_data['playerAnimation']

    def player_world_location(self):
        self.query['playerWorldPoint'] = True

    def get_player_world_location(self):
        return 'playerWorldPoint' in self.game_data and self.game_data['playerWorldPoint']

    def inventory(self):
        self.query['inv'] = True

    def get_inventory(self):
        return 'inv' in self.game_data and self.game_data['inv']

    def is_mining(self):
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

    def get_widgets(self):
        return 'widgets' in self.game_data and self.game_data['widgets']

    def query_backend(self):
        self.game_data = server.query_game_data(self.query, config['port'])
        return self.game_data
