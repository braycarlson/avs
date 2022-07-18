import lzma
import pickle

from constant import EXCLUDE
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
        self._index = 0
        self._length = None
        self.autogenerate = True
        self.current = None
        self.data = None
        self.input = None

    @property
    def empty(self):
        data = self.get_all()

        if self.data is None or len(data) == 0:
            return True

        return False

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = length

    def get_all(self):
        return [
            file.get('filename')
            for file in self.data
        ]

    def load(self, path):
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
        self.input = ui

    def update(self, filename):
        recordings = self.get_all()
        self.index = recordings.index(filename)

        file = self.data[self.index]
        self.current = Node.load(file)


def load_input(window, parameters):
    for key in parameters.keys():
        if key in IGNORE or key in REMOVE:
            continue

        if key == 'spectral_range':
            low, high = parameters[key]

            window['spectral_range_low'].update(low)
            window['spectral_range_high'].update(high)
        else:
            window[key].update(parameters[key])

    exclude = parameters.get('exclude')

    EXCLUDE.clear()
    EXCLUDE.update(exclude)

    if exclude:
        notes = ', '.join([str(note) for note in exclude])
        window['exclude'].update(notes)
    else:
        window['exclude'].update('')
