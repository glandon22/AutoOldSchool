from pynput.keyboard import Controller, Key

keyboard = Controller()
key = Key


def press_key(key):
    """

    :param key: 'esc' | 'enter' | 'f6'
    """
    if key == 'esc':
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
    elif key == 'enter':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif key == 'f6':
        keyboard.press(Key.f6)
        keyboard.release(Key.f6)


def write(phrase):
    keyboard.type(phrase)
