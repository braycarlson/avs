import json

from constant import SETTINGS, WARBLER
from datatype.dataset import Dataset
from datatype.settings import Settings
from datatype.signal import Signal
from functools import partial
from pathlib import Path
from validation import Input, IGNORE, REMOVE


class State:
    def __init__(self):
        self.index = 0
        self.length = 0
        self.autogenerate = True
        self.baseline = False
        self.current = None
        self.dataframe = None
        self.exclude = set()
        self.ui = None
        self._warbler = None

    @property
    def empty(self):
        data = self.get_all()

        if data is None or len(data) == 0:
            return True

        return False

    @property
    def warbler(self):
        return self._warbler

    @warbler.setter
    def warbler(self, warbler):
        self._warbler = warbler

    def get_all(self):
        return self.dataframe.filename.to_list()

    def open(self, path):
        filename = Path(path).stem

        dataset = Dataset(filename)
        self.dataframe = dataset.load()
        self.current = self.dataframe.iloc[self.index]
        self.length = len(self.dataframe)

    def next(self):
        if self.index == self.length - 1:
            self.index = 0
        else:
            self.index = self.index + 1

        self.autogenerate = True
        self.current = self.dataframe.iloc[self.index]

    def previous(self):
        if self.index == 0:
            self.index = self.length - 1
        else:
            self.index = self.index - 1

        self.autogenerate = True
        self.current = self.dataframe.iloc[self.index]

    def settings(self):
        if self.baseline:
            path = SETTINGS.joinpath('spectrogram.json')
        else:
            path = WARBLER.joinpath(self.current.segmentation)

        settings = Settings.from_file(path)

        if not self.autogenerate:
            ui = Input(self.ui)

            if ui.validate():
                data = ui.transform()
                settings.update(data)

        return settings

    def signal(self):
        if hasattr(self.current, 'signal'):
            signal = self.current.signal
        else:
            settings = self.settings()

            path = WARBLER.joinpath(self.current.recording)
            signal = Signal(path)

            path = SETTINGS.joinpath('dereverberate.json')
            dereverberate = Settings.from_file(path)

            callback = {}

            if settings.bandpass_filter:
                callback['filter'] = partial(
                    signal.filter,
                    settings.butter_lowcut,
                    settings.butter_highcut
                )

            if settings.normalize:
                callback['normalize'] = partial(signal.normalize)

            if settings.dereverberate:
                callback['dereverberate'] = partial(
                    signal.dereverberate,
                    dereverberate
                )

            if settings.reduce_noise:
                callback['reduce'] = partial(signal.reduce)

            # The order should match the warbler.py pipeline
            path = SETTINGS.joinpath('order.json')
            order = Settings.from_file(path)

            functions = list(
                dict(
                    sorted(
                        order.__dict__.items(),
                        key=lambda x: x[1]
                    )
                ).keys()
            )

            for function in functions:
                if function in callback:
                    callback[function]()

        return signal

    def set(self, ui):
        self.ui = ui

    def update(self, filename):
        data = self.get_all()

        self.index = data.index(filename)
        self.current = self.dataframe.iloc[self.index]

    def load(self, window):
        if self.baseline:
            path = SETTINGS.joinpath('spectrogram.json')
        else:
            path = WARBLER.joinpath(self.current.segmentation)

        with open(path, 'r') as handle:
            settings = json.load(handle)

        for key in settings.keys():
            if key in IGNORE or key in REMOVE:
                continue

            if key == 'spectral_range':
                low, high = settings[key]

                window['spectral_range_low'].update(low)
                window['spectral_range_high'].update(high)
            else:
                window[key].update(settings[key])

        exclude = settings.get('exclude')

        self.exclude.clear()
        self.exclude.update(exclude)

        if exclude:
            notes = ', '.join([str(note) for note in exclude])
            window['exclude'].update(notes)
        else:
            window['exclude'].update('')
