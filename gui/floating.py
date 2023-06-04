from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCloseEvent, QGuiApplication, QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class Floating(QWidget):
    exit = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.icon = QIcon('asset/avs.png')
        self.setWindowIcon(self.icon)

    def geometry(self) -> None:
        screen = (
            QGuiApplication
            .primaryScreen()
            .availableGeometry()
        )

        self.screen_width = screen.width()
        self.screen_height = screen.height()

        self.window_width = self.width() / 4
        self.window_height = self.height() / 4

        self.wt = (self.screen_width - self.window_width) / 2
        self.ht = (self.screen_height - self.window_height) / 2
        self.wb = self.window_width
        self.hb = self.window_height

        self.setGeometry(
            int(self.wt),
            int(self.ht),
            int(self.wb),
            int(self.hb)
        )

    def closeEvent(self, _: QCloseEvent) -> None:
        self.exit.emit(True)
