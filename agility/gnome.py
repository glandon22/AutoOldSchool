from osrs_utils import general_utils


def step1():
    while True:
        q = {
            'groundObjects': [
                {
                    'tile': '2474,3435,0',
                    'object': '23145'
                }
            ]
        }
        data = general_utils.query_game_data(q)
        if '23145' in data['groundObjects']:
            general_utils.move_and_click(data['groundObjects']['23145']['x'], data['groundObjects']['23145']['y'], 2, 3)
            general_utils.random_sleep(1, 1.1)
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 2474 and data['playerWorldPoint']['y'] == 3429:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break


def step2():
    while True:
        q = {
                'gameObjects': [
                    {
                        'tile': '2474,3425,0',
                        'object': '23134'
                    }
                ]
            }
        data = general_utils.query_game_data(q)
        if '23134' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['23134']['x'], data['gameObjects']['23134']['y'], 2, 3)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 2473 and data['playerWorldPoint']['y'] == 3423:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break
    general_utils.random_sleep(1, 1.1)

def step3():
    while True:
        q = {
                'gameObjects': [
                    {
                        'tile': '2473,3422,1',
                        'object': '23559'
                    }
                ]
            }
        data = general_utils.query_game_data(q)
        if '23559' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['23559']['x'], data['gameObjects']['23559']['y'], 2, 3)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 2473 and data['playerWorldPoint']['y'] == 3420:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break

def step4():
    while True:
        q = {
            'groundObjects': [
                {
                    'tile': '2478,3420,2',
                    'object': '23557'
                }
            ]
        }
        data = general_utils.query_game_data(q)
        if '23557' in data['groundObjects']:
            general_utils.move_and_click(data['groundObjects']['23557']['x'], data['groundObjects']['23557']['y'], 2, 3)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 2483 and data['playerWorldPoint']['y'] == 3420:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break


def step5():
    while True:
        q = {
                'playerWorldPoint': True,
                'gameObjects': [
                    {
                        'tile': '2486,3419,2',
                        'object': '23560'
                    }
                ]
            }
        data = general_utils.query_game_data(q)
        if '23560' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['23560']['x'], data['gameObjects']['23560']['y'], 2, 3)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 2487 and data['playerWorldPoint']['y'] == 3420:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break

def step6():
    while True:
        q = {
                'playerWorldPoint': True,
                'gameObjects': [
                    {
                        'tile': '2486,3426,0',
                        'object': '23135'
                    }
                ]
            }
        data = general_utils.query_game_data(q)
        if '23135' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['23135']['x'], data['gameObjects']['23135']['y'], 2, 3)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['y'] > 3425:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break

def step7():
    while True:
        q = {
                'playerWorldPoint': True,
                'gameObjects': [
                    {
                        'tile': '2487,3431,0',
                        'object': '23139'
                    }
                ]
            }
        data = general_utils.query_game_data(q)
        if '23139' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['23139']['x'], data['gameObjects']['23139']['y'], 2, 3)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['y'] > 3436:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break



def main():
    while True:
        print('Step 1')
        step1()
        print('Step 2')
        step2()
        print('Step 3')
        step3()
        print('Step 4')
        step4()
        print('Step 5')
        step5()
        print('Step 6')
        step6()
        general_utils.random_sleep(2, 2.2)
        print('Step 7')
        step7()


main()