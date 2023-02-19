import datetime

from osrs_utils import general_utils
fruits = [
    1955,
    1963,
    5504,
    247,
    2102,
    1951,
    2114,
    2120,
    464,
    19653,
    5972
]
def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 58, 423, 551, 'pass_71', False)
        q = {
            'isFishing': True,
            'inv': True,
            'poseAnimation': True
        }
        data = general_utils.query_game_data(q)
        if len(data["inv"]) == 28:
            # salmon + trout = 335, 331
            # shrimp anchovie 317, 321
            # leaping trout 11328
            general_utils.power_drop(data["inv"], [], fruits)
        stall = general_utils.get_game_object('1801,3608,0', '28823', '56799')
        if stall:
            general_utils.move_and_click(stall['x'], stall['y'], 9, 9)
            general_utils.random_sleep(0.4, 0.5)

main()