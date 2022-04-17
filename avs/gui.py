import PySimpleGUI as sg

from constant import PACKAGE


sg.theme('LightGrey1')


def filelist():
    return [
        sg.T(
            'File',
            size=(0, 0),
            font='Arial 10 bold'
        ),

        sg.Combo(
            [],
            size=(60, 1),
            key='file',
            pad=(10, 0),
            background_color='white',
            text_color='black',
            button_arrow_color='black',
            button_background_color='white',
            enable_events=True,
            readonly=True,
        ),

        sg.Combo(
            [],
            size=(0, 0),
            key='browse',
            pad=(0, 0),
            enable_events=True,
            readonly=True,
            visible=False
        ),

        sg.FileBrowse(
            size=(10, 0),
            button_color='#242424',
            key='explorer',
            target='browse',
            initial_folder=PACKAGE,
            enable_events=True,
            change_submits=False
        ),
    ]


def mode():
    return [
        sg.T(
            'Mode',
            size=(0, 0),
            font='Arial 10 bold'
        ),

        sg.Combo(
            ['Exclusion', 'Frequency'],
            size=(15, 1),
            key='mode',
            pad=((4, 0), 0),
            background_color='white',
            text_color='black',
            button_arrow_color='black',
            button_background_color='white',
            enable_events=True,
            readonly=True,
            default_value='Exclusion'
        )
    ]


def parameter(name, **kwargs):
    multi = kwargs.get('multi')

    if multi:
        return [
            sg.T(
                name,
                size=(20, 0),
                font='Arial 10 bold'
            ),

            sg.I(
                '',
                key=name + '_' + 'low',
                size=(22, 1)
            ),

            sg.I(
                '',
                key=name + '_' + 'high',
                size=(22, 1)
            )
        ]
    else:
        return [
            sg.T(
                name,
                size=(20, 0),
                font='Arial 10 bold'
            ),

            sg.I(
                '',
                key=name,
                size=(46, 1),
                **kwargs
            )
        ]


def button(name, **kwargs):
    font = 'Arial 10'
    size = (18, 1)

    return [
        sg.B(
            name,
            size=size,
            font=font,
            **kwargs
        )
    ]


def layout():
    left = [
        parameter('n_fft'),
        parameter('hop_length_ms'),
        parameter('win_length_ms'),
        parameter('ref_level_db'),
        parameter('preemphasis'),
        parameter('min_level_db'),
        parameter('min_level_db_floor'),
        parameter('db_delta'),
        parameter('silence_threshold'),
        parameter('min_silence_for_spec'),
        parameter('max_vocal_for_spec'),
    ]

    right = [
        parameter('min_syllable_length_s'),
        parameter('spectral_range', multi=True),
        parameter('num_mel_bins'),
        parameter('mel_lower_edge_hertz'),
        parameter('mel_upper_edge_hertz'),
        parameter('butter_lowcut'),
        parameter('butter_highcut'),
        parameter('bandpass_filter'),
        parameter('reduce_noise'),
        parameter('mask_spec'),
        parameter('exclude')
    ]

    return [
        [
            sg.Column(
                [filelist()],
                justification='center',
                element_justification='center',
                vertical_alignment='center',
                pad=(20, 5)
            ),
            sg.Column(
                [mode()],
                justification='center',
                element_justification='center',
                vertical_alignment='center',
                pad=(20, 5)
            )
        ],
        [
            sg.Canvas(
                key='canvas',
                size=(1600, 300),
                pad=(0, (10, 15))
            )
        ],
        [
            sg.Column(
                left,
                justification='center',
                element_justification='center',
                vertical_alignment='center',
                pad=(20, (0, 20))
            ),
            sg.Column(
                right,
                justification='center',
                element_justification='center',
                vertical_alignment='center',
                pad=(20, (0, 20))
            )
        ],
        [sg.Frame('', border_width=0, pad=(None, (20, 0)), layout=[
            button('Previous', key='previous', button_color='#242424') +
            button('Generate', key='generate', button_color='#d22245') +
            button('Next', key='next', button_color='#242424')
        ])],
        [sg.Frame('', border_width=0, pad=(None, (20, 0)), layout=[
            button('Parameters', key='parameters', button_color='#242424') +
            button('Reset to Custom', key='reset_custom', button_color='#242424') +
            button('Reset to Baseline', key='reset_baseline', button_color='#242424')
        ])],
        [sg.Frame('', border_width=0, pad=(None, (20, 0)), layout=[
            button('Play', key='play', button_color='#242424') +
            button('Copy', key='copy', button_color='#242424') +
            button('Save', key='save', button_color='#242424')
        ])]
    ]
