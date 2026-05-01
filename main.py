"""
Nicole Tressler
April 21, 2026.
CPSC 4970, Auburn University

Final Project: PyQt5 Interface

"""


"""Entry point for the Curling League Manager application."""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from curling_league_manager.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Curling League Manager")
    app.setApplicationVersion("1.0.0")

    # High-DPI support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
