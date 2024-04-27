from __future__ import annotations

from datatype.axes import LinearAxes
from datatype.parser import Parser
from datatype.settings import Settings
from gui.explorer import FileExplorer
from gui.menubar import Menubar
from gui.scroll import ScrollableWindow
from gui.parameter import Parameter
from gui.worker import Worker
from matplotlib.figure import Figure
from os import startfile
from PyQt6.QtCore import Qt, QThread, QTimer
from PyQt6.QtGui import QIcon, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QProgressDialog,
    QPushButton,
    QFileDialog,
    QWidget
)
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from datatype.dataloader import Dataloader


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('avs')

        self.icon = QIcon('asset/avs.png')
        self.setWindowIcon(self.icon)

        self.move(100, 100)
        self.resize(1600, 800)

        self.progress = QProgressDialog(
            'Loading file..',
            'Cancel',
            0,
            100,
            self
        )

        self.progress.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress.setWindowTitle('avs')
        self.progress.setCancelButton(None)
        self.progress.findChild(QTimer).stop()
        self.progress.setRange(0, 0)
        self.progress.resize(300, 75)
        self.progress.hide()

        self.parser = Parser()
        self.dataframe = None

        self.theme = None

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
            projection='linear'
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
        self.save = QPushButton('Save')
        self.next = QPushButton('Next')

        self.previous.setFixedSize(150, 30)
        self.generate.setFixedSize(150, 30)
        self.save.setFixedSize(150, 30)
        self.next.setFixedSize(150, 30)

        self.generate.setObjectName('Generate')

        self.sublayout.addStretch(1)
        self.sublayout.addWidget(self.previous)
        self.sublayout.addWidget(self.generate)
        self.sublayout.addWidget(self.save)
        self.sublayout.addWidget(self.next)
        self.sublayout.addStretch(1)

        self.layout.addLayout(self.sublayout)

        self.layout.setAlignment(
            self.sublayout,
            Qt.AlignmentFlag.AlignCenter
        )

        self.next.clicked.connect(self.on_next)
        self.generate.clicked.connect(self.on_generate)
        self.save.clicked.connect(self.on_click_save)
        self.previous.clicked.connect(self.on_previous)
        self.explorer.box.currentIndexChanged.connect(self.on_file_change)
        self.explorer.button.clicked.connect(self.on_click_load)
        self.menu.theme.connect(self.apply)
        self.menu.play.connect(self.on_click_play)
        self.menu.reset_to_baseline.connect(self.on_click_reset_baseline)
        self.menu.reset_to_custom.connect(self.on_click_reset_custom)
        self.menu.settings.connect(self.on_click_settings)
        self.menu.save.connect(self.on_click_save)
        self.menu.exit.connect(QApplication.quit)
        self.scrollable.error.connect(self.on_error)

    def create(self) -> None:
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

        exclude = (
            self
            .dataloader
            .current
            .settings
            .exclude
        )

        if self.dataloader.baseline:
            exclude = []

        self.scrollable.canvas.clear()
        settings['exclude'] = exclude

        self.scrollable.display(
            self.dataloader.current.signal,
            settings
        )

    def on_error(self, message: str) -> None:
        QMessageBox.critical(self, 'Error', message)

    def on_generate(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        draw = False

        index = self.explorer.box.currentText()
        self.dataloader.update(index)

        previous = self.dataloader.settings()

        parameters = self.parameter.get()
        settings = Settings.from_dict(parameters)

        if not settings.is_same(previous):
            draw = True

        signal, settings = self.dataloader.signal(settings=settings)

        if draw:
            self.scrollable.canvas.cleanup()
            self.scrollable.canvas.clear()
            settings['exclude'] = []

            self.scrollable.display(
                signal,
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

        self.explorer.box.currentIndexChanged.disconnect(self.on_file_change)

        self.dataloader.next()
        self.explorer.box.setCurrentIndex(self.dataloader.index)

        self.explorer.box.currentIndexChanged.connect(self.on_file_change)

        self.refresh()

    def on_previous(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        self.explorer.box.currentIndexChanged.disconnect(self.on_file_change)

        self.dataloader.previous()
        self.explorer.box.setCurrentIndex(self.dataloader.index)

        self.explorer.box.currentIndexChanged.connect(self.on_file_change)

        self.refresh()

    def on_file_change(self) -> None:
        index = self.explorer.box.currentText()
        self.dataloader.update(index)

        self.refresh()

    def refresh(self) -> None:
        self.update()

        self.scrollable.canvas.clear()
        self.scrollable.canvas.cleanup()

        parameters = self.parameter.get()
        settings = Settings.from_dict(parameters)

        signal, settings = self.dataloader.signal(settings=settings)

        self.scrollable.display(
            signal,
            settings
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

        self.scrollable.canvas.exclude.update(exclude)

    def on_click_load(self) -> None:
        directory = (
            self
            .parser
            .dataset
            .joinpath('output/parquet')
            .as_posix()
        )

        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file',
            filter='Dataset (*parquet)',
            directory=directory
        )

        if path == '':
            return

        if path != '' or path != ' ':
            self.progress.show()

            self.thread = QThread()
            self.worker = Worker(self.parser, path)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_file_load)
            self.worker.error.connect(self.on_load_error)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.progress.reset)

            self.thread.start()

    def on_file_load(self, dataloader: Dataloader) -> None:
        self.progress.reset()

        self.dataloader = dataloader

        filelist = self.dataloader.get_all()
        length = len(filelist)

        self.dataloader.filelist = filelist
        self.dataloader.length = length

        self.explorer.box.currentIndexChanged.disconnect(self.on_file_change)

        self.explorer.box.clear()
        self.explorer.box.addItems(filelist)

        if filelist:
            self.explorer.box.setCurrentIndex(0)

        self.explorer.box.currentIndexChanged.connect(self.on_file_change)

        self.on_file_change()

    def on_load_error(self, message: str) -> None:
        self.progress.reset()

        QMessageBox.critical(
            self,
            'Error',
            f'Failed to load file: {message}'
        )

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

        self.create()

        self.dataloader.baseline = False

    def on_click_reset_custom(self) -> None:
        if len(self.explorer.box) == 0:
            QMessageBox.warning(
                self,
                'Warning',
                'Please load a dataset.'
            )

            return

        self.dataloader.baseline = False

        settings = self.dataloader.settings()
        self.parameter.update(settings)

        self.create()

    def on_click_save(self) -> None:
        settings = self.parameter.get()

        if settings is None:
            QMessageBox.warning(
                self,
                'Warning',
                'A parameter field cannot be empty.'
            )

            return

        settings['exclude'] = list(self.scrollable.canvas.exclude)

        default = self.dataloader.settings()
        default.update(settings)

        path = self.parser.dataset.joinpath(
            self.dataloader.current.segmentation
        )

        default.save(path)

        self.dataloader.reload()

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

    def apply(
        self,
        theme: dict[str, str]
    ) -> None:
        self.theme = theme

        palette = QPalette()

        palette.setColor(
            QPalette.ColorRole.Window,
            theme['base']
        )

        palette.setColor(
            QPalette.ColorRole.WindowText,
            theme['text']
        )

        palette.setColor(
            QPalette.ColorRole.Base,
            theme['surface']
        )

        palette.setColor(
            QPalette.ColorRole.AlternateBase,
            theme['overlay']
        )

        palette.setColor(
            QPalette.ColorRole.ToolTipBase,
            theme['base']
        )

        palette.setColor(
            QPalette.ColorRole.ToolTipText,
            theme['text']
        )

        palette.setColor(
            QPalette.ColorRole.Text,
            theme['text']
        )

        palette.setColor(
            QPalette.ColorRole.Button,
            theme['base']
        )

        palette.setColor(
            QPalette.ColorRole.ButtonText,
            theme['text']
        )

        palette.setColor(
            QPalette.ColorRole.BrightText,
            theme['brightText']
        )

        palette.setColor(
            QPalette.ColorRole.Link,
            theme['link']
        )

        palette.setColor(
            QPalette.ColorRole.Highlight,
            theme['highlight']
        )

        palette.setColor(
            QPalette.ColorRole.HighlightedText,
            theme['highlightedText']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            theme['disabledWindowText']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Button,
            theme['base']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            theme['disabledButtonText']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Text,
            theme['disabledText']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Base,
            theme['surface']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Highlight,
            theme['disabledHighlight']
        )

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.HighlightedText,
            theme['highlightedText']
        )

        app = QApplication.instance()
        app.setPalette(palette)

        widgets = app.allWidgets()

        for widget in widgets:
            widget.setPalette(palette)

        self.scrollable.apply(theme)
