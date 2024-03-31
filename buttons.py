import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber
from typing import TYPE_CHECKING

# Quando quer importar apenas por tipagem, utilize isso para evitar
# importação cicular - dois módulos se importando da erro.
# repara que utiliza-se essa tipagem entre aspas, como da pra ver nos
# parâmetros da classe ButtonsGrid

if TYPE_CHECKING:
    from info import Info
    from main_window import MainWindow
    from display import Display


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()  # utilizando assim para não sobreescrever o qss
        font.setPixelSize(MEDIUM_FONT_SIZE)
        # font.setItalic(True)
        # font.setBold(True)
        self.setFont(font)
        self.setMinimumSize(75, 75)  # altura e largura mínima


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.display = display
        self._grid_mask = [
            ["C", "D", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["", "0", ".", "="],
        ]
        self.info = info
        self.window = window
        self._equationInitialValue = 'Sua conta'
        self._equation = self._equationInitialValue
        self._left = None
        self._right = None
        self._op = None
        self._result: float | str = 0.0
        self._makeGrid()
        self._makeSlotClicked()
        self._usedCalculate = False

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
        return

    def clearAll(self):
        self.display.clear()
        self.equation = self._equationInitialValue

    def _makeGrid(self):
        self.display.eqPressed.connect(self.calc)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self.clearAll)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._insertOperInDisplay)
        self.buttons = []
        for x, row in enumerate(self._grid_mask):
            for y, cell in enumerate(row):
                button = Button(cell)
                button.setObjectName(cell)
                self.buttons.append(button)
                # if cell not in '0123456789. ':
                #     button.setProperty('cssClass', 'especialButton')

                if not isNumOrDot(cell) and not isEmpty(cell):
                    button.setProperty('cssClass', 'especialButton')

                self.addWidget(button, x, y)

    def _makeSlotClicked(self):
        for index, _ in enumerate(self.buttons):
            self.buttons[index].clicked.connect(self.finderText)

    @Slot()
    def finderText(self):
        objButton = self.sender()
        tecla = objButton.objectName()

        if not isNumOrDot(tecla) and not isEmpty(tecla):
            self._insertOperInDisplay(tecla)
        else:
            self._insertToDisplay(tecla)


    def _insertToDisplay(self, text):
        if self._result == 'Error':
            self.equation = self._equationInitialValue
            self.display.setText('')
            self._left = None
            self._right = None
            self._op = None
            self._result = 0.0

        newDisplayValue = self.display.text() + text
        if text == '-':
            ...
        elif self._usedCalculate:
            self.display.setText(text)
            self._usedCalculate = False
            return
        elif not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)


    def _insertOperInDisplay(self, tecla):
        # self.display.insert(tecla)
        if self._result == 'Error':
            self.equation = self._equationInitialValue
            self.display.setText('')
            self._left = None
            self._right = None
            self._op = None
            self._result = 0.0

        self._usedCalculate = False
        if tecla == 'C':
            self._left = None
            self._right = None
            self._op = None
            self.equation = self._equationInitialValue
            self.display.clear()

        elif tecla == 'D':
            # new = self.display.text()[:-1]
            # self.display.setText(new)
            self.display.backspace()

        elif tecla in '+-*/^':
            self._operatorPressed(tecla)
        elif tecla == '=':
            self.calc()


    def _operatorPressed(self, tecla):
        displayText = self.display.text()

        if '?' in self.equation and isValidNumber(displayText):
            if displayText == self._result:
                self.calc()
                self._op = tecla
                displayText = self.display.text()
                self._left = convertToNumber(displayText)
                self.display.clear()
                self.equation = f'{self._left} {self._op} ??'
                return

        elif not self._result == 0.0 and displayText == self._result:
            displayText = self._result
            self._left = self._result

        elif displayText == '' and tecla == '-':
            print('selecionou opção')
            if self._equation == self._equationInitialValue:
                self._insertToDisplay(tecla)
            return

        elif not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada')
            return

        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = tecla
        self.equation = f'{self._left} {self._op} ??'
        self.display.clear()

    def calc(self):
        if self._left is None:
            return
        elif not isValidNumber(self.display.text()):
            self._showError('Valor incompleto', False, False)
            return
        elif not self._right is None:
            return

        # self._left = self._left
        self._right = self.display.text()
        self._equation = f'{self._left} {self._op} {self._right}'
        self._result = 'Error'
        try:
            if '^' in self.equation and isinstance(self._left, (float, int)):
                # self._result = eval(self.equation.replace('^', '**'))
                self._result = math.pow(self._left, self._right)
            else:
                self._result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisão por zero')
        except OverflowError:
            self._showError('Essa conta não pode ser realizada')

        self._result = convertToNumber(self._result)
        self.display.setText(str(self._result))
        self.info.setText(f'{self.equation} = {self._result}')
        self._left = None
        self._right = None
        self._usedCalculate = True

    def _showError(self, text: str = '', info: bool = False, buttons: bool = False):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        if info == True:
            msgBox.setInformativeText(
                "Qualquer mensagem que eu quiser."
            )
            msgBox.setIcon(msgBox.Icon.Information)

        if buttons == True:
            msgBox.setStandardButtons(
                msgBox.StandardButton.Save |
                msgBox.StandardButton.Cancel |
                msgBox.StandardButton.Ok
                )
            # msgBox.button(msgBox.StandardButton.Cancel).setText('Mudando')
            # acima: selecionando botão e mudando texto
            msgBox.setIcon(msgBox.Icon.Warning)

            result = msgBox.exec()
            if result == msgBox.StandardButton.Ok:
                print('Usuário clicou em Ok')
            elif result == msgBox.StandardButton.Cancel:
                print('Usuário clicou em Cancelar')
            elif result == msgBox.StandardButton.Save:
                print('Usuário clicou em Save')
        else:
            msgBox.setIcon(msgBox.Icon.NoIcon)
            msgBox.exec()
        # tem varias opções de icones prontas. Todas que começam em maiúsculo
        # são prontas para usar



"""
    Solução que funcionou para o prof e não para mim...

                buttonSlot = self._makeButtonDisplaySlot(
                    self._insertButtonTextToDisplay,
                    button,
                )
                button.clicked.connect(buttonSlot)  # type: ignore

    def _makeButtonDisplaySlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self, button):
        button_text = button.text()
        self.display.insert(button_text)
"""

