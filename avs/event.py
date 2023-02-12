import matplotlib.colors as mcolors

from matplotlib.backend_bases import MouseButton


def on_click(event, state, patches):
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

                facecolor = patch.get_facecolor()
                index = label * 2

                if facecolor == red:
                    color = blue
                    state.exclude.remove(label)
                else:
                    color = red
                    state.exclude.add(label)

                print(state.exclude)

                patch.set_color(color)
                event.inaxes.lines[index].set_color(color)
                event.inaxes.lines[index + 1].set_color(color)

                event.canvas.draw()
