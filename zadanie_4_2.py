import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox)


class StringCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка строк по условиям")
        self.setGeometry(100, 100, 500, 200)  # Уменьшил высоту окна, так как элементов стало меньше

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        description = QLabel(
            "Проверка на соответствие регулярным выражениям\n"
            "условие 1: (.*)01*\n"
            "условие 2: (0+1)01\n"
            "условия 3: 00(0+1)*"
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        # Единое поле ввода
        self.input_field = QLineEdit()
        layout.addWidget(QLabel("Введите строку:"))
        layout.addWidget(self.input_field)

        check_all_btn = QPushButton("Проверить все условия")
        check_all_btn.clicked.connect(self.check_all_conditions)
        layout.addWidget(check_all_btn)


        central_widget.setLayout(layout)

    def validate_input(self, s: str) -> bool:
        return all(c in {'0', '1'} for c in s)

    def show_message(self, title: str, message: str):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def check_all_conditions(self):
        s = self.input_field.text()

        condition1 = len(s.rstrip('1')) > 0 and s.rstrip('1')[-1] == '0'
        condition2 = len(s) == 3 and s[1] == '0' and s[2] == '1'
        condition3 = len(s) >= 2 and s[0:2] == '00'

        # Общее сообщение
        self.show_message("Результат проверки",
                          f"Условие 1: {'соответствует' if condition1 else 'не соответствует'}\n"
                          f"Условие 2: {'соответствует' if condition2 else 'не соответствует'}\n"
                          f"Условие 3: {'соответствует' if condition3 else 'не соответствует'}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StringCheckerApp()
    window.show()
    sys.exit(app.exec_())