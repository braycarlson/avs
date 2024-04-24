from __future__ import annotations

from datatype.dataloader import Dataloader
from PyQt6.QtCore import QObject, pyqtSignal
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from datatype.parser import Parser
    from pathlib import Path


class Worker(QObject):
    finished = pyqtSignal(Dataloader)
    error = pyqtSignal(str)

    def __init__(self, parser: Parser, path: str | Path):
        super().__init__()

        self.parser = parser
        self.path = path

    def run(self) -> None:
        try:
            dataloader = Dataloader(self.parser)
            dataloader.open(self.path)

            self.finished.emit(dataloader)
        except Exception as exception:
            message = str(exception)
            self.error.emit(message)
