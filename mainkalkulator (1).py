import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup
from kalkulatorz import Ui_MainWindow

class CalculatorApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CalculatorApp, self).__init__()
        self.setupUi(self)  # Load the UI

        # Connect button clicks to the appropriate slots
        self.buttonGroup = QButtonGroup(self)
        self.setup_button_connections()

        # Variable to keep track of operands and operations
        self.first_operand = None
        self.second_operand = None
        self.current_operation = None

    def setup_button_connections(self):
        buttons = [
            self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
            self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_8,
            self.pushButton_9, self.pushButton_10, self.pushButton_11, self.pushButton_12,
            self.pushButton_13, self.pushButton_14, self.pushButton_15, self.pushButton_16,
            self.pushButton_17, self.pushButton_18, self.pushButton_19
        ]
        
        button_names = [
            '1', 'AC', '7', '0', '4', 'M', '8', '5', '2', '%', 'MR', '9', '6', '3', '=',
            ':', 'X', '-', '+'
        ]

        for button, name in zip(buttons, button_names):
            self.buttonGroup.addButton(button)
            button.clicked.connect(lambda state, button_name=name: self.on_button_clicked(button_name))

    def on_button_clicked(self, operation):
        if operation.isdigit() or operation == '.':
            # If digit or '.', update LCD with the number
            current_text = str(self.lcdNumber.value())
            if current_text == '0' and operation.isdigit():
                new_text = operation
            else:
                new_text = current_text + operation
            self.lcdNumber.display(float(new_text))
        elif operation == 'AC':
            # Clear LCD and reset operands and operation
            self.lcdNumber.display(0)
            self.first_operand = None
            self.second_operand = None
            self.current_operation = None
        elif operation in ['+', '-', 'X', ':', '%']:
            # Set the current operation and store the first operand
            if self.first_operand is None:
                self.first_operand = float(self.lcdNumber.value())  # Convert to float
                self.current_operation = operation
                self.lcdNumber.display(0)
        elif operation == '=':
            # Perform the calculation
            if self.first_operand is not None and self.current_operation is not None:
                self.second_operand = float(self.lcdNumber.value())  # Convert to float
                result = self.calculate_result()
                if isinstance(result, str):
                    self.lcdNumber.display(result)  # Display error message
                else:
                    self.lcdNumber.display(result)  # Display result as float
                # Reset operands and operation
                self.first_operand = None
                self.second_operand = None
                self.current_operation = None

    def calculate_result(self):
        # Perform the calculation based on the current operation
        try:
            if self.current_operation == '+':
                return self.first_operand + self.second_operand
            elif self.current_operation == '-':
                return self.first_operand - self.second_operand
            elif self.current_operation == 'X':
                return self.first_operand * self.second_operand
            elif self.current_operation == ':':
                if self.second_operand != 0:
                    return self.first_operand / self.second_operand
                else:
                    return 'Error: Division by zero'
            elif self.current_operation == '%':
                return self.first_operand % self.second_operand
            else:
                return 0
        except Exception as e:
            return f'Error: {str(e)}'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CalculatorApp()
    mainWindow.show()
    sys.exit(app.exec_())
