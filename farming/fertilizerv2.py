from autoscape import general_utils
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
def main():
    while True:
        banker = general_utils.get_npc_by_id('6940', port)
        if banker:
            general_utils.move_and_click(banker['x'], banker['y'], 4, 4)
            general_utils.move_and_click(banker['x'], banker['y'], 4, 4)
            print('clicking')
            general_utils.wait_for_bank_interface(port)
            general_utils.bank_dump_inv(port)
            bank = general_utils.get_bank_data(port)
            if bank:
                first = general_utils.is_item_in_inventory_v2(bank, '13421')
                if not first:
                    exit('out of items')
                general_utils.move_and_click(first['x'], first['y'], 3, 3)
                second = general_utils.is_item_in_inventory_v2(bank, '6032')
                if not second:
                    exit('out of items')
                general_utils.move_and_click(second['x'], second['y'], 3, 3)
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                general_utils.random_sleep(1.2, 1.3)
                while True:
                    inv = general_utils.get_inv(port, True)
                    first = general_utils.is_item_in_inventory_v2(inv, '13421')
                    if not first:
                        break
                    general_utils.move_and_click(first['x'], first['y'], 3, 3)
                    second = general_utils.is_item_in_inventory_v2(inv, '6032')
                    if not second:
                        break
                    general_utils.move_and_click(second['x'], second['y'], 3, 3)
                    general_utils.random_sleep(0.6, 0.7)



general_utils.random_sleep(1 ,1.1)
main()