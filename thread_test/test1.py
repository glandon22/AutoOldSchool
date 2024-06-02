import datetime

import osrs
from combat import slayer_killer

pot_config = slayer_killer.PotConfig(super_combat=True)
from osrs.item_ids import ItemIDs


qh = osrs.queryHelper.QueryHelper()
qh.set_spot_anims()
while True:
    qh.query_backend()
    print("--------------------------------------------------")
    print(qh.get_spot_anims())
    print("--------------------------------------------------")
