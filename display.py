from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from variables import (TEXT_MARGIN, BIG_FONT_SIZE, MINIMUM_WIDTH)
from utils import isEmpty, isNumOrDot

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        self.setReadOnly(True)

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        # gera: [TEXT_MARGIN, TEXT_MARGIN, TEXT_MARGIN, TEXT_MARGIN]
        self.setStyleSheet(f"font-size:{BIG_FONT_SIZE}px; ")
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # print(event.text())
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key
        
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isOperator = text in '+-*/^'
        
        if isEnter or text == '=':
            self.eqPressed.emit()
            return event.ignore()  
        # ignorando no sentido de não ir nada no display
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
        if isEsc:
            self.clearPressed.emit()
            return event.ignore()
        
        # Não passar daqui se não tiver texto
        if isEmpty(text):
            return event.ignore()
        
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()

        if isOperator:
            self.operatorPressed.emit(text)
            return event.ignore()
