import PySimpleGUI as sg

from abc import ABC, abstractmethod
from constant import ICON


# The input field to ignore
IGNORE = (
    'exclude',
    'griffin_lim_iters',
    'mask_spec_kwargs',
    'noise_reduce_kwargs',
    'power',
    'sample_rate'
)

# The input field to remove
REMOVE = (
    'browse',
    'canvas',
    'explorer',
    'file',
    'mode',
)

# The input field to ignore in favor of custom processing
CUSTOM = (
    'spectral_range_low',
    'spectral_range_high'
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
    'num_mel_bins',
    'spectral_range_low',
    'spectral_range_high',
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
    'normalize',
    'dereverberate',
    'mask_spec',
    'realtime'
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


class Input:
    def __init__(self, data):
        self.data = data

    def to_boolean(self, key):
        if key in BOOLEAN:
            parameter = bool(
                int(
                    self.data.get(key)
                )
            )

            return parameter

    def to_float(self, key):
        if key in FLOAT:
            parameter = float(
                self.data.get(key)
            )

            return parameter

    def to_integer(self, key):
        if key in INTEGER:
            parameter = int(
                self.data.get(key)
            )

            return parameter

    def transform(self):
        func = (
            self.to_boolean,
            self.to_float,
            self.to_integer
        )

        self.data.update({
            k: f(k) for f in func
            for k in self.data.keys()
            if f(k) is not None
        })

        # Spectral Range
        condition = (
            'spectral_range_low' in self.data or
            'spectral_range_high' in self.data
        )

        if condition:
            low = self.data.pop('spectral_range_low')
            high = self.data.pop('spectral_range_high')

            parameter = [low, high]
            self.data['spectral_range'] = parameter

        return self.data

    def validate(self):
        bv = BooleanValidator(self.data)
        iv = IntegerValidator(self.data)
        fv = FloatValidator(self.data)

        if self.data is None:
            return False

        for key in self.data:
            if key in CUSTOM or key in IGNORE:
                continue

            if key in BOOLEAN:
                if not bv.validate(key):
                    return False

            if key in INTEGER:
                if not iv.validate(key):
                    return False

            if key in FLOAT:
                if not fv.validate(key):
                    return False

        return True


class Validator(ABC):
    def __init__(self, data):
        self.data = data
        self.type = 'integer'

    @abstractmethod
    def validate(self, key):
        pass

    def prompt(self, key):
        sg.Popup(
            f"{key} must be an {self.type}",
            title='Error',
            icon=ICON,
            button_color='#242424',
            keep_on_top=True
        )


class IntegerValidator(Validator):
    def __init__(self, data):
        self.data = data
        self.type = 'integer'

    def validate(self, key):
        try:
            parameter = self.data[key]
            self.data[key] = int(parameter)
        except ValueError:
            self.prompt(key)
            return False

        return True


class FloatValidator(Validator):
    def __init__(self, data):
        self.data = data
        self.type = 'float'

    def validate(self, key):
        try:
            parameter = self.data[key]
            self.data[key] = float(parameter)
        except ValueError:
            self.prompt(key)
            return False

        return True


class BooleanValidator(Validator):
    def __init__(self, data):
        self.data = data
        self.type = 'boolean'

    def validate(self, key):
        try:
            parameter = self.data[key]
            parameter = int(parameter)
        except ValueError:
            self.prompt(key)
            return False
        else:
            if parameter == 0:
                self.data[key] = False
                return True

            if parameter == 1:
                self.data[key] = True
                return True

            self.prompt(key)
            return False
