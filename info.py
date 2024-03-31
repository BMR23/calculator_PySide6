from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt
from variables import SMALL_FONT_SIZE

# from typing import Optional  # obsoleto. Forma mais nova:
# a | b


class Info(QLabel):
    # era muito mais fácil passar *args e **kwargs
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f"font-size: {SMALL_FONT_SIZE}px;")
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.setMinimumHeight(SMALL_FONT_SIZE + 10)
