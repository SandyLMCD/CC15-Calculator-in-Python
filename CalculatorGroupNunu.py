from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class Calculator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Calculator.ui", self)
        self.current_input = '0'
        self.stored_value = None
        self.operation = None
        self.reset_input = False
        self.full_expression = ""
        self.default_font_size = self.outputLabel.font().pointSize() 
        self.connect_buttons()
        self.update_display()
    

    def connect_buttons(self):
        self.pushButton0.clicked.connect(lambda: self.number_clicked('0'))
        self.pushButton1.clicked.connect(lambda: self.number_clicked('1'))
        self.pushButton2.clicked.connect(lambda: self.number_clicked('2'))
        self.pushButton3.clicked.connect(lambda: self.number_clicked('3'))
        self.pushButton4.clicked.connect(lambda: self.number_clicked('4'))
        self.pushButton5.clicked.connect(lambda: self.number_clicked('5'))
        self.pushButton6.clicked.connect(lambda: self.number_clicked('6'))
        self.pushButton7.clicked.connect(lambda: self.number_clicked('7'))
        self.pushButton8.clicked.connect(lambda: self.number_clicked('8'))
        self.pushButton9.clicked.connect(lambda: self.number_clicked('9'))
        
        self.additionButton.clicked.connect(lambda: self.operation_clicked('+'))
        self.subtractionButton.clicked.connect(lambda: self.operation_clicked('-'))
        self.multiplicationButton.clicked.connect(lambda: self.operation_clicked('*'))
        self.divideButton.clicked.connect(lambda: self.operation_clicked('/'))
        
        self.clearButton.clicked.connect(self.clear_clicked)
        self.acButton.clicked.connect(self.clear_all_clicked)
        self.equalButton.clicked.connect(self.equals_clicked)
        self.decimalButton.clicked.connect(self.decimal_clicked)
        self.plusminusButton.clicked.connect(self.plusminus_clicked)
        self.percentButton.clicked.connect(self.percent_clicked)
    

    def number_clicked(self, number):
        if self.outputLabel.text() == "Cannot divide by zero":
            self.clear_all_clicked()
        if self.reset_input:
            if self.operation is None:
                self.current_input = number
                self.full_expression = ""  
                self.stored_value = None  
            else:
                self.current_input = number
            self.reset_input = False
        elif self.current_input == '0':
            self.current_input = number
        else:
            self.current_input += number
        self.update_display()
    

    def operation_clicked(self, op):
        if self.outputLabel.text() == "Cannot divide by zero":
            return
        if self.stored_value is None:
            self.stored_value = float(self.current_input)
            if self.stored_value.is_integer():
                self.stored_value = int(self.stored_value)
        elif not self.reset_input:
            self.calculate()
        self.full_expression = f"{self.stored_value} {op} "
        self.operation = op
        self.reset_input = True
        self.update_display()

    def equals_clicked(self):
        if not self.stored_value or not self.operation or not self.current_input.strip():
            self.display_error("Invalid operation or missing operand")
            return
        self.full_expression = f"{self.full_expression}{self.current_input} ="
        self.calculate()
        self.operation = None  
        self.reset_input = True  
        self.stored_value = float(self.current_input)

    def calculate(self):
        try:
            if not self.current_input or self.current_input == '':
                self.display_error("Invalid operation")
                return
            second_number = float(self.current_input)
            if self.operation == '/' and second_number == 0:
                self.display_error("Undefined")
                return
            if self.operation == '+':
                self.stored_value += second_number
            elif self.operation == '-':
                self.stored_value -= second_number
            elif self.operation == '*':
                self.stored_value *= second_number
            elif self.operation == '/':
                self.stored_value /= second_number
            if self.stored_value is not None:
                self.current_input = str(int(self.stored_value)) if self.stored_value.is_integer() else str(self.stored_value)
                self.update_display()
        except ValueError:
            self.display_error("Invalid Input")
    
    # def clear_clicked(self):
    #     print("Clear clicked")
    #     if self.outputLabel.text() == "Cannot divide by zero":
    #         self.clear_all_clicked()
    #         return
    #     if self.reset_input:
    #         # If reset_input is True, reset the current input to '0'
    #         self.current_input = '0'
    #         self.reset_input = False
    #     else:
    #         # Perform backspace: remove the last character of current_input
    #         if len(self.current_input) > 1:
    #             self.current_input = self.current_input[:-1]
    #         else:
    #             # If only one character is left, reset to '0'
    #             self.current_input = '0'
    #     self.update_display()
    
    def clear_clicked(self):
        current_text = self.outputLabel.text() 
        
        # We can check if the current text is one of the error messages, each of them are stored in an array for better readability
        # and to avoid extensive elif statements
        if current_text in [
            "Cannot divide by zero", "Invalid operation", "Undefined", "Invalid Input", "Invalid operation or missing operand"
        ]:
            self.clear_all_clicked()
            return
        
        # Meaning that there is no error message and that there are numbers in the label
        if current_text != "0":
            # Prior to adding this, 'C' would leave out the space after the current number
            # making the user click 'C' twice to remove the space and the number
            if current_text.endswith(" "):
                new_text = current_text[:-3]
            else:
                new_text = current_text[:-1]
        
        # If the new text is empty, we set it to '0'
        if not new_text.strip():
            self.clear_all_clicked()
            self.update_display()
            
        if current_text == "":
            self.outputLabel.setText("0")
            
        self.outputLabel.setText(new_text)
                
        # current_text = self.outputLabel.text()
        # if current_text == "Undefined":
        #     self.clear_all_clicked()
        #     return
        # elif current_text == "Cannot divide by zero":
        #     self.clear_all_clicked()
        #     return
        # elif current_text == "Invalid operation or missing operand":
        #     self.clear_all_clicked()
        #     return
        # elif current_text != "0":
        #     new_text = current_text[:-1]  # Remove last character
        #     if not new_text:  # If text is now empty, show 0
        #         new_text = "0"
        #     self.outputLabel.setText(new_text)

    def clear_all_clicked(self):
        self.reset_calculator_state()
        self.update_display()

    def decimal_clicked(self):
        if self.reset_input:
            self.current_input = '0'
            self.reset_input = False
        if '.' not in self.current_input:
            self.current_input += '.'
        self.update_display()

    def plusminus_clicked(self):
        if self.current_input and self.current_input != '0':
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()

    def percent_clicked(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = str(value)
            self.update_display()
        except ValueError:
            self.display_error("Invalid input for percentage")

    def display_error(self, message):
        self.outputLabel.setText(message)
        self.reset_calculator_state()
        self.adjust_font_size()

    def update_display(self):
        if self.full_expression:
            display_text = f"{self.full_expression}{self.current_input if not self.reset_input else ''}"
        else:
            display_text = self.current_input
        self.outputLabel.setText(display_text)  
        self.adjust_font_size()

    def adjust_font_size(self):
        label = self.outputLabel
        text = label.text()
        font = label.font()
        metrics = QtGui.QFontMetrics(font)
        available_width = label.width() - 20  
        font.setPointSize(self.default_font_size)
        while True:
            metrics = QtGui.QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()
            if text_width <= available_width:
                break
            font.setPointSize(font.pointSize() - 1)
            if font.pointSize() < 8:  
                break
        label.setFont(font)

    def reset_calculator_state(self):
        self.current_input = '0'
        self.stored_value = None
        self.operation = None
        self.full_expression = ""
        self.reset_input = False

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())