'''# add 70 to y after click to move over ferox enclave
# # [161, 69] to get the equipment tab

q = {
    'widget': '161,69'
}
'''

# need to bank, find bank 26711 tile '3130,3632,0'
# dump air runes
# check if i need a new ring, if so withdraw and equip
# withdraw ess
# click free for all portal, 26645 on '3128,3626,0'
# wait a half second
# click home tele
# wait a sec
# click esc to get back to my inv
# repeat loop

# home tele 8013
import datetime

import keyboard
import pyautogui


import osrs


def click_home_tab():
    inv = osrs.inv.get_inv()
    home_tab = osrs.inv.is_item_in_inventory(inv, 8013)
    osrs.move.move_and_click(home_tab[0], home_tab[1], 4, 6)


def run_to_loc(steps):
    for step in steps:
        while True:
            data = osrs.server.query_game_data({
                'tiles': [step]
            })
            formatted_step = step.replace(',', '')
            if 'tiles' in data and formatted_step in data['tiles'] and data['tiles'][formatted_step]['y'] > 75:
                osrs.move.move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 7, 7)
                break
        osrs.clock.random_sleep(1, 1.1)
    osrs.move.wait_until_stationary()
    osrs.clock.random_sleep(0.5, 0.6)


def click_ruins():
    while True:
        ruins = osrs.server.get_game_object('3313,3255,0', '34817')
        if not ruins:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(ruins['x'], ruins['y'], 7, 7)
            osrs.clock.random_sleep(0.5, 0.6)
            osrs.move.wait_until_stationary()
            break


def click_altar():
    while True:
        altar = osrs.server.get_game_object('2585,4839,0', '34764')
        if not altar:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(altar['x'], altar['y'], 7, 7)
            osrs.clock.random_sleep(0.5, 0.6)
            osrs.move.wait_until_stationary()
            break


def tele_to_altar():
    while True:
        inv = osrs.inv.get_inv()
        ess = osrs.inv.is_item_in_inventory(inv, 7936)
        if ess:
            break
    while True:
        equipment_tab = osrs.server.get_widget('161,69')
        if not equipment_tab:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(equipment_tab['x'], equipment_tab['y'], 7, 7)
            osrs.clock.random_sleep(0.5, 0.6)
            break
    while True:
        ring_slot = osrs.server.get_widget('387,24')
        if not ring_slot:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(ring_slot['x'], ring_slot['y'], 7, 7, 'right')
            osrs.clock.random_sleep(0.5, 0.6)
            current_y_mouse_val = pyautogui.position()[1]
            osrs.move.move_and_click(ring_slot['x'], current_y_mouse_val + 40, 15, 0)
            keyboard.send('esc')
            osrs.clock.random_sleep(2, 2.1)
            break


def tele_to_ferox():
    while True:
        inv = osrs.inv.get_inv()
        ess = osrs.inv.is_item_in_inventory(inv, 7936)
        if not ess:
            break
    while True:
        equipment_tab = osrs.server.get_widget('161,69')
        if not equipment_tab:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(equipment_tab['x'], equipment_tab['y'], 7, 7)
            osrs.clock.random_sleep(0.5, 0.6)
            break
    while True:
        ring_slot = osrs.server.get_widget('387,24')
        if not ring_slot:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(ring_slot['x'], ring_slot['y'], 7, 7, 'right')
            osrs.clock.random_sleep(0.5, 0.6)
            # right click menus always open in the same place relative to where they are opened from,
            # so to access desired entry i just go down from my current y position
            current_y_mouse_val = pyautogui.position()[1]
            osrs.move.move_and_click(ring_slot['x'], current_y_mouse_val + 69, 15, 0)
            keyboard.send('esc')
            osrs.clock.random_sleep(2, 2.1)
            break


def click_bank():
    while True:
        bank = osrs.server.get_game_object('3130,3632,0', '26711')
        if not bank:
            osrs.clock.random_sleep(1, 2)
        else:
            osrs.move.move_and_click(bank['x'], bank['y'], 7, 7)
            osrs.clock.random_sleep(0.5, 0.6)
            osrs.move.wait_until_stationary()
            break


def handle_banking(ring_charges):
    if ring_charges == 0:
        dueling = osrs.bank.find_item_in_bank(2552)
        osrs.move.move_and_click(dueling['x'], dueling['y'], 3, 3, 'right')
        current_y_mouse_val = pyautogui.position()[1]
        osrs.clock.random_sleep(0.3, 0.4)
        osrs.move.move_and_click(dueling['x'], current_y_mouse_val + 45, 7, 3)
        osrs.clock.random_sleep(0.3, 0.4)
        keyboard.send('esc')
        osrs.clock.random_sleep(0.3, 0.4)
        inv = osrs.inv.get_inv()
        dueling = osrs.inv.is_item_in_inventory(inv, 2552)
        osrs.move.move_and_click(dueling[0], dueling[1], 3, 3)
        click_bank()
        osrs.bank.wait_for_bank_interface()
    pure_ess = osrs.bank.find_item_in_bank(7936)
    osrs.move.move_and_click(pure_ess['x'], pure_ess['y'], 3, 3)
    osrs.clock.random_sleep(0.3, 0.4)
    keyboard.send('esc')
    osrs.clock.random_sleep(0.3, 0.4)


def enter_ffa_portal():
    while True:
        portal = osrs.server.get_game_object('3129,3626,0', '26645')
        if portal:
            osrs.move.move_and_click(portal['x'], portal['y'], 3, 3)
            break
    while True:
        player_loc = osrs.server.get_world_location()
        if player_loc and player_loc['y'] > 4000:
            osrs.clock.random_sleep(0.5, 0.6)
            break


def main():
    trips = 0
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 47, 54, 423, 551, 'pass_70', False)
        tele_to_altar()
        osrs.clock.random_sleep(0.5, 0.6)
        click_ruins()
        click_altar()
        tele_to_ferox()
        trips += 1
        click_bank()
        osrs.bank.wait_for_bank_interface()
        handle_banking(trips % 4)
        enter_ffa_portal()


main()
