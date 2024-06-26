# 2134,9305,0
import datetime

import pyautogui

import osrs
from combat import slayer_killer
pot_config = slayer_killer.PotConfig(super_str=True)
slayer_killer.main(
    'suqah',
    pot_config.asdict(), 35,
    attackable_area={'x_min': 2090, 'x_max': 2111, 'y_min': 3847, 'y_max': 3878},
)
