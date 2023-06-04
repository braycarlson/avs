from __future__ import annotations

from gui.about import About
from gui.preferences import Preferences
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar


class Menubar(QMenuBar):
    exit = pyqtSignal()
    save = pyqtSignal()

    def __init__(self):
        super().__init__()

        # File
        file = self.addMenu('&File')

        exit = QAction('Exit', parent=self)
        exit.triggered.connect(self.on_click_exit)

        save = QAction('Save', parent=self)
        save.triggered.connect(self.on_click_save)

        file.addAction(save)
        file.addAction(exit)

        # Options
        options = self.addMenu('&Options')

        self.preferences = None

        preferences = QAction('Preferences', parent=self)
        preferences.triggered.connect(self.on_click_preferences)

        options.addAction(preferences)

        # Help
        help = self.addMenu("&Help")

        self.about = None

        about = QAction('About', parent=self)
        about.triggered.connect(self.on_click_about)

        help.addAction(about)

    def on_click_exit(self) -> None:
        self.exit.emit()

    def on_click_save(self) -> None:
        self.save.emit()

    def on_click_about(self) -> None:
        if self.about is not None:
            self.about.activateWindow()
        else:
            self.about = About()
            self.about.exit.connect(self.on_exit_about)

            self.about.geometry()
            self.about.show()

    def on_click_preferences(self) -> None:
        if self.preferences is not None:
            self.preferences.activateWindow()
        else:
            self.preferences = Preferences()
            self.preferences.exit.connect(self.on_exit_preferences)

            self.preferences.geometry()
            self.preferences.show()

    def on_exit_about(self) -> None:
        self.about.close()
        self.about = None

    def on_exit_preferences(self) -> None:
        self.preferences.close()
        self.preferences = None
