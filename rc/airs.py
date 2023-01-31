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
import keyboard

from osrs_utils import general_utils


def click_home_tab():
    inv = general_utils.get_inv()
    home_tab = general_utils.is_item_in_inventory(inv, 8013)
    general_utils.move_and_click(home_tab[0], home_tab[1], 4, 6)


def run_to_loc(steps):
    for step in steps:
        while True:
            data = general_utils.query_game_data({
                'tiles': [step]
            })
            formatted_step = step.replace(',', '')
            if 'tiles' in data and formatted_step in data['tiles'] and data['tiles'][formatted_step]['y'] > 75:
                general_utils.move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 7, 7)
                break
        general_utils.random_sleep(1, 1.1)
    general_utils.wait_until_stationary()
    general_utils.random_sleep(0.5, 0.6)


def click_ruins():
    while True:
        ruins = general_utils.get_game_object('2985,3292,0', '34813')
        if not ruins:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(ruins['x'], ruins['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break


def click_altar():
    while True:
        altar = general_utils.get_game_object('2844,4834,0', '34760')
        if not altar:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(altar['x'], altar['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break


def tele_to_ferox():
    while True:
        inv = general_utils.get_inv()
        ess = general_utils.is_item_in_inventory(inv, 7936)
        if not ess:
            break
    while True:
        equipment_tab = general_utils.get_widget('161,69')
        if not equipment_tab:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(equipment_tab['x'], equipment_tab['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            break
    while True:
        ring_slot = general_utils.get_widget('387,24')
        if not ring_slot:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(ring_slot['x'], ring_slot['y'], 7, 7, 'right')
            general_utils.random_sleep(0.5, 0.6)
            general_utils.move_and_click(ring_slot['x'], ring_slot['y'] + 69, 15, 2)
            keyboard.send('esc')
            general_utils.random_sleep(2, 2.1)
            break


def click_bank():
    while True:
        bank = general_utils.get_game_object('3130,3632,0', '26711')
        if not bank:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(bank['x'], bank['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break


def handle_banking(ring_charges):
    if ring_charges == 0:
        dueling = general_utils.find_item_in_bank(2552)
        general_utils.move_and_click(dueling['x'], dueling['y'], 3, 3, 'right')
        general_utils.random_sleep(0.3, 0.4)
        general_utils.move_and_click(dueling['x'], dueling['y'] + 45, 7, 0)
        general_utils.random_sleep(0.3, 0.4)
        keyboard.send('esc')
        general_utils.random_sleep(0.3, 0.4)
        inv = general_utils.get_inv()
        dueling = general_utils.is_item_in_inventory(inv, 2552)
        general_utils.move_and_click(dueling[0], dueling[1], 3, 3)
        click_bank()
        general_utils.wait_for_bank_interface()
    pure_ess = general_utils.find_item_in_bank(7936)
    general_utils.move_and_click(pure_ess['x'], pure_ess['y'], 3, 3)
    general_utils.random_sleep(0.3, 0.4)
    keyboard.send('esc')
    general_utils.random_sleep(0.3, 0.4)


def enter_ffa_portal():
    while True:
        portal = general_utils.get_game_object('3129,3626,0', '26645')
        if portal:
            general_utils.move_and_click(portal['x'], portal['y'], 3, 3)
            break
    while True:
        player_loc = general_utils.get_world_location()
        if player_loc and player_loc['y'] > 4000:
            general_utils.random_sleep(0.5, 0.6)
            break

def main():
    ring_charges = 8
    while True:
        click_home_tab()
        run_to_loc([
            '2957,3239,0',
            '2961,3252,0',
            '2971,3263,0',
            '2980,3273,0',
            '2983,3287,0'
        ])
        general_utils.random_sleep(0.5, 0.6)
        click_ruins()
        click_altar()
        tele_to_ferox()
        ring_charges -= 1
        run_to_loc(['3134,3628,0'])
        click_bank()
        general_utils.wait_for_bank_interface()
        handle_banking(ring_charges)
        enter_ffa_portal()

main()