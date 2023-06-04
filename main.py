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
    window.resize(1600, 800)
    window.show()
    window.showNormal()
    window.setFocus()

    with open('gui/stylesheet.qss', 'r') as handle:
        stylesheet = handle.read()

    app.setStyle('Fusion')
    app.setStyleSheet(stylesheet)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
