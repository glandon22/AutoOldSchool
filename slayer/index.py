import osrs
import slayer

'''
begin loop
check for slayer task
if not task, go to nieve/steve to get a task, then tele to bank

if task, invoke the script that handles that task
that script will look like:
gear up
travel to the location of the monster
once there, invoke my kill and loot with proper vars and loop until task is over

if i run out of supps that script will exit back to my task script handler
which will check whether task is done, if task is done it exits
otherwise it teles home and regears then calls kill script again

i repeat that process until task is successfully completed. then the task script handler will exit with success
back to my main index handler. it will then notice i have no task, and repeat from beginning
'''


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_slayer()
    while True:
        qh.query_backend()
        slayer_task = 'monster' in qh.get_slayer() and qh.get_slayer()['monster']
        if slayer_task:
            if slayer_task == 'Iron Dragons':
                slayer.iron_dragons.main()
            elif slayer_task == 'Kalphite':
                slayer.kalphite.main()
            elif slayer_task == 'Trolls':
                slayer.trolls.main()
                return
            else:
                return print(f'Can not parse {slayer_task}')
        else:
            return print('logic not implemented to get a new task yet')

main()