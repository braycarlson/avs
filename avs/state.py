import json
import lzma
import pickle

from constant import WARBLER
from types import SimpleNamespace
from validation import IGNORE, REMOVE


class Node(SimpleNamespace):
    def __init__(self, **data):
        super().__init__(**data)

    @classmethod
    def load(cls, data):
        return cls(**data)


class State:
    def __init__(self):
        self.index = 0
        self.length = 0
        self.autogenerate = True
        self.current = None
        self.data = None
        self.exclude = set()
        self.ui = None
        self._warbler = None

    @property
    def empty(self):
        data = self.get_all()

        if self.data is None or len(data) == 0:
            return True

        return False

    @property
    def warbler(self):
        return self._warbler

    @warbler.setter
    def warbler(self, warbler):
        self._warbler = warbler

    def get_all(self):
        return [
            file.get('filename')
            for file in self.data
        ]

    def open(self, path):
        with lzma.open(path, 'rb') as handle:
            self.data = pickle.load(handle)
            self.length = len(self.data)

            file = self.data[self.index]
            self.current = Node.load(file)

    def next(self):
        if self.index == self.length - 1:
            self.index = 0
        else:
            self.index = self.index + 1

        self.autogenerate = True

        file = self.data[self.index]
        self.current = Node.load(file)

    def previous(self):
        if self.index == 0:
            self.index = self.length - 1
        else:
            self.index = self.index - 1

        self.autogenerate = True

        file = self.data[self.index]
        self.current = Node.load(file)

    def set(self, ui):
        self.ui = ui

    def update(self, filename):
        recordings = self.get_all()
        self.index = recordings.index(filename)

        file = self.data[self.index]
        self.current = Node.load(file)

    def load(self, window):
        path = WARBLER.joinpath(
            self.current.segmentation
        )

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
