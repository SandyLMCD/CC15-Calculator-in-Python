from PyQt5 import QtWidgets
from Calculator import Ui_MainWindow  # Make sure this matches your filename if you saved it separately
import sys

class CalculatorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.expression = ""

        # Connect number buttons
        self.ui.pushButton0.clicked.connect(lambda: self.add_to_expression("0"))
        self.ui.pushButton1.clicked.connect(lambda: self.add_to_expression("1"))
        self.ui.pushButton2.clicked.connect(lambda: self.add_to_expression("2"))
        self.ui.pushButton3.clicked.connect(lambda: self.add_to_expression("3"))
        self.ui.pushButton4.clicked.connect(lambda: self.add_to_expression("4"))
        self.ui.pushButton5.clicked.connect(lambda: self.add_to_expression("5"))
        self.ui.pushButton6.clicked.connect(lambda: self.add_to_expression("6"))
        self.ui.pushButton7.clicked.connect(lambda: self.add_to_expression("7"))
        self.ui.pushButton8.clicked.connect(lambda: self.add_to_expression("8"))
        self.ui.pushButton9.clicked.connect(lambda: self.add_to_expression("9"))
        self.ui.decimalButton.clicked.connect(lambda: self.add_to_expression("."))

        # Connect operator buttons
        self.ui.additionButton.clicked.connect(lambda: self.add_to_expression("+"))
        self.ui.subtractionButton.clicked.connect(lambda: self.add_to_expression("-"))
        self.ui.multiplicationButton.clicked.connect(lambda: self.add_to_expression("*"))
        self.ui.divideButton.clicked.connect(lambda: self.add_to_expression("/"))
        self.ui.percentButton.clicked.connect(self.percent)
        self.ui.plusminusButton.clicked.connect(self.toggle_sign)

        # Functional buttons
        self.ui.clearButton.clicked.connect(self.clear_last)
        self.ui.acButton.clicked.connect(self.clear_all)
        self.ui.equalButton.clicked.connect(self.calculate_result)

    def add_to_expression(self, value):
        self.expression += value
        self.ui.outputLabel.setText(self.expression)

    def clear_last(self):
        self.expression = self.expression[:-1]
        self.ui.outputLabel.setText(self.expression if self.expression else "0")

    def clear_all(self):
        self.expression = ""
        self.ui.outputLabel.setText("0")

    def calculate_result(self):
        try:
            result = str(eval(self.expression))
            self.ui.outputLabel.setText(result)
            self.expression = result
        except:
            self.ui.outputLabel.setText("Error")
            self.expression = ""

    def percent(self):
        try:
            result = str(eval(self.expression) / 100)
            self.ui.outputLabel.setText(result)
            self.expression = result
        except:
            self.ui.outputLabel.setText("Error")
            self.expression = ""

    def toggle_sign(self):
        try:
            if self.expression:
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression
                self.ui.outputLabel.setText(self.expression)
        except:
            self.ui.outputLabel.setText("Error")
            self.expression = ""

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
