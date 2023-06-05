from __future__ import annotations

from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget
)


class FileExplorer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.box = QComboBox()

        self.box.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.button = QPushButton('Browse')

        self.button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred
        )

        self.button.setFixedWidth(100)

        self.layout.addWidget(self.box)
        self.layout.addWidget(self.button)

        self.setFixedHeight(50)
