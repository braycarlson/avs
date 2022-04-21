import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import PySimpleGUI as sg
import tkinter

from action import (
    backward,
    forward,
    get_metadata,
    load_input,
    load_pickle
)
from constant import (
    BASELINE,
    FILE,
    FILENAME,
    ICON
)
from dataclass.canvas import Canvas
from gui import layout
from plot import plot_bandwidth, plot_exclusion
from validation import (
    HIGH,
    LOW,
    REMOVE,
    to_digit,
    to_exclusion,
    validate
)


def main():
    window = sg.Window(
        '',
        layout(),
        icon=ICON,
        size=(1600, 850),
        location=(100, 75),
        element_justification='center',
        keep_on_top=False,
        return_keyboard_events=True,
        finalize=True
    )

    # Generate spectrogram
    if os.name == 'nt':
        window.bind('<Control-g>', 'generate_shortcut')
    else:
        window.bind('<Command-g>', 'generate_shortcut')

    # Previous recording
    if os.name == 'nt':
        window.bind('<Control-Left>', 'previous_shortcut')
    else:
        window.bind('<Command-Left>', 'previous_shortcut')

    # Next recording
    if os.name == 'nt':
        window.bind('<Control-Right>', 'next_shortcut')
    else:
        window.bind('<Command-Right>', 'next_shortcut')

    # Switch mode
    if os.name == 'nt':
        window.bind('<Control-m>', 'mode_shortcut')
    else:
        window.bind('<Command-m>', 'mode_shortcut')

    # Copy filename
    if os.name == 'nt':
        window.bind('<Control-f>', 'copy_shortcut')
    else:
        window.bind('<Command-f>', 'copy_shortcut')

    # Open the parameters file
    if os.name == 'nt':
        window.bind('<Control-p>', 'parameters_shortcut')
    else:
        window.bind('<Command-p>', 'parameters_shortcut')

    # Save parameters
    if os.name == 'nt':
        window.bind('<Control-s>', 'save_shortcut')
    else:
        window.bind('<Command-s>', 'save_shortcut')

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

    # The canvas for a spectrogram
    figsize = (16, 3)
    fig = plt.figure(figsize=figsize)
    tk_canvas = window['canvas'].tk_canvas
    canvas = Canvas(fig, tk_canvas)

    while True:
        event, data = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'keypress':
            element = window.find_element_with_focus()

            if isinstance(element, sg.PySimpleGUI.Input):
                ui = to_digit(data[element.key])
                cursor = element.widget.index(tkinter.INSERT)

                if element.key in LOW:
                    window['spectral_range_low'].update(ui)
                    window['mel_lower_edge_hertz'].update(ui)
                    window['butter_lowcut'].update(ui)
                elif element.key in HIGH:
                    window['spectral_range_high'].update(ui)
                    window['mel_upper_edge_hertz'].update(ui)
                    window['butter_highcut'].update(ui)
                else:
                    window[element.key].update(ui)

                element.widget.icursor(cursor)

        if event == 'up':
            element = window.find_element_with_focus()

            if isinstance(element, sg.PySimpleGUI.Input):
                element.widget.icursor(0)

        if event == 'down':
            element = window.find_element_with_focus()

            if isinstance(element, sg.PySimpleGUI.Input):
                ui = data[element.key]
                length = len(ui)
                element.widget.icursor(length)

        if event == 'file':
            data['exclude'] = ''

            item = data['file']
            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            with open(parameter, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

        if event == 'browse':
            item = data['browse']
            load_pickle(item)

            values = [item.get('filename') for item in FILE]

            window['file'].update(
                value='',
                values=values
            )

        if event == 'mode_shortcut':
            mode = window['mode']

            if data['mode'] == 'Exclusion':
                mode.update('Frequency')
            else:
                mode.update('Exclusion')

        if event == 'generate' or event == 'generate_shortcut':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            figure = plt.gcf()

            if figure is not None:
                plt.cla()
                plt.clf()
                plt.close('all')

            data = validate(data)

            if data is None:
                continue

            mode = data['mode']

            if mode == 'Exclusion':
                figure = plot_exclusion(window, data)
            else:
                figure = plot_bandwidth(window, data)

            if figure is None:
                continue

            canvas.set_figure(figure)
            canvas.draw()

        if event == 'reset_custom':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            data['exclude'] = ''
            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            with open(parameter, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

        if event == 'reset_baseline':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            data['exclude'] = ''

            with open(BASELINE, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

        if event == 'parameters' or event == 'parameters_shortcut':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            os.startfile(parameter)

        if event == 'next' or event == 'next_shortcut':
            if len(FILENAME) == 0:
                sg.Popup(
                    'Please open a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            item = data['file']

            if item == '':
                index = 0
            else:
                index = forward(item)

            window['file'].update(
                set_to_index=index,
            )

            item = FILENAME[index]
            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            with open(parameter, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

        if event == 'previous' or event == 'previous_shortcut':
            if len(FILENAME) == 0:
                sg.Popup(
                    'Please open a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            item = data['file']

            if item == '':
                index = len(FILENAME) - 1
            else:
                index = backward(item)

            window['file'].update(
                set_to_index=index,
            )

            item = FILENAME[index]
            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            with open(parameter, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

        if event == 'play':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            metadata = get_metadata(item)
            song = metadata.get('song')

            os.startfile(song)

        if event == 'copy' or event == 'copy_shortcut':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            df = pd.DataFrame([item])
            df.to_clipboard(index=False, header=False)

        if event == 'save' or event == 'save_shortcut':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            low = data.get('spectral_range_low')
            high = data.pop('spectral_range_high')
            spectral_range = [int(low), int(high)]

            data = {
                'spectral_range'
                if key == 'spectral_range_low' else key: value
                for key, value in data.items()
            }

            data['spectral_range'] = spectral_range

            exclude = to_exclusion(data['exclude'])

            data = validate(data)

            if data is None:
                continue

            data.update({
                'exclude': exclude,
                'power': 1.5,
                'griffin_lim_iters': 50,
                'noise_reduce_kwargs': {},
                'mask_spec_kwargs': {
                    'spec_thresh': 0.9,
                    'offset': 1e-10
                }
            })

            for key in REMOVE:
                data.pop(key)

            with open(parameter, 'w+') as handle:
                text = json.dumps(data, indent=4)
                handle.write(text)

    window.close()


if __name__ == '__main__':
    main()
