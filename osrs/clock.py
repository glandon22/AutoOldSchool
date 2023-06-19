import datetime
import random
import time


def random_sleep(min_time, max_time):
    duration = round(random.uniform(min_time, max_time), 6)
    #print('Sleeping for ', duration)
    time.sleep(duration)


def antiban_rest(short=10, med=25, long=75):
    if random.randint(0, short) == 1:
        print('Taking a short break.')
        random_sleep(5.1, 6.8)
    elif random.randint(0, med) == 1:
        print('Taking a medium break.')
        random_sleep(27.2, 39.9)
    elif random.randint(0, long) == 1:
        print('Taking a long break.')
        random_sleep(64.5, 83.9)


def sleep_one_tick():
    random_sleep(0.6, 0.7)


def break_every_hour(max_run, start_time=-1):
    if start_time == -1:
        start_time = datetime.datetime.now()
    random_sleep(0.5, 0.9)
    run_time = (datetime.datetime.now() - start_time).total_seconds()
    print('Current Script Runtime: ', run_time, '. Maximum Script Runtime: ', max_run * 60)
    if run_time > max_run * 60:
        return True
    else:
        return False

