import matplotlib.pyplot as plt
import os
import pandas as pd
import PySimpleGUI as sg
import tkinter

from constant import ICON, WARBLER
from datatype.canvas import Canvas
from datatype.settings import Settings
from gui import layout, popup
from keybind import register_keybind
from state import State
from validation import (
    HIGH,
    Input,
    LOW,
    to_digit
)


def main():
    if not WARBLER.is_dir():
        raise FileNotFoundError(f"{WARBLER} does not exist")

    window = sg.Window(
        'Animal Vocalization Segmentation',
        layout(),
        icon=ICON,
        size=(1600, 900),
        location=(100, 50),
        element_justification='center',
        keep_on_top=False,
        return_keyboard_events=True,
        finalize=True
    )

    register_keybind(window)

    fig, ax = plt.subplots(
        figsize=(18, 3),
        subplot_kw={'projection': 'spectrogram'}
    )

    fig.set_tight_layout(True)

    tk_canvas = window['canvas'].tk_canvas
    canvas = Canvas(fig, ax, tk_canvas)
    canvas.canvas.pack_forget()

    state = State()
    state.warbler = WARBLER

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

        if event == 'browse':
            prompt = popup('Loading file...')
            window.force_focus()

            item = data['browse']
            state.open(item)

            window['file'].update(
                value=state.current.filename,
                values=state.get_all()
            )

            window.start_thread(
                lambda: state.load(window),
                'loading'
            )

            if prompt:
                prompt.close()

        if event == 'file':
            file = data.get('file')
            state.update(file)

        if state.current is None:
            sg.Popup(
                'Please select a file',
                title='Error',
                icon=ICON,
                button_color='#242424',
                keep_on_top=True
            )

            continue

        if event == 'mode_shortcut':
            mode = window['mode']

            if data['mode'] == 'Exclusion':
                mode.update('Frequency')
            else:
                mode.update('Exclusion')

        if event == 'reset_baseline':
            data['exclude'] = ''

        if event == 'settings' or event == 'settings_shortcut':
            path = WARBLER.joinpath(state.current.segmentation)
            os.startfile(path)

        if event == 'next' or event == 'next_shortcut':
            state.next()
            window['file'].update(set_to_index=state.index)

        if event == 'previous' or event == 'previous_shortcut':
            state.previous()
            window['file'].update(set_to_index=state.index)

        if event in [
            'browse',
            'file',
            'generate',
            'generate_shortcut',
            'mode',
            'next',
            'next_shortcut',
            'previous',
            'previous_shortcut',
            'reset_baseline',
            'reset_custom'
        ]:
            if event == 'generate' or event == 'generate_shortcut':
                state.autogenerate = False
            else:
                state.autogenerate = True

            if event == 'reset_baseline':
                state.baseline = True
            else:
                state.baseline = False

            if event in [
                'file',
                'next',
                'next_shortcut',
                'previous',
                'previous_shortcut',
                'reset_baseline',
                'reset_custom'
            ]:
                state.load(window)

            state.set(data)

            success = canvas.display(window, state)

            if success is False:
                continue

        if event == 'play':
            path = WARBLER.joinpath(state.current.recording)
            os.startfile(path)

        if event == 'copy' or event == 'copy_shortcut':
            df = pd.DataFrame([state.current.filename])
            df.to_clipboard(index=False, header=False)

        if event == 'save' or event == 'save_shortcut':
            state.set(data)
            ui = Input(state.ui)

            if not ui.validate():
                continue

            data = ui.transform()
            data['exclude'] = list(state.exclude)

            path = WARBLER.joinpath(state.current.segmentation)

            settings = Settings.from_file(path)
            settings.update(data)
            settings.save(path)

    window.close()


if __name__ == '__main__':
    main()
