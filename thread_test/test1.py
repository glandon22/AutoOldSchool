# 2134,9305,0
import datetime

import osrs
'''from osrs.item_ids import ItemIDs
from combat import slayer_killer



loot = osrs.loot.Loot()
loot.retrieve_loot()'''

qh = osrs.queryHelper.QueryHelper()
qh.set_active_prayers()
while True:
    qh.query_backend()
    print(qh.get_active_prayers())