from __future__ import annotations

from datatype.dataloader import Dataloader
from datatype.parser import Parser
from datatype.settings import Settings
from gui.explorer import FileExplorer
from gui.menubar import Menubar
from gui.scroll import ScrollableWindow
from gui.parameter import Parameter
from matplotlib.figure import Figure
from os import startfile
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QWidget
)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('avs')

        self.icon = QIcon('asset/avs.png')
        self.setWindowIcon(self.icon)

        self.move(100, 100)

        self.parser = Parser()
        self.dataframe = None

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.menu = Menubar(self.parser)
        self.layout.setMenuBar(self.menu)

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
        self.menu.play.connect(self.on_click_play)
        self.menu.reset_to_baseline.connect(self.on_click_reset_baseline)
        self.menu.reset_to_custom.connect(self.on_click_reset_custom)
        self.menu.settings.connect(self.on_click_settings)
        self.menu.save.connect(self.on_click_save)
        self.menu.exit.connect(QApplication.quit)

    def on_generate(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        index = self.explorer.box.currentText()
        self.dataloader.update(index)

        self.scrollable.canvas.cleanup()

        parameters = self.parameter.get()
        settings = Settings.from_dict(parameters)

        settings['exclude'] = (
            self
            .dataloader
            .current
            .settings
            .exclude
        )

        self.scrollable.display(
            self.dataloader.current.signal,
            settings
        )

    def on_next(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        self.dataloader.next()
        self.explorer.box.setCurrentIndex(self.dataloader.index)

    def on_previous(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

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
                if k == 'exclude':
                    continue

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

    def on_click_load(self) -> None:
        directory = (
            self
            .parser
            .dataset
            .joinpath('output/pickle')
            .as_posix()
        )

        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file',
            filter='Pickle (*.pickle *.pkl *.xz)',
            directory=directory
        )

        if not path:
            QMessageBox.warning(
                self,
                'Warning',
                'Please provide a valid path.'
            )

            return

        self.dataloader = Dataloader(self.parser)
        self.dataloader.open(path)

        filelist = self.dataloader.get_all()
        self.explorer.box.addItems(filelist)

    def on_click_play(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        path = self.parser.dataset.joinpath(
            self.dataloader.current.recording
        )

        startfile(path)

    def on_click_reset_baseline(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        self.dataloader.baseline = True
        settings = self.dataloader.settings()

        self.parameter.update(settings)
        self.dataloader.baseline = False

        self.on_generate()

    def on_click_reset_custom(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        settings = self.dataloader.settings()
        self.parameter.update(settings)

        self.on_generate()

    def on_click_save(self) -> None:
        settings = self.parameter.get()

        if settings is None:
            QMessageBox.warning(
                self,
                'Warning',
                'A parameter field cannot be empty.'
            )

            return

        settings['exclude'] = self.scrollable.canvas.exclude

        default = self.dataloader.settings()
        default.update(settings)

        path = self.parser.dataset.joinpath(
            self.dataloader.current.segmentation
        )

        default.save(path)

    def on_click_settings(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        path = self.parser.dataset.joinpath(
            self.dataloader.current.segmentation
        )

        startfile(path)
