import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import PySimpleGUI as sg

from action import get_metadata
from constant import ICON
from dataclass.signal import Signal
from dataclass.spectrogram import Spectrogram
from event import on_click
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from parameters import Parameters
from spectrogram.axes import SpectrogramAxes
from spectrogram.plot import (
    plot_spectrogram
)
from validation import to_exclusion
from vocalseg.dynamic_thresholding import dynamic_threshold_segmentation


def draw(canvas, figure):
    figcan = FigureCanvasTkAgg(figure, canvas)
    figcan.draw()

    figcan.get_tk_widget().pack(
        side='top',
        fill='x',
        expand=0
    )

    return figcan


def plot_bandwidth(window, data):
    metadata = get_metadata(data['file'])
    song = metadata.get('song')
    parameter = metadata.get('parameter')

    parameters = Parameters(parameter)

    parameters.n_fft = data['n_fft']
    parameters.hop_length_ms = data['hop_length_ms']
    parameters.win_length_ms = data['win_length_ms']
    parameters.ref_level_db = data['ref_level_db']
    parameters.preemphasis = data['preemphasis']
    parameters.min_level_db = data['min_level_db']
    parameters.min_level_db_floor = data['min_level_db_floor']
    parameters.db_delta = data['db_delta']
    parameters.silence_threshold = data['silence_threshold']
    parameters.min_silence_for_spec = data['min_silence_for_spec']
    parameters.max_vocal_for_spec = data['max_vocal_for_spec']
    parameters.min_syllable_length_s = data['min_syllable_length_s']
    parameters.spectral_range = [
        data['spectral_range_low'],
        data['spectral_range_high']
    ]
    parameters.num_mel_bins = data['num_mel_bins']
    parameters.mel_lower_edge_hertz = data['mel_lower_edge_hertz']
    parameters.mel_upper_edge_hertz = data['mel_upper_edge_hertz']
    parameters.butter_lowcut = data['butter_lowcut']
    parameters.butter_highcut = data['butter_highcut']
    parameters.bandpass_filter = data['bandpass_filter']
    parameters.reduce_noise = data['reduce_noise']
    parameters.mask_spec = data['mask_spec']

    signal = Signal(song)

    signal.filter(
        parameters.butter_lowcut,
        parameters.butter_highcut
    )

    spectrogram = Spectrogram(signal, parameters)

    fig, ax = plt.subplots(
        figsize=(18, 3),
        subplot_kw={'projection': 'spectrogram'}
    )

    fig.patch.set_facecolor('#ffffff')
    ax.patch.set_facecolor('#ffffff')

    plot_spectrogram(
        spectrogram.spectrogram_nn(),
        ax=ax,
        signal=signal,
        cmap=plt.cm.Greys,
    )

    color = mcolors.to_rgba('#d1193e', alpha=0.75)

    ax.axhline(
        parameters.butter_lowcut,
        color=color,
        ls='dashed',
        lw=1,
        alpha=1
    )

    ax.axhline(
        parameters.butter_highcut,
        color=color,
        ls='dashed',
        lw=1,
        alpha=1
    )

    plt.tight_layout()

    return fig


def plot_exclusion(window, data):
    metadata = get_metadata(data['file'])
    song = metadata.get('song')
    parameter = metadata.get('parameter')

    parameters = Parameters(parameter)

    parameters.n_fft = data['n_fft']
    parameters.hop_length_ms = data['hop_length_ms']
    parameters.win_length_ms = data['win_length_ms']
    parameters.ref_level_db = data['ref_level_db']
    parameters.preemphasis = data['preemphasis']
    parameters.min_level_db = data['min_level_db']
    parameters.min_level_db_floor = data['min_level_db_floor']
    parameters.db_delta = data['db_delta']
    parameters.silence_threshold = data['silence_threshold']
    parameters.min_silence_for_spec = data['min_silence_for_spec']
    parameters.max_vocal_for_spec = data['max_vocal_for_spec']
    parameters.min_syllable_length_s = data['min_syllable_length_s']
    parameters.spectral_range = [
        data['spectral_range_low'],
        data['spectral_range_high']
    ]
    parameters.num_mel_bins = data['num_mel_bins']
    parameters.mel_lower_edge_hertz = data['mel_lower_edge_hertz']
    parameters.mel_upper_edge_hertz = data['mel_upper_edge_hertz']
    parameters.butter_lowcut = data['butter_lowcut']
    parameters.butter_highcut = data['butter_highcut']
    parameters.bandpass_filter = data['bandpass_filter']
    parameters.reduce_noise = data['reduce_noise']
    parameters.mask_spec = data['mask_spec']

    signal = Signal(song)

    signal.filter(
        parameters.butter_lowcut,
        parameters.butter_highcut
    )

    try:
        dts = dynamic_threshold_segmentation(
            signal.data,
            signal.rate,
            n_fft=parameters.n_fft,
            hop_length_ms=parameters.hop_length_ms,
            win_length_ms=parameters.win_length_ms,
            ref_level_db=parameters.ref_level_db,
            pre=parameters.preemphasis,
            min_level_db=parameters.min_level_db,
            min_level_db_floor=parameters.min_level_db_floor,
            db_delta=parameters.db_delta,
            silence_threshold=parameters.silence_threshold,
            # spectral_range=parameters.spectral_range,
            min_silence_for_spec=parameters.min_silence_for_spec,
            max_vocal_for_spec=parameters.max_vocal_for_spec,
            min_syllable_length_s=parameters.min_syllable_length_s,
        )

        spectrogram = dts.get('spec')
        onsets = dts.get('onsets')
        offsets = dts.get('offsets')
    except AttributeError:
        sg.Popup(
            'Please adjust the parameter(s)',
            title='Error',
            icon=ICON,
            button_color='#242424',
            keep_on_top=True
        )

        return None
    except Exception:
        sg.Popup(
            'Please adjust the parameter(s)',
            title='Error',
            icon=ICON,
            button_color='#242424',
            keep_on_top=True
        )

        return None

    fig, ax = plt.subplots(
        figsize=(18, 3),
        subplot_kw={'projection': 'spectrogram'}
    )

    fig.patch.set_facecolor('#ffffff')
    ax.patch.set_facecolor('#ffffff')

    plot_spectrogram(
        spectrogram,
        ax=ax,
        signal=signal,
        cmap=plt.cm.Greys,
    )

    ylmin, ylmax = ax.get_ylim()
    ysize = (ylmax - ylmin) * 0.1
    ymin = ylmax - ysize

    patches = []

    blue = mcolors.to_rgba('#0079d3', alpha=0.75)
    red = mcolors.to_rgba('#d1193e', alpha=0.75)

    exclude = to_exclusion(data['exclude'])

    for index, (onset, offset) in enumerate(zip(onsets, offsets), 0):
        if index in exclude:
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

        patches.append(rectangle)

    collection = PatchCollection(
        patches,
        match_original=True
    )

    ax.add_collection(collection)

    plt.tight_layout()

    fig.canvas.mpl_connect(
        'button_press_event',
        lambda event: on_click(
            event,
            window,
            patches
        )
    )

    return fig
