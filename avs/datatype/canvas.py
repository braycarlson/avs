import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import PySimpleGUI as sg

from abc import ABC, abstractmethod
from constant import ICON, WARBLER
from copy import copy
from datatype.axes import SpectrogramAxes
from datatype.segmentation import dynamic_threshold_segmentation
from datatype.settings import Settings
from datatype.signal import Signal
from datatype.spectrogram import Linear, Spectrogram
from event import on_click, on_draw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from theme import BUTTON_BACKGROUND
from validation import Input


class Canvas(FigureCanvasTkAgg):
    def __init__(self, figure=None, master=None):
        super().__init__(figure=figure, master=master)
        self.figure = figure
        self.canvas = self.get_tk_widget()
        self.canvas.pack(side='top', fill='both', expand=True)

    @property
    def width(self):
        return self.canvas.winfo_width() / 100

    @property
    def height(self):
        return self.canvas.winfo_height() / 100

    def prepare(self, window, state):
        path = WARBLER.joinpath(state.current.segmentation)
        settings = Settings.from_file(path)

        if not state.autogenerate:
            ui = Input(state.ui)

            if ui.validate():
                data = ui.transform()
                settings.update(data)

        if hasattr(state.current, 'dereverberate'):
            signal = copy(state.current.dereverberate)
        else:
            path = WARBLER.joinpath(state.current.recording)
            signal = Signal(path)

        if settings.bandpass_filter:
            signal.filter(
                settings.butter_lowcut,
                settings.butter_highcut
            )

        if settings.reduce_noise:
            signal.reduce()

        spectrogram = Spectrogram()
        strategy = Linear(signal, settings)
        spectrogram.strategy = strategy

        spectrogram = spectrogram.generate()

        mode = state.ui.get('mode')

        if mode == 'Exclusion':
            image = ExclusionSpectrogram(settings, signal)
            figure = image.create()

            if figure is None:
                return None

            patches = figure.gca().patches

            if patches:
                length = len(patches) - 1

                remove = [
                    index
                    for index in state.exclude
                    if index > length
                ]

                state.exclude.difference_update(remove)

                notes = ', '.join(
                    [
                        str(note)
                        for note in sorted(state.exclude)
                    ]
                )

                window['exclude'].update(notes)

                figure.canvas.mpl_connect(
                    'button_press_event',
                    lambda event: on_click(
                        event,
                        window,
                        state,
                        patches
                    )
                )
        else:
            spectrogram = Spectrogram()
            strategy = Linear(signal, settings)
            spectrogram.strategy = strategy

            spectrogram = spectrogram.generate(normalize=False)
            image = BandwidthSpectrogram(settings, signal, spectrogram)
            figure = image.create()

        return figure

    def close(self):
        plt.close(self.figure)

    def set(self, figure):
        self.close()

        self.figure = figure
        self.figure.set_figwidth(self.width)
        self.figure.set_figheight(self.height)


class Plot(ABC):
    @abstractmethod
    def create(self):
        pass

    def plot(self, **kwargs):
        ax = kwargs.pop('ax')
        signal = kwargs.pop('signal')
        spectrogram = kwargs.pop('spectrogram')

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

        image = ax.matshow(
            spectrogram,
            aspect='auto',
            extent=extent,
            interpolation=None,
            origin='lower',
            **kwargs
        )

        ax.initialize()
        ax._x_lim(x_maximum)
        ax._x_step(x_maximum)

        return image


class ExclusionSpectrogram(Plot):
    def __init__(self, settings, signal):
        self.settings = settings
        self.signal = signal

    def create(self):
        try:
            dts = dynamic_threshold_segmentation(
                self.signal,
                self.settings
            )

            spectrogram = dts.get('spectrogram')
            onsets = dts.get('onset')
            offsets = dts.get('offset')
        except AttributeError as exception:
            print(exception)

            sg.Popup(
                'Please adjust the parameter(s)',
                title='Error',
                icon=ICON,
                button_color=BUTTON_BACKGROUND,
                keep_on_top=True
            )

            return None
        except Exception as exception:
            print(exception)

            sg.Popup(
                'Please adjust the parameter(s)',
                title='Error',
                icon=ICON,
                button_color=BUTTON_BACKGROUND,
                keep_on_top=True
            )

            return None

        fig, ax = plt.subplots(
            figsize=(18, 3),
            subplot_kw={'projection': 'spectrogram'}
        )

        fig.patch.set_facecolor('#ffffff')
        ax.patch.set_facecolor('#ffffff')

        self.plot(
            ax=ax,
            cmap=plt.cm.Greys,
            signal=self.signal,
            spectrogram=spectrogram
        )

        ylmin, ylmax = ax.get_ylim()
        ysize = (ylmax - ylmin) * 0.1
        ymin = ylmax - ysize

        blue = mcolors.to_rgba('#0079d3', alpha=0.75)
        red = mcolors.to_rgba('#d1193e', alpha=0.75)

        for index, (onset, offset) in enumerate(zip(onsets, offsets), 0):
            if index in self.settings.exclude:
                color = red
            else:
                color = blue

            ax.axvline(
                onset,
                color=color,
                ls='dashed',
                lw=1,
                alpha=0.75
            )

            ax.axvline(
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

            ax.annotate(
                index,
                (cx, cy),
                color='white',
                weight=600,
                fontfamily='Arial',
                fontsize=8,
                ha='center',
                va='center'
            )

            ax.add_patch(rectangle)

        plt.tight_layout()
        return fig


class BandwidthSpectrogram(Plot):
    def __init__(self, settings, signal, spectrogram):
        self.settings = settings
        self.signal = signal
        self.spectrogram = spectrogram

    def create(self):
        fig, ax = plt.subplots(
            figsize=(18, 3),
            subplot_kw={'projection': 'spectrogram'}
        )

        cmap = plt.cm.Greys

        self.plot(
            ax=ax,
            cmap=cmap,
            signal=self.signal,
            spectrogram=self.spectrogram.data
        )

        fig.patch.set_facecolor('#ffffff')
        ax.patch.set_facecolor('#ffffff')

        color = mcolors.to_rgba('#d1193e', alpha=0.75)

        ax.axhline(
            self.settings.butter_lowcut,
            color=color,
            ls='dashed',
            lw=1,
            alpha=1
        )

        ax.axhline(
            self.settings.butter_highcut,
            color=color,
            ls='dashed',
            lw=1,
            alpha=1
        )

        plt.tight_layout()
        return fig
