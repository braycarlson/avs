import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import PySimpleGUI as sg

from abc import ABC, abstractmethod
from constant import ICON
from datatype.axes import SpectrogramAxes
from datatype.parameters import Parameters
from datatype.signal import Signal
from datatype.spectrogram import Spectrogram
from event import on_click
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
# from spectrogram.plot import plot_spectrogram
from theme import BUTTON_BACKGROUND
from validation import Input
from vocalseg.dynamic_thresholding import dynamic_threshold_segmentation


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
        path = state.current.parameters
        parameters = Parameters.from_file(path)

        if not state.autogenerate:
            ui = Input(state.input)

            if ui.validate():
                data = ui.transform()
                parameters.update(data)

        path = state.current.signal
        signal = Signal(path)

        if parameters.bandpass_filter:
            signal.filter(
                parameters.butter_lowcut,
                parameters.butter_highcut
            )

        if parameters.reduce_noise:
            signal.reduce()

        spectrogram = Spectrogram(signal, parameters)

        mode = state.input.get('mode')

        if mode == 'Exclusion':
            image = ExclusionSpectrogram(parameters, signal)
            figure = image.create()

            patches = figure.gca().patches

            figure.canvas.mpl_connect(
                'button_press_event',
                lambda event: on_click(
                    event,
                    window,
                    patches
                )
            )
        else:
            spectrogram._spectrogram_nn()
            image = BandwidthSpectrogram(parameters, signal, spectrogram)
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
    def __init__(self, parameters, signal):
        self.parameters = parameters
        self.signal = signal

    def create(self):
        try:
            dts = dynamic_threshold_segmentation(
                self.signal.data,
                self.signal.rate,
                n_fft=self.parameters.n_fft,
                hop_length_ms=self.parameters.hop_length_ms,
                win_length_ms=self.parameters.win_length_ms,
                ref_level_db=self.parameters.ref_level_db,
                pre=self.parameters.preemphasis,
                min_level_db=self.parameters.min_level_db,
                min_level_db_floor=self.parameters.min_level_db_floor,
                db_delta=self.parameters.db_delta,
                silence_threshold=self.parameters.silence_threshold,
                # spectral_range=self.parameters.spectral_range,
                min_silence_for_spec=self.parameters.min_silence_for_spec,
                max_vocal_for_spec=self.parameters.max_vocal_for_spec,
                min_syllable_length_s=self.parameters.min_syllable_length_s,
            )

            spectrogram = dts.get('spec')
            onsets = dts.get('onsets')
            offsets = dts.get('offsets')
        except AttributeError:
            sg.Popup(
                'Please adjust the parameter(s)',
                title='Error',
                icon=ICON,
                button_color=BUTTON_BACKGROUND,
                keep_on_top=True
            )

            return None
        except Exception:
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
            if index in self.parameters.exclude:
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
    def __init__(self, parameters, signal, spectrogram):
        self.parameters = parameters
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
            self.parameters.butter_lowcut,
            color=color,
            ls='dashed',
            lw=1,
            alpha=1
        )

        ax.axhline(
            self.parameters.butter_highcut,
            color=color,
            ls='dashed',
            lw=1,
            alpha=1
        )

        plt.tight_layout()
        return fig
