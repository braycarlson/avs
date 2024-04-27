from __future__ import annotations

from gui.about import About
from gui.palette import MAPPING
from gui.preferences import Preferences
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datatype.parser import Parser


class Menubar(QMenuBar):
    # File
    save = pyqtSignal()
    exit = pyqtSignal()

    # Options
    play = pyqtSignal()
    settings = pyqtSignal()
    reset_to_baseline = pyqtSignal()
    reset_to_custom = pyqtSignal()
    preferences = pyqtSignal()

    # Themes
    theme = pyqtSignal(dict)

    def __init__(self, parser: Parser = None):
        super().__init__()

        self.parser = parser

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

        play = QAction('Play', parent=self)
        play.triggered.connect(self.on_click_play)

        settings = QAction('Open Settings', parent=self)
        settings.triggered.connect(self.on_click_settings)

        reset_to_baseline = QAction('Reset to Baseline', parent=self)
        reset_to_baseline.triggered.connect(self.on_click_reset_baseline)

        reset_to_custom = QAction('Reset to Custom', parent=self)
        reset_to_custom.triggered.connect(self.on_click_reset_custom)

        preferences = QAction('Preferences', parent=self)
        preferences.triggered.connect(self.on_click_preferences)

        options.addAction(play)
        options.addAction(settings)
        options.addAction(reset_to_baseline)
        options.addAction(reset_to_custom)
        options.addAction(preferences)

        # Theme
        themes = self.addMenu('&Themes')

        self.brackets = QAction('Brackets', parent=self)
        self.brackets.setCheckable(True)

        self.dracula = QAction('Dracula', parent=self)
        self.dracula.setCheckable(True)

        self.gruvbox = QAction('Gruvbox', parent=self)
        self.gruvbox.setCheckable(True)

        self.onedark = QAction('One Dark', parent=self)
        self.onedark.setCheckable(True)

        self.rosepine = QAction('Rose Pine', parent=self)
        self.rosepine.setCheckable(True)
        self.rosepine.setChecked(True)

        self.brackets.triggered.connect(
            lambda: self.on_change_theme('brackets')
        )

        self.gruvbox.triggered.connect(
            lambda: self.on_change_theme('gruvbox')
        )

        self.dracula.triggered.connect(
            lambda: self.on_change_theme('dracula')
        )

        self.onedark.triggered.connect(
            lambda: self.on_change_theme('onedark')
        )

        self.rosepine.triggered.connect(
            lambda: self.on_change_theme('rosepine')
        )

        themes.addAction(self.brackets)
        themes.addAction(self.dracula)
        themes.addAction(self.gruvbox)
        themes.addAction(self.onedark)
        themes.addAction(self.rosepine)

        # Help
        help = self.addMenu("&Help")

        self.about = None

        about = QAction('About', parent=self)
        about.triggered.connect(self.on_click_about)

        help.addAction(about)

    def on_change_theme(self, name: str) -> None:
        action = {
            'brackets': self.brackets,
            'dracula': self.dracula,
            'gruvbox': self.gruvbox,
            'onedark': self.onedark,
            'rosepine': self.rosepine
        }

        if name in MAPPING:
            theme = MAPPING[name]
            self.theme.emit(theme)

            for k, v in action.items():
                v.setChecked(k == name)

    def on_click_about(self) -> None:
        if self.about is not None:
            self.about.activateWindow()
        else:
            self.about = About()
            self.about.exit.connect(self.on_exit_about)

            self.about.geometry()
            self.about.show()

    def on_click_exit(self) -> None:
        self.exit.emit()

    def on_click_play(self) -> None:
        self.play.emit()

    def on_click_preferences(self) -> None:
        if self.preferences is not None:
            self.preferences.activateWindow()
        else:
            self.preferences = Preferences(self.parser)
            self.preferences.exit.connect(self.on_exit_preferences)

            self.preferences.geometry()
            self.preferences.show()

    def on_click_reset_baseline(self) -> None:
        self.reset_to_baseline.emit()

    def on_click_reset_custom(self) -> None:
        self.reset_to_custom.emit()

    def on_click_save(self) -> None:
        self.save.emit()

    def on_click_settings(self) -> None:
        self.settings.emit()

    def on_exit_about(self) -> None:
        self.about.close()
        self.about = None

    def on_exit_preferences(self) -> None:
        self.preferences.close()
        self.preferences = None
