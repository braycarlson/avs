from __future__ import annotations

from gui.floating import Floating
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCloseEvent, QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout
)


class Preferences(Floating):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Preferences')
        self.layout = QVBoxLayout(self)

        self.setFixedSize(400, 200)

        dlayout = QHBoxLayout()
        slayout = QHBoxLayout()

        dlabel = QLabel('Dataset:')
        slabel = QLabel('Settings:')

        self.dataset = QLineEdit()
        self.settings = QLineEdit()

        self.dataset.setReadOnly(True)
        self.settings.setReadOnly(True)

        dbrowse = QPushButton('Browse')
        sbrowse = QPushButton('Browse')

        dbrowse.clicked.connect(self.on_dbrowse)
        sbrowse.clicked.connect(self.on_sbrowse)

        dlayout.addWidget(dlabel)
        slayout.addWidget(slabel)

        dlayout.addWidget(self.dataset)
        slayout.addWidget(self.settings)

        dlayout.addWidget(dbrowse)
        slayout.addWidget(sbrowse)

        self.layout.addLayout(dlayout)
        self.layout.addLayout(slayout)

        self.setLayout(self.layout)

    def load(self) -> None:
        pass

    def on_dbrowse(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            path, *_ = dialog.selectedFiles()
            self.dataset.setText(path)

    def on_sbrowse(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            path, *_ = dialog.selectedFiles()
            self.settings.setText(path)
