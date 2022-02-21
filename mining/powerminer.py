from osrs_utils import general_utils

def main():
    curr_rock = 0
    while True:
        while True:
            clicked = False
            data = general_utils.get_player_info(7776)
            general_utils.check_and_dismiss_random(data["randomEvent"])
            if data["rockData"]:
                for rock in data["rockData"]:
                    print(rock)
                    if rock["num"] == (curr_rock % 3):
                        general_utils.move_and_click(rock["x"], rock["y"], 7, 7)
                        clicked = True
                        curr_rock += 1
                        break
                if clicked:
                    break
                general_utils.random_sleep(1, 2)
        general_utils.bezier_movement(1721,  753, 1874, 802)
        # wait for the rock to be mined
        found_ore = False
        general_utils.antiban_rest(50, 150, 250)
        while True:
            data = general_utils.get_player_info(7776)
            general_utils.check_and_dismiss_random(data["randomEvent"])
            if data["inv"]:
                for item in data["inv"]:
                    if item["id"] == 440:
                        general_utils.move_and_click(item["x"], item["y"], 5, 5)
                        found_ore = True
                if found_ore:
                    break
        general_utils.antiban_rest(50, 150, 250)
main()