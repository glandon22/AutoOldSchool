from pynput.keyboard import Controller, Key

keyboard = Controller()
key = Key


def press_key(key):
    """

    :param key: 'esc' | 'enter' | 'f5 | 'f6'
    """
    if key == 'esc':
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
    elif key == 'enter':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif key == 'f1':
        keyboard.press(Key.f1)
        keyboard.release(Key.f1)
    elif key == 'f4':
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
    elif key == 'f5':
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    elif key == 'f6':
        keyboard.press(Key.f6)
        keyboard.release(Key.f6)
    elif key == 'space':
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif key == 'shift':
        keyboard.press(Key.shift)
        keyboard.release(Key.space)


def write(phrase):
    keyboard.type(phrase)
