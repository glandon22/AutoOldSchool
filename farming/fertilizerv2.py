
import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
def main():
    while True:
        banker = osrs.server.get_npc_by_id('6940', port)
        if banker:
            osrs.move.move_and_click(banker['x'], banker['y'], 4, 4)
            osrs.move.move_and_click(banker['x'], banker['y'], 4, 4)
            print('clicking')
            osrs.bank.wait_for_bank_interface(port)
            osrs.bank.bank_dump_inv(port)
            bank = osrs.bank.get_bank_data(port)
            if bank:
                first = osrs.inv.is_item_in_inventory_v2(bank, '13421')
                if not first:
                    exit('out of items')
                osrs.move.move_and_click(first['x'], first['y'], 3, 3)
                second = osrs.inv.is_item_in_inventory_v2(bank, '6032')
                if not second:
                    exit('out of items')
                osrs.move.move_and_click(second['x'], second['y'], 3, 3)
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                osrs.clock.random_sleep(1.2, 1.3)
                while True:
                    inv = osrs.inv.get_inv(port, True)
                    first = osrs.inv.is_item_in_inventory_v2(inv, '13421')
                    if not first:
                        break
                    osrs.move.move_and_click(first['x'], first['y'], 3, 3)
                    second = osrs.inv.is_item_in_inventory_v2(inv, '6032')
                    if not second:
                        break
                    osrs.move.move_and_click(second['x'], second['y'], 3, 3)
                    osrs.clock.random_sleep(0.6, 0.7)



osrs.clock.random_sleep(1 ,1.1)
main()