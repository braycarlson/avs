import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from datatype.axes import SpectrogramAxes
from datatype.segmentation import dynamic_threshold_segmentation
from datatype.spectrogram import Linear, Spectrogram
from event import on_click
from librosa.util.exceptions import ParameterError
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle


class Canvas(FigureCanvasTkAgg):
    def __init__(self, figure=None, axis=None, master=None):
        super().__init__(figure=figure, master=master)
        self.callback = None
        self.axis = axis
        self.figure = figure
        self.image = None
        self.canvas = self.get_tk_widget()

    def display(self, window, state):
        try:
            signal = state.signal()
        except ParameterError:
            print(state.current.recording)
            return False
        except Exception:
            print(state.current.recording)
            return False

        self.cleanup()

        settings = state.settings()

        spectrogram = Spectrogram()
        strategy = Linear(signal, settings)
        spectrogram.strategy = strategy

        mode = state.ui.get('mode')

        if mode == 'Exclusion':
            try:
                spectrogram = spectrogram.generate()
            except ParameterError:
                print(state.current.recording)
                return False

            if spectrogram is None:
                return False

            try:
                dts = dynamic_threshold_segmentation(
                    signal,
                    settings
                )
            except ValueError:
                print(state.current.recording)
                return False
            except UnboundLocalError:
                print(state.current.recording)
                return False

            onsets = dts.get('onset')
            offsets = dts.get('offset')

            self.figure.patch.set_facecolor('#ffffff')
            self.axis.patch.set_facecolor('#ffffff')

            x_minimum = 0
            x_maximum = signal.duration
            y_minimum = 0
            y_maximum = signal.rate / 2

            extent = [
                x_minimum,
                x_maximum,
                y_minimum,
                y_maximum
            ]

            self.image = self.axis.matshow(
                spectrogram,
                aspect='auto',
                cmap=plt.cm.Greys,
                extent=extent,
                interpolation=None,
                origin='lower'
            )

            self.axis.initialize()
            self.axis._x_lim(x_maximum)
            self.axis._x_step(x_maximum)

            ylmin, ylmax = self.axis.get_ylim()
            ysize = (ylmax - ylmin) * 0.1
            ymin = ylmax - ysize

            blue = mcolors.to_rgba('#0079d3', alpha=0.75)
            red = mcolors.to_rgba('#d1193e', alpha=0.75)

            for index, (onset, offset) in enumerate(zip(onsets, offsets), 0):
                if index in settings.exclude:
                    color = red
                else:
                    color = blue

                self.axis.axvline(
                    onset,
                    color=color,
                    ls='dashed',
                    lw=1,
                    alpha=0.75
                )

                self.axis.axvline(
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
                cx = rx + rectangle.get_width() / 2.0
                cy = ry + rectangle.get_height() / 2.0

                self.axis.annotate(
                    index,
                    (cx, cy),
                    color='white',
                    weight=600,
                    fontfamily='Arial',
                    fontsize=8,
                    ha='center',
                    va='center'
                )

                self.axis.add_patch(rectangle)

            if self.axis.patches:
                length = len(self.axis.patches) - 1

                remove = [
                    index
                    for index in state.exclude
                    if index > length
                ]

                state.exclude.difference_update(remove)

                self.callback = self.figure.canvas.mpl_connect(
                    'button_press_event',
                    lambda event: on_click(
                        event,
                        state,
                        self.axis.patches
                    )
                )
        else:
            spectrogram = spectrogram.generate(normalize=False)

            if spectrogram is None:
                return False

            self.figure.patch.set_facecolor('#ffffff')
            self.axis.patch.set_facecolor('#ffffff')

            x_minimum = 0
            x_maximum = signal.duration
            y_minimum = 0
            y_maximum = signal.rate / 2

            extent = [
                x_minimum,
                x_maximum,
                y_minimum,
                y_maximum
            ]

            self.image = self.axis.matshow(
                spectrogram,
                aspect='auto',
                cmap=plt.cm.Greys,
                extent=extent,
                interpolation=None,
                origin='lower'
            )

            self.axis.initialize()
            self.axis._x_lim(x_maximum)
            self.axis._x_step(x_maximum)

            color = mcolors.to_rgba('#d1193e', alpha=0.75)

            self.axis.axhline(
                settings.butter_lowcut,
                color=color,
                ls='dashed',
                lw=1,
                alpha=1
            )

            self.axis.axhline(
                settings.butter_highcut - 100,
                color=color,
                ls='dashed',
                lw=1,
                alpha=1
            )

        self.canvas.pack(side='top', fill='both', expand=True)
        self.draw()

    def cleanup(self):
        if self.callback is not None:
            self.figure.canvas.mpl_disconnect(self.callback)

        for text in self.axis.texts:
            text.remove()

        for patch in self.axis.patches:
            patch.remove()

        for line in self.axis.lines:
            line.remove()

        if self.image is not None:
            try:
                self.image.remove()
            except ValueError as exception:
                print(exception)

        plt.close(self.figure)
