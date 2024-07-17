import time

from flask import Flask, request
import pyautogui
import pywinctl as pwc
import osrs

app = Flask(__name__)
logger = osrs.dev.instantiate_logger()


@app.route('/click', methods=['POST', 'GET'])
def handle_click():
    click_request = request.get_json()
    if 'name' not in click_request:
        logger.warning('Request submitted with no player name.: %s', click_request)
        return ''
    elif 'x' not in click_request:
        logger.warning('Request submitted with no x coordinate: %s', click_request)
        return ''
    elif 'y' not in click_request:
        logger.warning('Request submitted with no y coordinate: %s', click_request)
        return ''

    windows = pwc.getWindowsWithTitle(click_request['name'], condition=pwc.Re.CONTAINS)
    if not windows:
        logger.warning('No RuneLite window found for: %s', click_request['name'])
    window = windows[0]
    window.activate()
    pyautogui.click(click_request['x'], click_request['y'])
    logger.info('Clicked (%s, %s) for player: %s', click_request['x'], click_request['y'], click_request['name'])
    return 'success'


@app.route('/type', methods=['POST', 'GET'])
def handle_typing():
    click_request = request.get_json()
    if 'name' not in click_request:
        logger.warning('Typing request submitted with no player name.: %s', click_request)
        return ''
    elif 'input' not in click_request and 'key_press' not in click_request:
        logger.warning('Typing request submitted with no input or key press: %s', click_request)
        return ''

    windows = pwc.getWindowsWithTitle(click_request['name'], condition=pwc.Re.CONTAINS)
    if not windows:
        logger.warning('No RuneLite window found for: %s', click_request['name'])
    window = windows[0]
    window.activate()
    time.sleep(0.1)
    if 'input' in click_request:
        osrs.keeb.write(str(click_request['input']))
        osrs.keeb.press_key('enter')
        logger.info('Wrote "%s" for player: %s', click_request['input'], click_request['name'])
    elif 'key_press' in click_request:
        osrs.keeb.press_key(click_request['key_press'])
        logger.info('Press key "%s" for player: %s', click_request['key_press'], click_request['name'])
    return 'success'


if __name__ == '__main__':
   app.run(port=1848)