import math
import os
import yaml


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def point_dist(x1, y1, x2, y2):
    return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def config_loader():
    config = {
        'port': '56799',
        'password': 'pass_70',
        'timings': {
            'script_start': None,
            'break_start': None,
            'break_end': None,
            'on_break': False
        },
        'high_intensity_script': {
            'max_session': 48,
            'min_session': 42,
            'max_rest': 10,
            'min_rest': 7
        },
        'low_intensity_script': {
            'max_session': 59,
            'min_session': 53,
            'max_rest': 10,
            'min_rest': 7
        }
    }

    yaml_output = yaml.dump(config, sort_keys=True)

    print(yaml_output)


def load_yaml():
    with open("{}/config.yaml".format(ROOT_DIR[:-5]), "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print('Failed to load configuration.')
            print(exc)
            return