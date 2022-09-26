import PySimpleGUI as sg

from constant import WARBLER
from theme import (
    BUTTON_BACKGROUND,
    BUTTON_FONT,
    COMBOBOX_BACKGROUND,
    CTA_BACKGROUND,
    FONT,
    INPUT_BACKGROUND,
    TEXT_COLOR
)


sg.theme('LightGrey1')
sg.PySimpleGUI.TOOLTIP_BACKGROUND_COLOR = INPUT_BACKGROUND


def filelist():
    initial_folder = WARBLER.joinpath('output/pickle')

    return [
        sg.T(
            'File',
            size=(0, 0),
            font=FONT
        ),

        sg.Combo(
            [],
            size=(60, 1),
            key='file',
            pad=(10, 0),
            background_color=COMBOBOX_BACKGROUND,
            text_color=TEXT_COLOR,
            button_arrow_color=TEXT_COLOR,
            button_background_color=COMBOBOX_BACKGROUND,
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
            button_color=BUTTON_BACKGROUND,
            key='explorer',
            target='browse',
            file_types=(
                ('lzma', '*.xz'),
            ),
            initial_folder=initial_folder,
            enable_events=True,
            change_submits=False
        ),
    ]


def mode():
    return [
        sg.T(
            'Mode',
            size=(0, 0),
            font=FONT
        ),

        sg.Combo(
            ['Exclusion', 'Frequency'],
            size=(15, 1),
            key='mode',
            pad=((4, 0), 0),
            background_color=COMBOBOX_BACKGROUND,
            text_color=TEXT_COLOR,
            button_arrow_color=TEXT_COLOR,
            button_background_color=COMBOBOX_BACKGROUND,
            enable_events=True,
            readonly=True,
            default_value='Exclusion'
        )
    ]


def parameter(name, **kwargs):
    multi = False

    if kwargs.get('multi'):
        multi = kwargs.pop('multi')

    if multi:
        return [
            sg.T(
                name,
                size=(20, 0),
                font=FONT,
                text_color=TEXT_COLOR
            ),

            sg.I(
                '',
                key=name + '_' + 'low',
                size=(22, 1),
                text_color=TEXT_COLOR,
                background_color=INPUT_BACKGROUND,
                **kwargs
            ),

            sg.I(
                '',
                key=name + '_' + 'high',
                size=(22, 1),
                text_color=TEXT_COLOR,
                background_color=INPUT_BACKGROUND,
                **kwargs
            )
        ]
    else:
        return [
            sg.T(
                name,
                size=(20, 0),
                font=FONT,
                text_color=TEXT_COLOR
            ),

            sg.I(
                '',
                key=name,
                size=(46, 1),
                text_color=TEXT_COLOR,
                background_color=INPUT_BACKGROUND,
                **kwargs
            )
        ]


def button(name, **kwargs):
    size = (18, 1)

    return [
        sg.B(
            name,
            border_width=0,
            size=size,
            font=BUTTON_FONT,
            **kwargs
        )
    ]


def layout():
    left = [
        parameter(
            'n_fft',
            tooltip='The size of the FFT window'
        ),
        parameter(
            'hop_length_ms',
            tooltip='The number of audio frames in ms between STFT columns'
        ),
        parameter(
            'win_length_ms',
            tooltip='The size of the FFT window in ms'
        ),
        parameter(
            'ref_level_db',
            tooltip='The reference level dB of audio'
        ),
        parameter(
            'preemphasis',
            tooltip='The coefficient for the preemphasis filter'
        ),
        parameter(
            'min_level_db',
            tooltip='The default dB minimum of the spectrogram and threshold anything below'
        ),
        parameter(
            'min_level_db_floor',
            tooltip='The highest number min_level_db is allowed to reach'
        ),
        parameter(
            'db_delta',
            tooltip='The delta in setting min_level_db'
        ),
        parameter(
            'silence_threshold',
            tooltip='The threshold for a spectrogram to consider noise as silence'
        ),
        parameter(
            'min_silence_for_spec',
            tooltip='The shortest expected length of silence in a recording, which is used to set dynamic threshold'
        ),
        parameter(
            'max_vocal_for_spec',
            tooltip='The longest expected vocalization in seconds'
        ),
    ]

    right = [
        parameter(
            'min_syllable_length_s',
            tooltip='The shortest expected length of a syllable'
        ),
        parameter(
            'spectral_range',
            multi=True,
            tooltip='The spectral range to care about for the spectrogram'
        ),
        parameter(
            'num_mel_bins',
            # tooltip=''
        ),
        parameter(
            'mel_lower_edge_hertz',
            # tooltip=''
        ),
        parameter(
            'mel_upper_edge_hertz',
            # tooltip=''
        ),
        parameter(
            'butter_lowcut',
            # tooltip=''
        ),
        parameter(
            'butter_highcut',
            # tooltip=''
        ),
        parameter(
            'bandpass_filter',
            # tooltip=''
        ),
        parameter(
            'reduce_noise',
            # tooltip=''
        ),
        parameter(
            'mask_spec',
            # tooltip=''
        ),
        parameter(
            'exclude',
            tooltip='A list of indices, which correspond to each segment of a recording',
            disabled=True,
            use_readonly_for_disable=True
        )
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
            button('Previous', key='previous', button_color=BUTTON_BACKGROUND) +
            button('Generate', key='generate', button_color=CTA_BACKGROUND) +
            button('Next', key='next', button_color=BUTTON_BACKGROUND)
        ])],
        [sg.Frame('', border_width=0, pad=(None, (20, 0)), layout=[
            button('Settings', key='settings', button_color=BUTTON_BACKGROUND) +
            button('Reset to Custom', key='reset_custom', button_color=BUTTON_BACKGROUND) +
            button('Reset to Baseline', key='reset_baseline', button_color=BUTTON_BACKGROUND)
        ])],
        [sg.Frame('', border_width=0, pad=(None, (20, 0)), layout=[
            button('Play', key='play', button_color=BUTTON_BACKGROUND) +
            button('Copy', key='copy', button_color=BUTTON_BACKGROUND) +
            button('Save', key='save', button_color=BUTTON_BACKGROUND)
        ])]
    ]
