from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from platformdirs import user_data_dir
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class Parser(ConfigParser):
    def __init__(self):
        super().__init__()
        self._initialize()

    @property
    def dataset(self) -> Path:
        path = self['path']['dataset']
        return Path(path)

    @property
    def settings(self) -> Path:
        path = self['path']['settings']
        return Path(path)

    def _initialize(self) -> None:
        user = user_data_dir(roaming=True)

        self.home = Path(user).joinpath('avs')
        self.home.mkdir(exist_ok=True)

        self.configuration = self.home.joinpath('avs.ini')

        if not self.configuration.exists():
            current = Path.cwd().as_posix()

            self['path'] = {
                'dataset': current,
                'settings': current
            }

            with open(self.configuration, 'w+') as handle:
                self.write(handle)

        self.read(self.configuration)

    def save(self, settings: dict[str, Any]) -> None:
        for k, v in settings.items():
            self['path'][k] = v

        with open(self.configuration, 'w+') as handle:
            self.write(handle)
