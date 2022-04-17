import matplotlib.colors as mcolors
import numpy as np

from constant import EXCLUDE
from matplotlib.backend_bases import MouseButton


def on_click(event, window, patches):
    if event.inaxes is None:
        return

    if event.button is MouseButton.LEFT:
        position = event.xdata

        for patch in patches:
            start = patch.get_x()
            end = start + patch.get_width()

            if start <= position <= end:
                label = patch.get_label()
                label = int(label)

                blue = mcolors.to_rgba('#0079d3', alpha=0.75)
                red = mcolors.to_rgba('#d1193e', alpha=0.75)

                for collection in event.inaxes.collections:
                    paths = collection.get_paths()
                    colors = collection.get_facecolors()
                    length = len(paths)

                    if len(colors) == 1 and length != 1:
                        colors = np.array([colors[0]] * length)

                    index = label * 2

                    if all(colors[label] == red):
                        color = blue
                        EXCLUDE.remove(label)
                    else:
                        color = red
                        EXCLUDE.add(label)

                    colors[label] = color
                    collection.set_facecolor(colors)
                    collection.set_edgecolor(colors)

                    event.inaxes.lines[index].set_color(color)
                    event.inaxes.lines[index + 1].set_color(color)

                    notes = ', '.join(
                        [str(note) for note in sorted(EXCLUDE)]
                    )

                    window['exclude'].update(notes)
                    window.refresh()

                event.canvas.draw()
