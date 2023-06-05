from __future__ import annotations

from gui.floating import Floating
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel


class About(Floating):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('About')
        self.setFixedSize(250, 100)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        author = QLabel('Samantha Huang & Brayden Carlson')
        license = QLabel('GPL v3')
        copyright = QLabel('Copyright © 2023')

        self.layout.addWidget(author)
        self.layout.addWidget(license)
        self.layout.addWidget(copyright)

        self.setLayout(self.layout)
