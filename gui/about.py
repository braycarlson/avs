from __future__ import annotations

from gui.floating import Floating
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCloseEvent, QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget
)


class About(Floating):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('About')
        self.layout = QVBoxLayout(self)

        name = 'Samantha Huang & Brayden Carlson'
        author = QLabel(f"Author(s): {name}")

        license = QLabel('License: GPL v3')
        copyright = QLabel('Copyright© 2023')

        self.layout.addWidget(author)
        self.layout.addWidget(license)
        self.layout.addWidget(copyright)

        self.setLayout(self.layout)
