from pynput.keyboard import Controller, Key

keyboard = Controller()


def press_key(key):
    if key == 'esc':
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)