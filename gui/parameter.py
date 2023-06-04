from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpacerItem,
    QSizePolicy
)


class Parameter(QWidget):
    def __init__(self):
        super().__init__()

        self.field: dict[str, QLineEdit] = {}

        labels = (
            'n_fft',
            'hop_length_ms',
            'win_length_ms',
            'ref_level_db',
            'preemphasis',
            'min_level_db',
            'min_level_db_floor',
            'db_delta',
            'silence_threshold',
            'min_silence_for_spec',
            'max_vocal_for_spec',
            'min_syllable_length_s',
            'num_mel_bins',
            'spectral_range',
            'mel_lower_edge_hertz',
            'mel_upper_edge_hertz',
            'butter_lowcut',
            'butter_highcut',
            'bandpass_filter',
            'reduce_noise',
            'normalize',
            'dereverberate',
            'mask_spec',
            'realtime'
        )

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)
        self.setLayout(grid)

        rows = len(labels) // 3

        if len(labels) % 3 != 0:
            rows += 1

        for index, label in enumerate(labels, 0):
            row = index % rows
            column = index // rows

            if label == 'spectral_range':
                qlabel = QLabel(label)
                minimum = QLineEdit()
                maximum = QLineEdit()

                layout = QHBoxLayout()

                layout.addWidget(minimum)
                layout.addStretch()
                layout.addWidget(maximum)

                layout.setContentsMargins(0, 0, 0, 0)

                container = QWidget()
                container.setLayout(layout)

                grid.addWidget(qlabel, row, column * 4)
                grid.addWidget(container, row, column * 4 + 1, 1, 3)

                self.field[label] = (minimum, maximum)
            else:
                qlabel = QLabel(label)
                field = QLineEdit()

                grid.addWidget(qlabel, row, column * 4)
                grid.addWidget(field, row, column * 4 + 1, 1, 3)

                spacer = QSpacerItem(
                    40,
                    0,
                    QSizePolicy.Policy.Fixed,
                    QSizePolicy.Policy.Fixed
                )

                grid.addItem(spacer, row, column * 4 + 2)

                self.field[label] = field
