# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from combat import slayer_killer



qh = osrs.queryHelper.QueryHelper()
qh.set_npcs_by_name([])
while True:
    qh.query_backend()
    print('p', qh.get_npcs_by_name())