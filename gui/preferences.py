from __future__ import annotations

from gui.floating import Floating
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datatype.parser import Parser


class Preferences(Floating):
    def __init__(self, parser: Parser = None):
        super().__init__()

        self.parser = parser

        self.setWindowTitle('Preferences')
        self.setFixedSize(350, 150)

        self.layout = QVBoxLayout(self)

        dlayout = QHBoxLayout()
        slayout = QHBoxLayout()
        group = QHBoxLayout()

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

        dataset = str(self.parser.dataset)
        settings = str(self.parser.settings)

        self.dataset.setText(dataset)
        self.settings.setText(settings)

        self.save = QPushButton('Save')
        self.cancel = QPushButton('Cancel')

        self.save.clicked.connect(self.on_save)
        self.cancel.clicked.connect(self.on_cancel)

        self.save.setObjectName('Save')

        group.addWidget(self.save)
        group.addWidget(self.cancel)

        self.layout.addLayout(dlayout)
        self.layout.addLayout(slayout)
        self.layout.addSpacing(20)
        self.layout.addLayout(group)

        self.setLayout(self.layout)

    def on_cancel(self) -> None:
        self.exit.emit(True)

    def on_dbrowse(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            path, *_ = dialog.selectedFiles()
            self.dataset.setText(path)

    def on_save(self) -> None:
        settings = {
            'dataset': self.dataset.text(),
            'settings': self.settings.text(),
        }

        self.parser.save(settings)

        QMessageBox.information(
            self,
            'Success',
            'Preferences saved.'
        )

    def on_sbrowse(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            path, *_ = dialog.selectedFiles()
            self.settings.setText(path)
