from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Canvas(FigureCanvasTkAgg):
    def __init__(self, figure=None, master=None):
        super().__init__(figure=figure, master=master)
        self.figure = figure
        self.canvas = self.get_tk_widget()
        self.canvas.pack(side='top', fill='both', expand=True)

    def set_figure(self, figure):
        self.figure.gca().clear()
        self.figure.clf()
        plt.close('all')

        width = self.canvas.winfo_width() / 100
        height = self.canvas.winfo_height() / 100

        self.figure = figure
        self.figure.set_figwidth(width)
        self.figure.set_figheight(height)
