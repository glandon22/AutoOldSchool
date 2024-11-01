from datetime import datetime, timedelta


import osrs

temp_arrow = '754,74'
red_temp = '754,21'
yellow_temp = '754,20'
green_temp = '754,19'
station_arrow = '754,78'

def load_crucible(items):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_chat_options()
    qh.set_canvas()
    qh.set_objects_v2('game', {44776})
    last_crucible = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_chat_options('All'):
            osrs.keeb.write(str(qh.get_chat_options('All')))
        elif (qh.get_inventory(items)
              and qh.get_objects_v2('game', 44776)
              and (datetime.now() - last_crucible).total_seconds() > 7.0):
            osrs.move.right_click_v6(
                qh.get_inventory(items),
                'Use',
                qh.get_canvas(),
                in_inv=True
            )
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 44776)[0])
            last_crucible = datetime.now()
        elif not qh.get_inventory(items):
            return


def get_commission():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'231,6'})
    qh.set_npcs(['11472'])
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_widgets('231,6') and qh.get_widgets('231,6')['text']:
            res = []
            comm = qh.get_widgets('231,6')['text'].split('<col=ef1020>')
            for word in comm:
                if '<' in word:
                    attr = word.split('<')
                    if ' ' in attr[0]:
                        res += attr[0].split(' ')
                    else:
                        res += [attr[0]]
            return res
        elif qh.get_npcs():
            osrs.move.right_click_v6(
                qh.get_npcs()[0],
                'Commission',
                qh.get_canvas(),
                in_inv=True
            )

def config_open():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'718,1'})
    qh.query_backend()
    if qh.get_widgets('718,1'):
        return True

def calc_values(commission):
    qh = osrs.queryHelper.QueryHelper()
    for i in range(0, 9):
        qh.set_widgets({
            f"718,9,{85 + 17 * i}",
            f"718,9,{92 + 17 * i}",
            f"718,9,{93 + 17 * i}",
            f"718,9,{96 + 17 * i}",
            f"718,9,{97 + 17 * i}",
            f"718,9,{100 + 17 * i}",
            f"718,9,{101 + 17 * i}",
        })
    while True:
        qh.query_backend()
        if qh.get_widgets():
            break
    max_point_dict = {}
    for i in range(0, 9):
        # check if full row exists
        if qh.get_widgets(f"718,9,{85 + 17 * i}"):
            max_point_dict[f"718,9,{85 + 17 * i}"] = 0
            # check if first type is a match
            if qh.get_widgets(f"718,9,{92 + 17 * i}") and qh.get_widgets(f"718,9,{92 + 17 * i}")['text'] in commission:
                max_point_dict[f"718,9,{85 + 17 * i}"] += int(qh.get_widgets(f"718,9,{93 + 17 * i}")['text'])
            if qh.get_widgets(f"718,9,{96 + 17 * i}") and qh.get_widgets(f"718,9,{96 + 17 * i}")['text'] in commission:
                max_point_dict[f"718,9,{85 + 17 * i}"] += int(qh.get_widgets(f"718,9,{97 + 17 * i}")['text'])
            if qh.get_widgets(f"718,9,{100 + 17 * i}") and qh.get_widgets(f"718,9,{100 + 17 * i}")['text'] in commission:
                max_point_dict[f"718,9,{85 + 17 * i}"] += int(qh.get_widgets(f"718,9,{101 + 17 * i}")['text'])
    max_pts = 0
    name = None
    for key in max_point_dict:
        if max_point_dict[key] > max_pts:
            max_pts = max_point_dict[key]
            name = key
    return name

def configure_crucible(commission):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'718,12,9', '718,12,0', '718,6', '718,12,18'})
    osrs.move.interact_with_object_v3(
        44777,
        custom_exit_function=config_open,
        timeout=7,
        right_click_option='Setup'
    )
    target = calc_values(commission)
    qh.set_widgets(
        {target}
    )
    while True:
        qh.query_backend()
        if qh.get_widgets('718,12,18'):
            osrs.move.fast_click_v2(qh.get_widgets('718,12,18'))
            osrs.clock.sleep_one_tick()
            break
    while True:
        qh.query_backend()
        if qh.get_widgets(target):
            osrs.move.fast_click_v2(qh.get_widgets(target))
            break
    osrs.move.fast_click_v2(qh.get_widgets('718,12,9'))
    osrs.clock.sleep_one_tick()
    target = calc_values(commission)
    qh.set_widgets(
        {target}
    )
    while True:
        qh.query_backend()
        if qh.get_widgets(target):
            osrs.move.fast_click_v2(qh.get_widgets(target))
            break
    osrs.move.fast_click_v2(qh.get_widgets('718,12,0'))
    osrs.clock.sleep_one_tick()
    target = calc_values(commission)
    qh.set_widgets(
        {target}
    )
    while True:
        qh.query_backend()
        if qh.get_widgets(target):
            osrs.move.fast_click_v2(qh.get_widgets(target))
            break
    osrs.move.fast_click_v2(qh.get_widgets('718,6'))


def holding_preform():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_equipment()
    qh.query_backend()
    if osrs.item_ids.PREFORM in qh.get_equipment():
        return True


def heat_sword(dest='red'):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        red_temp, green_temp, yellow_temp, temp_arrow
    })
    qh.set_objects_v2('game', {44619, 44631})
    qh.set_player_animation()
    last_dunk = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        if (dest == 'red' and qh.get_widgets(temp_arrow)
                and qh.get_widgets(red_temp)
                and qh.get_widgets(temp_arrow)['x'] >= qh.get_widgets(red_temp)['x']):
            osrs.dev.logger.info("Finished heating sword to red temp.")
            return
        elif (dest == 'yellow' and qh.get_widgets(temp_arrow)
                and qh.get_widgets(yellow_temp)
                and qh.get_widgets(temp_arrow)['x'] >= qh.get_widgets(yellow_temp)['x']):
            osrs.dev.logger.info("Finished heating sword to yellow temp.")
            return
        elif (dest == 'green' and qh.get_widgets(temp_arrow)
                and qh.get_widgets(green_temp)
                and qh.get_widgets(temp_arrow)['x'] >= qh.get_widgets(green_temp)['x']):
            osrs.dev.logger.info("Finished heating sword to green temp.")
            return
        elif qh.get_player_animation() == 827:
            osrs.dev.logger.info("Heating sword to continue hammering.")
            last_dunk = datetime.now()
        elif qh.get_objects_v2('game', 44631) and (datetime.now() - last_dunk).total_seconds() > 3:
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 44631)[0])


def hammer_sword(holder):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        holder, station_arrow, red_temp, temp_arrow
    })
    qh.set_objects_v2('game', {44619})
    qh.set_player_animation()
    last_dunk = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        # finished this step
        if (qh.get_widgets(station_arrow)
                and qh.get_widgets(holder)
                and qh.get_widgets(station_arrow)['x'] > qh.get_widgets(holder)['xMax']):
            return
        elif qh.get_widgets(temp_arrow) \
            and qh.get_widgets(red_temp) \
            and qh.get_widgets(temp_arrow)['x'] <= qh.get_widgets(red_temp)['xMin']:
                osrs.dev.logger.warning('Sword has gotten too cold while hammering - heating up.')
                heat_sword()
        elif qh.get_widgets(temp_arrow) \
            and qh.get_widgets(red_temp) \
            and qh.get_widgets(temp_arrow)['x'] >= qh.get_widgets(red_temp)['xMax']:
                osrs.dev.logger.warning('Sword has gotten too hot while hammering - cooling.')
                cool_sword('red')
        elif qh.get_player_animation() != 9455 and qh.get_objects_v2('game', 44619):
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 44619)[0])


def cool_sword(dest):
    '''

    :param dest: 'green' || 'yellow' || 'red'
    :return:
    '''
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        yellow_temp, green_temp, temp_arrow, red_temp
    })
    qh.set_objects_v2('game', {44632})
    qh.set_player_animation()
    last_dunk = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        if (dest == 'red' and qh.get_widgets(temp_arrow)
                and qh.get_widgets(red_temp)
                and qh.get_widgets(temp_arrow)['x'] <= qh.get_widgets(red_temp)['xMax']):
            osrs.dev.logger.info("Finished cooling sword - in upper red quadrant.")
            return
        elif (dest == 'yellow' and qh.get_widgets(temp_arrow)
                and qh.get_widgets(yellow_temp)
                and qh.get_widgets(temp_arrow)['x'] <= qh.get_widgets(yellow_temp)['x']):
            osrs.dev.logger.info("Finished cooling sword - in lower yellow quadrant.")
            return
        elif (dest == 'green' and qh.get_widgets(temp_arrow)
                and qh.get_widgets(green_temp)
                and qh.get_widgets(temp_arrow)['x'] <= qh.get_widgets(green_temp)['xMax']):
            osrs.dev.logger.info("Finished cooling sword - in upper green quadrant.")
            return
        elif qh.get_player_animation() == 832:
            osrs.dev.logger.info("Cooling sword to continue working.")
            last_dunk = datetime.now()
        elif qh.get_objects_v2('game', 44632) and (datetime.now() - last_dunk).total_seconds() > 3:
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 44632)[0])

def grind_sword(holder):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        holder, station_arrow, yellow_temp, temp_arrow
    })
    qh.set_objects_v2('game', {44620})
    qh.set_player_animation()
    last_grind = datetime.now() - timedelta(hours=1)
    # 9454
    while True:
        qh.query_backend()
        # finished this step
        if (qh.get_widgets(station_arrow)
                and qh.get_widgets(holder)
                and qh.get_widgets(station_arrow)['x'] > qh.get_widgets(holder)['xMax']):
            return
        elif qh.get_widgets(temp_arrow) \
                and qh.get_widgets(yellow_temp) \
                and qh.get_widgets(temp_arrow)['x'] >= qh.get_widgets(yellow_temp)['xMax']:
            osrs.dev.logger.warning('Sword has gotten too hot while grinding - cooling down.')
            cool_sword('yellow')
        elif qh.get_widgets(temp_arrow) \
                and qh.get_widgets(yellow_temp) \
                and qh.get_widgets(temp_arrow)['x'] <= qh.get_widgets(yellow_temp)['xMin']:
            osrs.dev.logger.warning('Sword has gotten too cold while grinding - heating up.')
            heat_sword('yellow')
        elif qh.get_player_animation() == 9454:
            last_grind = datetime.now()
        elif (qh.get_player_animation() != 9454
              and qh.get_objects_v2('game', 44620)
              and (datetime.now() - last_grind).total_seconds() > 2):
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 44620)[0])


def polish_sword(holder):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        holder, station_arrow, green_temp, temp_arrow
    })
    qh.set_objects_v2('game', {44621})
    qh.set_player_animation()
    last_grind = datetime.now() - timedelta(hours=1)
    # 9454
    while True:
        qh.query_backend()
        # finished this step
        if (qh.get_widgets(station_arrow)
                and qh.get_widgets(holder)
                and qh.get_widgets(station_arrow)['x'] > qh.get_widgets(holder)['xMax']):
            return
        elif qh.get_widgets(temp_arrow) \
                and qh.get_widgets(green_temp) \
                and qh.get_widgets(temp_arrow)['x'] >= qh.get_widgets(green_temp)['xMax']:
            osrs.dev.logger.warning('Sword has gotten too hot while polishing - cooling down.')
            cool_sword('green')
        elif qh.get_widgets(temp_arrow) \
                and qh.get_widgets(green_temp) \
                and qh.get_widgets(temp_arrow)['x'] <= qh.get_widgets(green_temp)['xMin']:
            osrs.dev.logger.warning('Sword has gotten too cold while polishing - heating up.')
            heat_sword('green')
        elif qh.get_player_animation() == 9454:
            last_grind = datetime.now()
        elif (qh.get_player_animation() != 9454
              and qh.get_objects_v2('game', 44621)
              and (datetime.now() - last_grind).total_seconds() > 2):
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 44621)[0])

def smith_sword():
    for i in range(0, 7):
        step_holder = f"754,75,{0 + i * 11}"
        step_icon = f"754,75,{10 + i * 11}"
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({
            temp_arrow, red_temp, yellow_temp, green_temp, station_arrow,
            step_holder, step_icon
        })
        while True:
            qh.query_backend()
            if qh.get_widgets(step_icon):
                if qh.get_widgets(step_icon)['spriteID'] == 4442:
                    hammer_sword(step_holder)
                    break
                elif qh.get_widgets(step_icon)['spriteID'] == 4443:
                    grind_sword(step_holder)
                    break
                elif qh.get_widgets(step_icon)['spriteID'] == 4444:
                    polish_sword(step_holder)
                    break
            else:
                return


def returned_sword():
    osrs.keeb.press_key('space')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.query_backend()
    if qh.get_chat_options('Yes.'):
        osrs.keeb.write(str(qh.get_chat_options('Yes.')))
        return True


while True:
    osrs.game.break_manager_v4({
        'intensity': 'high',
        'login': False,
        'logout': False
    })
    commission1 = get_commission()
    osrs.bank.banking_handler({
        'search': [{'query': 'giants', 'items': [
            osrs.item_ids.ADAMANT_PLATEBODY,
            osrs.item_ids.ADAMANT_PLATEBODY,
            osrs.item_ids.ADAMANT_PLATEBODY,
            osrs.item_ids.MITHRIL_PLATEBODY,
            osrs.item_ids.MITHRIL_PLATEBODY,
            osrs.item_ids.MITHRIL_PLATEBODY,
            osrs.item_ids.MITHRIL_PLATEBODY,
        ]}]
    })
    configure_crucible(commission1)
    load_crucible([osrs.item_ids.ADAMANT_PLATEBODY, osrs.item_ids.MITHRIL_PLATEBODY])
    osrs.move.interact_with_object_v3(
        44776,
        custom_exit_function=lambda start: (datetime.now() - start).total_seconds() > 9,
        custom_exit_function_arg=datetime.now()
    )
    osrs.move.interact_with_object_v3(
        44777,
        custom_exit_function=holding_preform,
        right_click_option='Pick-up',
        timeout=7
    )
    smith_sword()
    osrs.move.interact_with_npc(
        11472,
        custom_exit_function=returned_sword,
        right_click_option='Hand-in',
        timeout=10
    )
