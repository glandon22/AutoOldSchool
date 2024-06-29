
import osrs

q = {
    'allObjects': {
        'game': [29091],
        'wall': [],
        'decorative': [],
        'ground': [],

    }
}
d = osrs.server.query_game_data(q)
print(d)