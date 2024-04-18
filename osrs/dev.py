import math
import os
import yaml
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DuplicateFilter(logging.Filter):

    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)


def instantiate_logger():
    logger = logging.getLogger("GoonLite")
    logger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())
    ch.addFilter(DuplicateFilter())
    logger.addHandler(ch)
    return logger


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


def load_yaml():
    with open("{}/config.yaml".format(ROOT_DIR[:-5]), "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print('Failed to load configuration.')
            print(exc)
            return

