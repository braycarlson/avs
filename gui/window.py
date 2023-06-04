from __future__ import annotations

import pickle

from ast import literal_eval
from datatype.dataloader import Dataloader
from datatype.signal import Signal
from datatype.settings import Settings
from gui.canvas import Canvas
from gui.explorer import FileExplorer
from gui.menubar import Menubar
from gui.scroll import ScrollableWindow
from gui.parameter import Parameter
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizeGrip,
    QSizePolicy,
    QWidget
)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataframe = None
        self.exclude = set()

        self.setWindowTitle('avs')

        self.icon = QIcon('asset/avs.png')
        self.setWindowIcon(self.icon)

        # Set up the QWidget and the layout
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.menu = Menubar()
        self.layout.setMenuBar(self.menu)

        # Set up the file loading button
        self.explorer = FileExplorer()
        self.layout.addWidget(self.explorer)

        self.figure = Figure()

        self.ax = self.figure.add_subplot(
            111,
            autoscale_on=True,
            projection='spectrogram'
        )

        self.scrollable = ScrollableWindow(self.figure, self.ax)

        self.layout.addWidget(self.scrollable)

        self.parameter = Parameter()
        self.layout.addWidget(self.parameter)

        self.layout.setAlignment(
            self.parameter,
            Qt.AlignmentFlag.AlignCenter
        )

        self.sublayout = QHBoxLayout()

        self.previous = QPushButton('Previous')
        self.generate = QPushButton('Generate')
        self.next = QPushButton('Next')

        self.previous.setFixedSize(150, 30)
        self.generate.setFixedSize(150, 30)
        self.next.setFixedSize(150, 30)

        self.generate.setObjectName('Generate')

        self.sublayout.addStretch(1)
        self.sublayout.addWidget(self.previous)
        self.sublayout.addWidget(self.generate)
        self.sublayout.addWidget(self.next)
        self.sublayout.addStretch(1)

        self.layout.addLayout(self.sublayout)

        self.layout.setAlignment(
            self.sublayout,
            Qt.AlignmentFlag.AlignCenter
        )

        self.next.clicked.connect(self.on_next)
        self.generate.clicked.connect(self.on_generate)
        self.previous.clicked.connect(self.on_previous)
        self.explorer.box.currentIndexChanged.connect(self.on_file_change)
        self.explorer.button.clicked.connect(self.on_click_load)

    def on_generate(self) -> None:
        if len(self.explorer.box) == 0:
            return

        index = self.explorer.box.currentText()
        self.dataloader.update(index)

        self.scrollable.canvas.cleanup()

        self.scrollable.display(
            self.dataloader.current.signal,
            self.dataloader.current.settings
        )

    def on_next(self) -> None:
        if len(self.explorer.box) == 0:
            return

        self.dataloader.next()
        self.explorer.box.setCurrentIndex(self.dataloader.index)

    def on_previous(self) -> None:
        if len(self.explorer.box) == 0:
            return

        self.dataloader.previous()
        self.explorer.box.setCurrentIndex(self.dataloader.index)

    def on_file_change(self) -> None:
        index = self.explorer.box.currentText()
        self.dataloader.update(index)

        self.update()

        self.scrollable.canvas.cleanup()

        self.scrollable.display(
            self.dataloader.current.signal,
            self.dataloader.current.settings
        )

    def update(self) -> None:
        settings = self.dataloader.settings()
        settings = settings.__dict__

        for k, v in settings.items():
            if k in self.parameter.field:
                if isinstance(self.parameter.field[k], tuple):
                    minimum, maximum = self.parameter.field[k]
                    mi, mx = v
                    mi, mx = str(mi), str(mx)

                    minimum.setText(mi)
                    maximum.setText(mx)
                else:
                    v = str(v)
                    self.parameter.field[k].setText(v)

        exclude = settings.get('exclude')
        exclude = set(exclude)

        self.scrollable.canvas.clear()
        self.scrollable.canvas.exclude.update(exclude)

    # def on_click_load(self) -> None:
    #     path, _ = QFileDialog.getOpenFileName(
    #         self,
    #         'Open file',
    #         filter='(*.wav)',
    #         directory='E:/dataset/jedlikowski/132_white_browed_crake'
    #     )

    #     if not path:
    #         return

    #     signal = Signal(path)

    #     settings = Settings.from_file(
    #         'E:/code/personal/warbler.py/warbler.py/settings/spectrogram.json'
    #     )

    #     self.scrollable.canvas.cleanup()
    #     self.scrollable.display(signal, settings)

    def on_click_load(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file',
            filter='Pickle (*.pickle *.pkl *.xz)',
            directory='E:/code/personal/warbler.py/output/pickle/'
        )

        if not path:
            return

        self.dataloader = Dataloader()
        self.dataloader.open(path)

        filelist = self.dataloader.get_all()
        self.explorer.box.addItems(filelist)
