import pickle

from constant import EXCLUDE, FILE, FILENAME
from validation import IGNORE, REMOVE


def load_input(window, parameters):
    for key in parameters.keys():
        if key in IGNORE or key in REMOVE:
            continue

        if key == 'spectral_range':
            low, high = parameters[key]

            window['spectral_range_low'].update(low)
            window['spectral_range_high'].update(high)
        else:
            window[key].update(parameters[key])

    exclude = parameters.get('exclude')

    EXCLUDE.clear()
    EXCLUDE.update(exclude)

    if exclude:
        notes = ', '.join([str(note) for note in exclude])
        window['exclude'].update(notes)
    else:
        window['exclude'].update('')


def load_pickle(path):
    with open(path, 'rb') as handle:
        FILE.clear()
        FILENAME.clear()

        FILE.extend(
            pickle.load(handle)
        )

        FILENAME.extend(
            [file.get('filename') for file in FILE]
        )


def get_index(option):
    try:
        index = FILENAME.index(option)
    except ValueError:
        return None
    else:
        return index


def forward(option):
    length = len(FILE)
    index = get_index(option)

    if index == length - 1:
        index = 0
    else:
        index = index + 1

    return index


def backward(option):
    length = len(FILE)
    index = get_index(option)

    if index == 0:
        index = length - 1
    else:
        index = index - 1

    return index


def get_metadata(option):
    metadata = {}

    for file in FILE:
        if file.get('filename') == option:
            metadata.update(file)

    return metadata
