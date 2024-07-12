import osrs
import util_functions
import transport_functions

dialogue = [
    "Yes.",
    "What's happened to her?",
    "Yes, I'll return it for you.",
    "I fear not a mere plague.",
    "I want to check anyway.",
    "I need permission to enter a plague house.",
    "This is urgent though! Someone's been kidnapped!",
    "This is really important though!",
    "Do you know what's in the cure?",
    "They won't listen to me!",
    "Okay, I'll look for it."
]


def get_picture():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.PICTURE.value):
        return True


def get_key():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.A_SMALL_KEY.value):
        return True


def click_water():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value))


def click_spade():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.SPADE.value):
        osrs.move.right_click_v6(
            qh.get_inventory(osrs.item_ids.ItemIDs.SPADE.value),
            'Use',
            qh.get_canvas(),
            in_inv=True
        )


def click_rope():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.ROPE.value):
        osrs.move.right_click_v6(
            qh.get_inventory(osrs.item_ids.ItemIDs.ROPE.value),
            'Use',
            qh.get_canvas(),
            in_inv=True
        )


def click_mask():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GAS_MASK.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.GAS_MASK.value))


def use_all_water():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value):
        return True


def make_cure():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.HANGOVER_CURE.value):
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('space')
            return
        elif (qh.get_inventory(osrs.item_ids.ItemIDs.CHOCOLATE_DUST.value)
              and qh.get_inventory(osrs.item_ids.ItemIDs.BUCKET_OF_MILK.value)):
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.CHOCOLATE_DUST.value))
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.BUCKET_OF_MILK.value))
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
        elif (qh.get_inventory(osrs.item_ids.ItemIDs.SNAPE_GRASS.value)
              and qh.get_inventory(osrs.item_ids.ItemIDs.CHOCOLATEY_MILK.value)):
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.SNAPE_GRASS.value))
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.CHOCOLATEY_MILK.value))
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()


def open_cover():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {2544})
    qh.query_backend()
    if qh.get_objects_v2('game', 2544):
        return True


def read_scroll():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({util_functions.main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(util_functions.main_chat_widget):
            osrs.clock.sleep_one_tick()
            util_functions.dialogue_handler([])
            return
        elif qh.get_inventory(osrs.item_ids.ItemIDs.ARDOUGNE_TELEPORT_SCROLL.value):
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.ARDOUGNE_TELEPORT_SCROLL.value))
            osrs.clock.random_sleep(1, 1.1)


def main():
    util_functions.talk_to_npc('edmond')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(
        1535, 'x', 2571, True, intermediate_tile='2572,3333,0',
        obj_type='wall', obj_tile={'x': 2570, 'y': 3333}
    )
    util_functions.talk_to_npc('alrena')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(
        1535, 'x', 2574, True, intermediate_tile='2576,3334,0',
        obj_type='wall', obj_tile={'x': 2574, 'y': 3333}
    )
    osrs.move.interact_with_object(598, 'a', 1, True, custom_exit_function=get_picture)
    osrs.move.go_to_loc(2567, 3333)
    util_functions.talk_to_npc('edmond')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2532, 'a', 1, False, obj_type='ground', pre_interact=click_water,
                                   custom_exit_function=use_all_water)
    osrs.move.interact_with_object(2532, 'y', 5500, True, obj_type='ground', pre_interact=click_spade)
    osrs.move.go_to_loc(2514, 9742)
    osrs.move.interact_with_object(11422, 'a', 1, False, obj_type='decorative',
                                   custom_exit_function=util_functions.check_for_dialogue, right_click_option='Open')
    util_functions.dialogue_handler([])
    osrs.move.interact_with_object(
        11422, 'a', 1, False, obj_type='decorative', custom_exit_function=util_functions.check_for_dialogue,
        pre_interact=click_rope)
    util_functions.dialogue_handler([])
    osrs.move.go_to_loc(2516, 9753)
    util_functions.talk_to_npc('edmond')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2542, 'y', 5500, False, pre_interact=click_mask())
    osrs.clock.random_sleep(5, 5.1)
    util_functions.talk_to_npc('jethick')
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2531, 3325)
    osrs.move.interact_with_object(2537, 'a', 1, True, custom_exit_function=util_functions.check_for_dialogue,
                                   obj_type='wall')
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('martha rehnison', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2539, 'z', 1, True, timeout=3, right_click_option='Walk-up')
    util_functions.talk_to_npc('milli rehnison')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2540, 'z', 0, False, timeout=3, right_click_option='Walk-down')
    osrs.move.interact_with_object(2537, 'y', 3328, False, obj_type='wall')
    osrs.move.go_to_loc(2540, 3275)
    osrs.move.interact_with_object(37321, 'y', 3272, False, obj_type='wall',
                                   custom_exit_function=util_functions.check_for_dialogue)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2525, 3309, right_click=True)
    osrs.move.interact_with_object(
        2546, 'y', 3312, True, obj_type='wall', intermediate_tile='2525,3314,0'
    )
    util_functions.talk_to_npc(4255)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2528, 'x', 2530, True, obj_type='wall')
    util_functions.talk_to_npc('bravek')
    util_functions.dialogue_handler(dialogue)
    make_cure()
    util_functions.talk_to_npc('bravek', right_click=True)
    util_functions.dialogue_handler(dialogue, timeout=15)
    osrs.move.interact_with_object(2528, 'x', 2529, False, obj_type='wall')
    osrs.move.interact_with_object(
        2546, 'y', 3311, False, obj_type='wall', intermediate_tile='2525,3310,0'
    )
    osrs.move.go_to_loc(2540, 3275)
    osrs.move.interact_with_object(
        37321, 'y', 3272, False, obj_type='wall',
        timeout=10, custom_exit_function=util_functions.check_for_dialogue, obj_tile={'x': 2540, 'y': 3273}
    )
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2522, 'y', 5500, True, timeout=4, right_click_option='Walk-down')
    osrs.move.interact_with_object(
        2526, 'y', 5500, True, timeout=4,
        custom_exit_function=util_functions.check_for_dialogue, obj_type='wall'
    )
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2523, 'y', 5500, False, timeout=4, right_click_option='Walk-up')
    osrs.move.interact_with_object(2530, 'y', 5500, False, custom_exit_function=get_key)
    osrs.move.interact_with_object(
        2522, 'y', 5500, True, timeout=4, right_click_option='Walk-down'
    )
    osrs.move.interact_with_object(2526, 'x', 2540, True, obj_type='wall')
    util_functions.talk_to_npc('elena')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2526, 'x', 2539, False, obj_type='wall')
    osrs.move.interact_with_object(2523, 'y', 5500, False, timeout=4, right_click_option='Walk-up')
    osrs.move.interact_with_object(37321, 'y', 3273, True, obj_type='wall', obj_tile={'x': 2540, 'y': 3273})
    osrs.move.go_to_loc(2533, 3304)
    osrs.move.interact_with_object(
        2543, 'y', 5500, True, right_click_option='Open', custom_exit_function=open_cover
    )
    osrs.move.interact_with_object(2544, 'y', 5500, True, right_click_option='Climb-down')
    osrs.move.go_to_loc(2516, 9753)
    osrs.move.interact_with_object(2533, 'y', 5500, False)
    util_functions.talk_to_npc('edmond')
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()
    osrs.clock.random_sleep(4, 4.1)
    read_scroll()
