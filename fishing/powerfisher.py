# find a fishing spot
# start fishing
# fish until bag is full
# drop everything
# repeat
import datetime
import time
import random

from osrs_utils import general_utils
import math


def find_spot():
    data = general_utils.get_player_info()
    if not data or len(data["fishingSpotData"]) == 0:
        return 'server error'
    closest_spot = [0, 0]
    dist = 999
    for spot in data["fishingSpotData"]:
        if spot["dist"] < dist:
            closest_spot = [math.floor(spot["x"]), math.floor(spot["y"])]
            dist = spot["dist"]
    print(closest_spot)
    general_utils.move_and_click(closest_spot[0], closest_spot[1], 8, 8)
    general_utils.click_off_screen()
    cycles_waiting_for_spot = 0
    while True:
        data = general_utils.get_player_info()
        if cycles_waiting_for_spot > 50:
            return 'never started fishing'
        elif data["amFishing"]:
            break
        else:
            cycles_waiting_for_spot += 1
        time.sleep(1)
    return 'success'


def main():
    start = datetime.datetime.now()
    max_run = random.randint(3422, 4329)
    desired_rest = random.randint(543, 847)
    while True:
        long_break = general_utils.long_break_manager((datetime.datetime.now() - start).seconds, max_run, desired_rest)
        if long_break != 'no break':
            start = long_break[0]
            max_run = long_break[1]
            desired_rest = long_break[2]
        general_utils.antiban_rest()
        data = general_utils.get_player_info()
        random_event = general_utils.check_and_dismiss_random(data["randomEvent"])
        if random_event == 'didnt find the dismiss option':
            print('failed to handle random: ', random)
            break
        start_fishing = find_spot()
        if start_fishing != 'success':
            return start_fishing
        while True:
            data = general_utils.get_player_info()
            random_event = general_utils.check_and_dismiss_random(data["randomEvent"])
            if random_event == 'didnt find the dismiss option':
                print('failed to handle random: ', random)
                break
            general_utils.antiban_rest()
            if data["amFishing"]:
                print('still fishing')
                time.sleep(3)
                continue
            elif len(data["inv"]) == 28:
                print('full bag')
                break
            elif not data["amFishing"]:
                print('not fishing')
                # wait a second or two so that I dont click the spot right before it disappears
                general_utils.random_sleep(1.2, 1.5)
                start_fishing = find_spot()
                if start_fishing != 'success':
                    return start_fishing
                time.sleep(3)
                continue
        general_utils.random_sleep(2, 5)
        data = general_utils.get_player_info()
        #salmon + trout = 335, 331
        general_utils.power_drop(data["inv"], [0, 1], [11328])


print(main())