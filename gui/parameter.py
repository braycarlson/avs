from __future__ import annotations

from ast import literal_eval
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpacerItem,
    QSizePolicy
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


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
            'realtime',
            'exclude'
        )

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)
        self.setLayout(grid)

        validator = QIntValidator()

        rows = len(labels) // 3

        if len(labels) % 3 != 0:
            rows += 1

        for index, label in enumerate(labels, 0):
            row = index % rows
            column = index // rows

            if label == 'exclude':
                self.field[label] = []
                continue

            if label == 'spectral_range':
                qlabel = QLabel(label)
                minimum = QLineEdit()
                maximum = QLineEdit()

                minimum.setValidator(validator)
                maximum.setValidator(validator)

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

                field.setValidator(validator)

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

    def get(self) -> dict[str, Any] | None:
        parameters = {}

        for key, value in self.field.items():
            if key == 'exclude':
                continue

            if isinstance(value, tuple):
                x, y = value
                x, y = x.text(), y.text()
                x, y = literal_eval(x), literal_eval(y)

                v = (x, y)
            else:
                v = value.text()
                v = literal_eval(v)

            # if not v:
            #     return None

            parameters[key] = v

        return parameters

    def update(self, settings: dict[str, Any]) -> None:
        for key, value in settings.__dict__.items():
            if key not in self.field or key == 'exclude':
                continue

            element = self.field[key]

            if isinstance(element, tuple):
                x, y = value
                x, y = str(x), str(y)

                minimum, maximum = element

                minimum.setText(x)
                maximum.setText(y)
            else:
                value = str(value)
                element.setText(value)
