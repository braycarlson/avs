class Keyboard:
    def __init__(self, key):
        self.key = key
        self.modifier = None


class MicrosoftKeyboard(Keyboard):
    def __init__(self, key):
        self.key = key
        self.modifier = 'Control'

    def __str__(self):
        return f"<{self.modifier}-{self.key}>"


class AppleKeyboard(Keyboard):
    def __init__(self, key):
        self.key = key
        self.modifier = 'Command'

    def __str__(self):
        return f"<{self.modifier}-{self.key}>"


class Keybind:
    def __init__(self, window):
        self.window = window

    def register(self, key, event):
        microsoft = MicrosoftKeyboard(key)
        apple = AppleKeyboard(key)

        self.window.bind(microsoft, event)
        self.window.bind(apple, event)


def register_keybind(window):
    keybind = Keybind(window)

    # Generate spectrogram
    keybind.register('g', 'generate_shortcut')

    # # Previous recording
    # keybind.register('Left', 'previous_shortcut')

    # # Next recording
    # keybind.register('Right', 'next_shortcut')

    # Switch mode
    keybind.register('m', 'mode_shortcut')

    # Copy filename
    keybind.register('f', 'copy_shortcut')

    # Open the settings file
    keybind.register('p', 'settings_shortcut')

    # Save settings
    keybind.register('s', 'save_shortcut')

    # Detect keypress
    window.bind('<Key>', 'keypress')

    # Up arrow
    window.bind('<Up>', 'up')

    # Left arrow
    window.bind('<Left>', 'left')

    # Down arrow
    window.bind('<Down>', 'down')

    # Right arrow
    window.bind('<Right>', 'right')
