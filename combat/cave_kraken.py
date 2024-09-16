import datetime
import osrs
from slayer.transport_functions import kraken_cove_private

logger = osrs.dev.instantiate_logger()


script_config = {
    'intensity': 'high',
    'login': kraken_cove_private,
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    asleep_kraken_id = '496'
    awake_kraken_id = '494'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_slayer()
    qh.set_interating_with()
    qh.set_npcs([asleep_kraken_id, awake_kraken_id])
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
    last_explosive = datetime.datetime.now() - datetime.timedelta(hours=1)
    loot_handler = osrs.loot.Loot()
    while True:
        qh.query_backend()
        if not qh.get_slayer() or not qh.get_slayer()['monster']:
            logger.info('task complete')
            return True

        asleep_kraken = list(filter(lambda npc: str(npc['id']) == asleep_kraken_id, qh.get_npcs()))
        awake_kraken = list(filter(lambda npc: str(npc['id']) == awake_kraken_id, qh.get_npcs()))
        if qh.get_skills('hitpoints')['boostedLevel'] < 40:
            logger.info('Health below 40, eating.')
            result = osrs.combat_utils.food_handler(qh, 40)
            if not result:
                return False
        elif qh.get_interating_with() and awake_kraken:
            logger.info('In combat with Kraken.')
        elif len(awake_kraken) > 0 and awake_kraken[0]['health'] != 0:
            logger.info('Attacking a vulnerable kraken')
            osrs.move.fast_click(awake_kraken[0])
        elif not qh.get_interating_with() and len(asleep_kraken) > 0 and (datetime.datetime.now() - last_explosive).total_seconds() > 15:
            osrs.game.break_manager_v4(script_config)
            kraken = asleep_kraken[0]
            explosive = qh.get_inventory(osrs.item_ids.FISHING_EXPLOSIVE_6664)
            if not explosive:
                return False
            if len(kraken) > 0:
                logger.info('Throwing an explosive to awaken Kraken.')
                osrs.move.fast_click(explosive)
                osrs.move.fast_click(kraken)
                last_explosive = datetime.datetime.now()
        osrs.combat_utils.pot_handler(qh, osrs.combat_utils.PotConfig(super_def=True).asdict())
        loot_handler.retrieve_loot()
        osrs.keeb.press_key('esc')

