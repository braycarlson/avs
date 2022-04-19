import PySimpleGUI as sg
import string

from constant import ICON


# The input field to ignore
IGNORE = (
    'griffin_lim_iters',
    'mask_spec_kwargs',
    'noise_reduce_kwargs',
    'power'
)

# The input field to remove
REMOVE = (
    'browse',
    'canvas',
    'explorer',
    'file',
    'mode'
)

# The input field to ignore in favor of custom processing
CUSTOM = (
    'exclude',
    'spectral_range'
)

# The input field to convert to an integer
INTEGER = (
    'n_fft',
    'hop_length_ms',
    'win_length_ms',
    'ref_level_db',
    'min_level_db',
    'min_level_db_floor',
    'db_delta',
    'spectral_range_low',
    'spectral_range_high',
    'num_mel_bins',
    'mel_lower_edge_hertz',
    'mel_upper_edge_hertz',
    'butter_lowcut',
    'butter_highcut',
)

# The input field to convert to a float
FLOAT = (
    'preemphasis',
    'silence_threshold',
    'min_silence_for_spec',
    'max_vocal_for_spec',
    'min_syllable_length_s',
)

# The input field to convert to a boolean
BOOLEAN = (
    'bandpass_filter',
    'reduce_noise',
    'mask_spec'
)

# The accepted punctuation for an input field
PUNCTUATION = (
    '-',
    '.',
    ',',
    ' ',
)

LOW = (
    'spectral_range_low',
    'mel_lower_edge_hertz',
    'butter_lowcut'
)

HIGH = (
    'spectral_range_high',
    'mel_upper_edge_hertz',
    'butter_highcut'
)


def to_digit(data):
    numerical = [
        character
        for character in data
        if character.isdigit() or character in PUNCTUATION
    ]

    return ''.join(numerical)


def to_exclusion(data):
    exclude = []

    table = str.maketrans(
        dict.fromkeys(
            string.ascii_letters + string.punctuation
        )
    )

    translation = data.translate(table)

    if translation:
        digit = [
            int(character)
            for character in translation.strip().split(' ')
        ]

        digit = sorted(
            set(digit)
        )

        exclude.extend(digit)

    return exclude


def validate(data):
    for key in data:
        if key in CUSTOM or key in IGNORE:
            continue

        if key in BOOLEAN:
            try:
                data[key] = bool(data[key])
            except ValueError:
                sg.Popup(
                    f"{key} must be an bool",
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                return None

        if key in INTEGER:
            try:
                data[key] = int(data[key])
            except ValueError:
                sg.Popup(
                    f"{key} must be an integer",
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                return None

        if key in FLOAT:
            try:
                data[key] = float(data[key])
            except ValueError:
                sg.Popup(
                    f"{key} must be an float",
                    title='Error',
                    icon=ICON,
                    button_color='#242424',
                    keep_on_top=True
                )

                return None

    return data
