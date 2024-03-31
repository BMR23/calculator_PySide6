from PySide6.QtWidgets import QVBoxLayout, QMainWindow, QMessageBox, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)

        self.setCentralWidget(self.cw)
        self.setWindowTitle("Calculadora")

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height() + 20)
        # O label estava espremendo o display. Deixei + espaço para resolver.
        
    def makeMsgBox(self):
        # return QMessageBox(parent=self)  # da na mesma
        return QMessageBox(self)
