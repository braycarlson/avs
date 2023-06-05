from __future__ import annotations

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


class Canvas(FigureCanvasQTAgg):
    def __init__(self, figure: Figure = None, ax: Axes = None):
        super().__init__(figure)

        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.Fixed
        )

        self.ax = ax
        self.callback = None
        self.figure = figure
        self.image = None

        self.figure.set_tight_layout(True)

        self.figure.patch.set_facecolor('#222222')
        self.ax.patch.set_facecolor('#222222')

        self.blue = mcolors.to_rgba('#0079d3', alpha=0.75)
        self.red = mcolors.to_rgba('#d1193e', alpha=0.75)

        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.set_axis_off()

        self.draw()

        self.exclude = set()

        self.x_minimum = 0
        self.x_maximum = 0

    def cleanup(self) -> None:
        if self.callback is not None:
            self.figure.canvas.mpl_disconnect(self.callback)

        for text in self.ax.texts:
            text.remove()

        for patch in self.ax.patches:
            patch.remove()

        for line in self.ax.lines:
            line.remove()

        if self.image is not None:
            self.image.remove()

        plt.close(self.figure)

    def clear(self) -> None:
        self.exclude.clear()
