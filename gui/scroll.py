from __future__ import annotations

import matplotlib.colors as mcolors

from gui.canvas import Canvas
from datatype.segmentation import DynamicThresholdSegmentation
from datatype.spectrogram import Linear, Spectrogram
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QScrollArea,
    QWidget
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datatype.settings import Settings
    from datatype.signal import Signal
    from matplotlib.axes import Axes
    from matplotlib.backend_bases import MouseEvent
    from matplotlib.figure import Figure


class ScrollableWindow(QWidget):
    def __init__(self, fig: Figure, ax: Axes):
        super().__init__()

        self.minimum = 1.0
        self.last = None
        self.zoom = 1.0

        self.canvas = Canvas(fig, ax)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.scroll = QScrollArea(self)
        self.scroll.resizeEvent = self.on_resize
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.canvas)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

        self.setFixedHeight(300)

    @property
    def maximum(self) -> float:
        length = self.canvas.x_maximum - self.canvas.x_minimum
        width = self.canvas.width()

        maximum = width / length

        restriction = 2 ** 16
        image = restriction / width
        return min(maximum, image)

    def on_click(self, event: MouseEvent) -> None:
        if event.inaxes is None:
            return

        if event.button is MouseButton.LEFT:
            position = event.xdata

            for patch in self.canvas.ax.patches:
                start = patch.get_x()
                end = start + patch.get_width()

                if start <= position <= end:
                    label = patch.get_label()
                    label = int(label)

                    blue = mcolors.to_rgba('#0079d3', alpha=0.75)
                    red = mcolors.to_rgba('#d1193e', alpha=0.75)

                    facecolor = patch.get_facecolor()
                    index = label * 2

                    if facecolor == red:
                        color = blue
                        self.canvas.exclude.remove(label)
                    else:
                        color = red
                        self.canvas.exclude.add(label)

                    patch.set_color(color)
                    event.inaxes.lines[index].set_color(color)
                    event.inaxes.lines[index + 1].set_color(color)

                    event.canvas.draw()

            print(self.canvas.exclude)

    def on_motion(self, event: MouseEvent) -> None:
        if hasattr(self, 'press') and self.press:
            x, _ = self.press

            if self.x is not None:
                dx = event.x - x
                self.x = event.x

                scroll = self.scroll.horizontalScrollBar().value()

                factor = 0.5
                scroll = scroll - int(dx * factor)

                self.scroll.horizontalScrollBar().setValue(scroll)
            else:
                self.x = event.x

    def on_press(self, event: MouseEvent) -> None:
        if event.button == MouseButton.RIGHT:
            self.press = event.x, event.y

    def on_release(self, event: MouseEvent) -> None:
        if event.button == MouseButton.RIGHT:
            self.press = None

    def on_resize(self, event: MouseEvent) -> None:
        viewport = self.scroll.viewport().size()
        scroll = event.size().width()

        width = int(scroll * self.zoom)
        height = viewport.height()

        height = int(height)

        self.canvas.setFixedWidth(width)
        self.canvas.setFixedHeight(height)

    def on_scroll(self, event: MouseEvent) -> None:
        rx = event.x / self.canvas.width()
        ry = event.y / self.canvas.height()

        if event.button == 'up':
            if self.zoom >= self.maximum:
                return

            self.zoom = min(self.zoom * 1.50, self.maximum)

        if event.button == 'down':
            if self.zoom <= self.minimum:
                return

            self.zoom = max(self.zoom * 0.50, self.minimum)

        size = self.scroll.viewport().size()
        resize = QResizeEvent(size, size)

        self.on_resize(resize)
        self.canvas.draw_idle()

        sx = int(rx * self.canvas.width() - self.scroll.viewport().width() / 2)
        sy = int(ry * self.canvas.height() - self.scroll.viewport().height() / 2)

        mx = (
            self.scroll.horizontalScrollBar().maximum() -
            self.scroll.horizontalScrollBar().pageStep()
        )

        my = (
            self.scroll.verticalScrollBar().maximum() -
            self.scroll.verticalScrollBar().pageStep()
        )

        sx = min(max(0, sx), mx)
        sy = min(max(0, sy), my)

        self.scroll.horizontalScrollBar().setValue(sx)
        self.scroll.verticalScrollBar().setValue(sy)

    def display(self, signal: Signal, settings: Settings) -> None:
        spectrogram = Spectrogram()
        strategy = Linear(signal, settings)
        spectrogram.strategy = strategy

        spectrogram = spectrogram.generate()

        algorithm = DynamicThresholdSegmentation()
        algorithm.signal = signal
        algorithm.settings = settings
        algorithm.start()

        onsets = algorithm.component.get('onset')
        offsets = algorithm.component.get('offset')

        self.canvas.exclude.update(settings.exclude)

        x_minimum = 0
        x_maximum = signal.duration
        y_minimum = 0
        y_maximum = signal.rate / 2

        self.canvas.x_minimum = x_minimum
        self.canvas.x_maximum = x_maximum

        extent = [
            x_minimum,
            x_maximum,
            y_minimum,
            y_maximum
        ]

        self.canvas.image = self.canvas.ax.matshow(
            spectrogram,
            aspect='auto',
            cmap='inferno',
            extent=extent,
            interpolation=None,
            origin='lower'
        )

        self.canvas.ax.initialize()
        self.canvas.ax._x_lim(x_maximum)
        self.canvas.ax._y_lim(y_maximum)
        self.canvas.ax._x_step(x_maximum)

        ylmin, ylmax = self.canvas.ax.get_ylim()
        ysize = (ylmax - ylmin) * 0.1
        ymin = ylmax - ysize

        for index, (onset, offset) in enumerate(zip(onsets, offsets), 0):
            color = (
                self.canvas.red
                if index in settings.exclude
                else self.canvas.blue
            )

            self.canvas.ax.axvline(
                onset,
                color=color,
                ls='dashed',
                lw=1,
                alpha=0.75
            )

            self.canvas.ax.axvline(
                offset,
                color=color,
                ls='dashed',
                lw=1,
                alpha=0.75
            )

            rectangle = Rectangle(
                xy=(onset, ymin),
                width=offset - onset,
                height=1000,
                alpha=0.75,
                color=color,
                label=str(index)
            )

            rx, ry = rectangle.get_xy()

            self.canvas.ax.add_patch(rectangle)

        if self.canvas.ax.patches:
            length = len(self.canvas.ax.patches) - 1

            remove = [
                index
                for index in self.canvas.exclude
                if index > length
            ]

            self.canvas.exclude.difference_update(remove)

            self.canvas.callback = self.canvas.figure.canvas.mpl_connect(
                'button_press_event',
                self.on_click
            )

        self.canvas.draw()
