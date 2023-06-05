"""
Dataloader
----------

"""

from __future__ import annotations

from datatype.dataset import Dataset
from datatype.settings import Settings
from datatype.signal import Signal
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datatype.parser import Parser


class Dataloader:
    def __init__(self, parser: Parser = None):
        self.index = 0
        self.length = 0
        self.baseline = False
        self.current = None
        self.dataframe = None
        self.filelist = None
        self.parser = parser
        self.realtime = False
        self.ui = None

    @property
    def empty(self) -> bool:
        data = self.get_all()

        if data is None or len(data) == 0:
            return True

        return False

    def get_all(self) -> list[str]:
        return self.dataframe.filename.to_list()

    def open(self, path: str | Path) -> None:
        filename = Path(path).stem

        dataset = Dataset(filename)
        self.dataframe = dataset.load()

        self.current = self.dataframe.iloc[self.index]
        self.length = len(self.dataframe)
        self.filelist = self.get_all()

    def next(self) -> None:
        if self.index == self.length - 1:
            self.index = 0
        else:
            self.index = self.index + 1

        self.current = self.dataframe.iloc[self.index]

    def previous(self) -> None:
        if self.index == 0:
            self.index = self.length - 1
        else:
            self.index = self.index - 1

        self.current = self.dataframe.iloc[self.index]

    def settings(self) -> Settings:
        if self.baseline:
            path = (
                self
                .parser
                .settings
                .joinpath('spectrogram.json')
            )
        else:
            path = (
                self
                .parser
                .dataset
                .joinpath(self.current.segmentation)
            )

        return Settings.from_file(path)

    def signal(self) -> Signal:
        if hasattr(self.current, 'signal'):
            signal = self.current.signal

        settings = self.settings()

        if not hasattr(self.current, 'signal') or settings.realtime:
            path = (
                self
                .parser
                .dataset
                .joinpath(self.current.recording)
            )

            signal = Signal(path)

            path = self.parser.settings.joinpath('dereverberate.json')
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
            path = self.parser.settings.joinpath('order.json')
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

    def update(self, filename: str) -> None:
        data = self.get_all()

        self.index = data.index(filename)
        self.current = self.dataframe.iloc[self.index]
