import datetime

import osrs
from combat import slayer_killer
pot_config = slayer_killer.PotConfig(super_combat=True)

slayer_killer.main(
    'dagannoth',
    pot_config.asdict(), 35, -1, -1, -1,
    attackable_area={'x_min': 2442, 'x_max': 2487, 'y_min': 10125, 'y_max': 10163}
)