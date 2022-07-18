import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import PySimpleGUI as sg
import tkinter

from constant import ICON, SETTINGS
from datatype.canvas import Canvas
from datatype.parameters import Parameters
from gui import layout
from keybind import register_keybind
from state import load_input, State
from validation import (
    HIGH,
    Input,
    LOW,
    to_digit
)


def main():
    window = sg.Window(
        'Animal Vocalization Segmentation',
        layout(),
        icon=ICON,
        size=(1600, 850),
        location=(100, 75),
        element_justification='center',
        keep_on_top=False,
        return_keyboard_events=True,
        finalize=True
    )

    register_keybind(window)

    figsize = (16, 3)
    fig = plt.figure(figsize=figsize)
    tk_canvas = window['canvas'].tk_canvas
    canvas = Canvas(fig, tk_canvas)

    state = State()

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

            file = data.get('file')
            state.update(file)

            path = state.current.parameters

            with open(path, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

            state.set(data)
            state.autogenerate = True
            spectrogram = canvas.prepare(window, state)

            if spectrogram is None:
                continue

            canvas.set(spectrogram)
            canvas.draw()

        if event == 'browse':
            item = data['browse']
            state.load(item)

            window['file'].update(
                value=state.current.filename,
                values=state.get_all()
            )

            path = state.current.parameters

            with open(path, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

            state.set(data)
            state.autogenerate = True
            spectrogram = canvas.prepare(window, state)

            if spectrogram is None:
                continue

            canvas.set(spectrogram)
            canvas.draw()

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

            state.set(data)
            state.autogenerate = False
            spectrogram = canvas.prepare(window, state)

            if spectrogram is None:
                continue

            canvas.set(spectrogram)
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
            path = state.current.parameters

            with open(path, 'r') as handle:
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

            path = SETTINGS.joinpath('parameters.json')

            with open(path, 'r') as handle:
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

            path = state.current.parameters
            os.startfile(path)

        if event == 'next' or event == 'next_shortcut':
            item = data['file']

            if item == '' or state.empty:
                sg.Popup(
                    'Please open a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            state.next()

            window['file'].update(
                set_to_index=state.index,
            )

            path = state.current.parameters

            with open(path, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

            canvas.close()

            state.set(data)
            spectrogram = canvas.prepare(window, state)

            if spectrogram is None:
                continue

            canvas.set(spectrogram)
            canvas.draw()

        if event == 'previous' or event == 'previous_shortcut':
            item = data['file']

            if item == '' or state.empty:
                sg.Popup(
                    'Please open a file',
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                continue

            state.previous()

            window['file'].update(
                set_to_index=state.index,
            )

            path = state.current.parameters

            with open(path, 'r') as handle:
                file = json.load(handle)
                load_input(window, file)

            state.set(data)
            spectrogram = canvas.prepare(window, state)

            if spectrogram is None:
                continue

            canvas.set(spectrogram)
            canvas.draw()

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

            path = state.current.signal
            os.startfile(path)

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

            state.set(data)
            ui = Input(state.input)

            if not ui.validate():
                continue

            data = ui.transform()

            path = state.current.parameters
            parameters = Parameters.from_file(path)
            parameters.update(data)
            parameters.save(path)

    window.close()


if __name__ == '__main__':
    main()
