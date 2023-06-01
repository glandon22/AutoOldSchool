import datetime

from osrs_utils import general_utils

port = 56799
EMPTY_PLOT = '27383'
start_point_diff = {
    'x': 4,
    'y': -12
}

plot_offsets_from_anchor = [
    # Place in order you want to plant
    {
        'x': 1,
        'y': -10
    },
    {
        'x': 6,
        'y': -10
    },
    {
        'x': 6,
        'y': -7
    },
    {
        'x': 1,
        'y': -7
    },
    {
        'x': 1,
        'y': -4
    },
    {
        'x': 6,
        'y': -4
    },
    {
        'x': 6,
        'y': -1
    },
    {
        'x': 1,
        'y': -1
    },
    {
        'x': 1,
        'y': 3
    },
    {
        'x': 6,
        'y': 3
    },
    {
        'x': 6,
        'y': 6
    },
    {
        'x': 3,
        'y': 6
    },
    {
        'x': 3,
        'y': 9
    },
    {
        'x': 6,
        'y': 9
    },
    {
        'x': 6,
        'y': 12
    },
    {
        'x': 3,
        'y': 12
    },
]


def fill_watering_cans():
    while True:
        inv = general_utils.get_inv(port)
        not_full_can = general_utils.are_items_in_inventory_v2(inv, [5331, 5333, 5334, 5335, 5336, 5337, 5338, 5339])
        if not_full_can:
            general_utils.move_and_click(not_full_can['x'], not_full_can['y'], 3, 3)
            water = general_utils.get_surrounding_game_objects(10, ['5598'], port)
            if '5598' in water:
                general_utils.move_and_click(water['5598']['x'], water['5598']['y'], 2, 2)
                general_utils.random_sleep(0.6, 0.7)
        else:
            break


def determine_anchor_tile():
    while True:
        water = general_utils.get_surrounding_game_objects(25, ['5598'], port)
        if '5598' in water:
            return water['5598']


def place_seed(seed, plot):
    general_utils.move_and_click(seed['x'], seed['y'], 3, 3)
    general_utils.move_and_click(plot['x'], plot['y'], 3, 3)


def plant_seeds(anchor):
    for plot in plot_offsets_from_anchor:
        inv = general_utils.get_inv(port)
        seed = general_utils.is_item_in_inventory_v2(inv, '13423')
        if not seed:
            print('OUT OF SEEDS')
            exit(1)
        plot = general_utils.get_game_object(
            '{},{},0'.format(anchor['x_coord'] + plot['x'], anchor['y_coord'] + plot['y']),
            EMPTY_PLOT,
            port
        )
        if plot:
            place_seed(seed, plot)
            start_time = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - start_time).total_seconds() > 4:
                    print('timeout')
                    plot = general_utils.get_game_object(
                        '{},{},0'.format(anchor['x_coord'] + plot['x'], anchor['y_coord'] + plot['y']),
                        EMPTY_PLOT,
                        port
                    )
                    place_seed(seed, plot)

                planted = general_utils.get_game_object(
                    '{},{},0'.format(anchor['x_coord'] + plot['x'], anchor['y_coord'] + plot['y']),
                    EMPTY_PLOT,
                    port
                )
                print('planted', planted)
                if not planted:
                    print('planted was false')
                    break


def main():
    anchor = determine_anchor_tile()
    fill_watering_cans()
    general_utils.run_towards_square_v2(
        {'x': anchor['x_coord'] + start_point_diff['x'], 'y': anchor['y_coord'] + start_point_diff['y'], 'z': 0},
        port
    )
    plant_seeds(anchor)

anchor = determine_anchor_tile()
for plot in plot_offsets_from_anchor:
    plot = general_utils.get_game_object(
        '{},{},0'.format(anchor['x_coord'] + plot['x'], anchor['y_coord'] + plot['y']),
        EMPTY_PLOT,
        port
    )
    print(plot)