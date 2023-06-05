import matplotlib as mpl
import os
import sys

from gui.window import Window
from PyQt6.QtWidgets import QApplication


def main() -> None:
    mpl.use('Qt5Agg')
    os.environ['MPLBACKEND'] = 'module://matplotlib.backends.backend_agg_fast'

    app = QApplication(sys.argv)

    window = Window()
    window.showNormal()
    window.setFocus()

    with open('gui/stylesheet.qss', 'r') as handle:
        stylesheet = handle.read()

    app.setStyle('fusion')
    app.setStyleSheet(stylesheet)

    handle = app.exec()
    sys.exit(handle)


if __name__ == "__main__":
    main()
