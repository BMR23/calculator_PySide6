import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QVBoxLayout, QMainWindow, QWidget
from buttons import ButtonsGrid
from info import Info
from main_window import MainWindow
from variables import WINDOW_ICON_PATH
from style import setupTheme
from display import Display


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    setupTheme()

    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)

    # Info
    info = Info("Sua conta")
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)
    # display.setPlaceholderText('Digite algo')

    # Grid
    buttons_grid = ButtonsGrid(display, info, window)

    window.vLayout.addLayout(buttons_grid)
    window.adjustFixedSize()

    window.show()
    app.exec()
