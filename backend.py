from flask import Flask, request
import pyautogui
import pywinctl as pwc
import osrs

app = Flask(__name__)
logger = osrs.dev.instantiate_logger()


@app.route('/', methods=['POST', 'GET'])
def handle_input():
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


if __name__ == '__main__':
   app.run(port=1848)