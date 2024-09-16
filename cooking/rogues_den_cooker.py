import datetime

import osrs

fire_id = 43475


def cook_fish(qh: osrs.queryHelper.QueryHelper, fish):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets_v2(osrs.widget_ids.CHATBOX_SKILLING_INPUT_BOX) or not qh.get_inventory(fish):
            osrs.keeb.press_key('space')
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            break
        elif (qh.get_objects_v2('game', fire_id)
              and (datetime.datetime.now() - last_click).total_seconds() > 3):
            osrs.move.click(qh.get_objects_v2('game', fire_id)[0])
            last_click = datetime.datetime.now()


def main(fish, goal=99):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['emerald benedict'])
    qh.set_inventory()
    qh.set_widgets_v2({
        osrs.widget_ids.CHATBOX_SKILLING_INPUT_BOX,
        osrs.widget_ids.LEVEL_UP_SKILL,
    })
    qh.set_objects_v2('game', {fire_id})
    qh.set_skills({'cooking'})
    last_cooked = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_banked = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_skills('cooking') and qh.get_skills('cooking')['level'] >= goal:
            return

        if (qh.get_inventory(fish)
                and (qh.get_widgets_v2(osrs.widget_ids.LEVEL_UP_SKILL)
                     or (datetime.datetime.now() - last_cooked).total_seconds() > 75)):
            cook_fish(qh, fish)
            last_cooked = datetime.datetime.now()
        elif not qh.get_inventory(fish) and (datetime.datetime.now() - last_banked).total_seconds() > 2:
            osrs.game.talk_to_npc('emerald benedict', right_click=True)
            osrs.game.dialogue_handler(['Yes actually, can you help?'], timeout=1)
            osrs.bank.banking_handler({
                'dump_inv': True,
                'withdraw': [{
                    'items': [
                        {'id': fish, 'quantity': 'All'},
                    ]
                }]
            })
            last_banked = datetime.datetime.now()
            last_cooked = datetime.datetime.now() - datetime.timedelta(hours=1)
