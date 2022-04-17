import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import PySimpleGUI as sg

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
    FILENAME
)
from gui import layout
from plot import draw, plot_bandwidth, plot_exclusion
from validation import REMOVE, to_digit, validate


def main():
    window = sg.Window(
        'avs',
        layout(),
        size=(1600, 850),
        location=(100, 75),
        element_justification='center',
        keep_on_top=False,
        finalize=True
    )

    widget = None

    while True:
        event, data = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'file':
            data['exclude'] = ''

            if widget is not None:
                widget.get_tk_widget().forget()
                plt.close('all')

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

        if event == 'generate':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    keep_on_top=True
                )

                continue

            data = validate(data)

            if data is None:
                continue

            mode = data['mode']

            if mode == 'Exclusion':
                fig = plot_exclusion(window, data)
            else:
                fig = plot_bandwidth(window, data)

            if fig is None:
                continue

            if widget is not None:
                widget.get_tk_widget().forget()
                plt.close('all')

            widget = draw(window['canvas'].TKCanvas, fig)

        if event == 'reset_custom':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
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
                    keep_on_top=True
                )

                continue

            data['exclude'] = ''

            with open(BASELINE, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

        if event == 'parameters':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    keep_on_top=True
                )

                continue

            metadata = get_metadata(item)
            parameter = metadata.get('parameter')

            os.startfile(parameter)

        if event == 'next':
            if len(FILENAME) == 0:
                sg.Popup(
                    'Please open a file',
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

        if event == 'previous':
            if len(FILENAME) == 0:
                sg.Popup(
                    'Please open a file',
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
                    keep_on_top=True
                )

                continue

            metadata = get_metadata(item)
            song = metadata.get('song')

            os.startfile(song)

        if event == 'copy':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
                    keep_on_top=True
                )

                continue

            df = pd.DataFrame([item])
            df.to_clipboard(index=False, header=False)

        if event == 'save':
            item = data['file']

            if item == '':
                sg.Popup(
                    'Please select a file',
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

            exclude = to_digit(data['exclude'])

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
