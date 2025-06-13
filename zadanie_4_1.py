import re
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QMessageBox)


class RegexApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регулярные выражения")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tab1()
        self.create_tab2()
        self.create_tab3()
        self.create_tab4()
        self.create_tab5()

    def create_tab1(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Задание 1.1
        group1 = QVBoxLayout()
        group1.addWidget(QLabel("1) Цепочки с алфавитом {a, b, c}, содержащие хотя бы один 'a' и хотя бы один 'b':"))
        self.regex1_1 = QLineEdit("^(?=.*a)(?=.*b)[abc]+$")
        group1.addWidget(self.regex1_1)
        self.test1_1 = QLineEdit()
        group1.addWidget(QLabel("Тестовая строка:"))
        group1.addWidget(self.test1_1)
        btn1_1 = QPushButton("Проверить")
        btn1_1.clicked.connect(lambda: self.test_regex(self.regex1_1.text(), self.test1_1.text()))
        group1.addWidget(btn1_1)
        layout.addLayout(group1)

        # Задание 1.2
        group2 = QVBoxLayout()
        group2.addWidget(QLabel("2) Цепочки из 0 и 1, где 10-й символ справа равен 1:"))
        self.regex1_2 = QLineEdit("^[01]*1[01]{9}$")
        group2.addWidget(self.regex1_2)
        self.test1_2 = QLineEdit()
        group2.addWidget(QLabel("Тестовая строка:"))
        group2.addWidget(self.test1_2)
        btn1_2 = QPushButton("Проверить")
        btn1_2.clicked.connect(lambda: self.test_regex_long(self.regex1_2.text(), self.test1_2.text(), 10))
        group2.addWidget(btn1_2)
        layout.addLayout(group2)

        # Задание 1.3
        group3 = QVBoxLayout()
        group3.addWidget(QLabel("3) Цепочки из 0 и 1, содержащие не более одной пары последовательных единиц:"))
        self.regex1_3 = QLineEdit("^(?!.*111)(?!.*11.*11)[01]*$")
        group3.addWidget(self.regex1_3)
        self.test1_3 = QLineEdit()
        group3.addWidget(QLabel("Тестовая строка:"))
        group3.addWidget(self.test1_3)
        btn1_3 = QPushButton("Проверить")
        btn1_3.clicked.connect(lambda: self.test_regex(self.regex1_3.text(), self.test1_3.text()))
        group3.addWidget(btn1_3)
        layout.addLayout(group3)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Задание 1")

    def create_tab2(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Задание 2а
        group1 = QVBoxLayout()
        group1.addWidget(QLabel("а) Цепочки из 0 и 1, где каждая пара смежных 0 перед парой смежных 1:"))
        self.regex2_a = QLineEdit("^(?!.*11.*00)[01]*$")
        group1.addWidget(self.regex2_a)
        self.test2_a = QLineEdit()
        group1.addWidget(QLabel("Тестовая строка:"))
        group1.addWidget(self.test2_a)
        btn2_a = QPushButton("Проверить")
        btn2_a.clicked.connect(lambda: self.test_regex(self.regex2_a.text(), self.test2_a.text()))
        group1.addWidget(btn2_a)
        layout.addLayout(group1)

        # Задание 2б
        group2 = QVBoxLayout()
        group2.addWidget(QLabel("б) Цепочки из 0 и 1, где число 0 кратно 5:"))
        self.regex2_b = QLineEdit("^(1*0){5}1*)*$")
        group2.addWidget(self.regex2_b)
        self.test2_b = QLineEdit()
        group2.addWidget(QLabel("Тестовая строка:"))
        group2.addWidget(self.test2_b)
        btn2_b = QPushButton("Проверить")
        btn2_b.clicked.connect(lambda: self.test_regex_count(self.regex2_b.text(), self.test2_b.text(), '0', 5))
        group2.addWidget(btn2_b)
        layout.addLayout(group2)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Задание 2")

    def create_tab3(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Задание 3.1
        group1 = QVBoxLayout()
        group1.addWidget(QLabel("1) Цепочки из 0 и 1, в которых нет подцепочки 101:"))
        self.regex3_1 = QLineEdit("^(?!.*101)[01]*$")
        group1.addWidget(self.regex3_1)
        self.test3_1 = QLineEdit()
        group1.addWidget(QLabel("Тестовая строка:"))
        group1.addWidget(self.test3_1)
        btn3_1 = QPushButton("Проверить")
        btn3_1.clicked.connect(lambda: self.test_regex(self.regex3_1.text(), self.test3_1.text()))
        group1.addWidget(btn3_1)
        layout.addLayout(group1)

        # Задание 3.2
        group2 = QVBoxLayout()
        group2.addWidget(QLabel("2) Цепочки с поровну 0 и 1 и без префиксов с разницей >2:"))
        self.regex3_2 = QLineEdit("^(01|10)((1010|0101|1100|0110|011|1001)(?!000|111))*$")
        group2.addWidget(self.regex3_2)
        self.test3_2 = QLineEdit()
        group2.addWidget(QLabel("Тестовая строка:"))
        group2.addWidget(self.test3_2)
        btn3_2 = QPushButton("Проверить")
        btn3_2.clicked.connect(lambda: self.test_balanced(self.test3_2.text()))
        group2.addWidget(btn3_2)
        layout.addLayout(group2)

        # Задание 3.3
        group3 = QVBoxLayout()
        group3.addWidget(QLabel("3) Цепочки из 0 и 1, где число 0 делится на 5, а число 1 четно:"))
        self.regex3_3 = QLineEdit("^(?=(.*0.*){5}$)(?=(.*1.*){2}$)[01]+$")
        group3.addWidget(self.regex3_3)
        self.test3_3 = QLineEdit()
        group3.addWidget(QLabel("Тестовая строка:"))
        group3.addWidget(self.test3_3)
        btn3_3 = QPushButton("Проверить")
        btn3_3.clicked.connect(lambda: self.test_regex_double(self.regex3_3.text(), self.test3_3.text()))
        group3.addWidget(btn3_3)
        layout.addLayout(group3)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Задание 3")

    def create_tab4(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group = QVBoxLayout()
        group.addWidget(QLabel("Регулярное выражение для телефонных номеров:"))
        self.regex4 = QLineEdit(r"^(?:\+?\d{1,3}[ -]?)?(?:\(\d{1,4}\)|\d{1,4})[ -]?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,9}$"
                                r"|^0[1-9]$|^1(?:1[02-9]|33|5[0-35-9]|7[0-7]|8[0-8]|9[1-9])$|^9(?:11|9[1-9])$")
        group.addWidget(self.regex4)
        self.test4 = QLineEdit()
        group.addWidget(QLabel("Тестовый номер:"))
        group.addWidget(self.test4)
        btn4 = QPushButton("Проверить")
        btn4.clicked.connect(lambda: self.test_regex(self.regex4.text(), self.test4.text()))
        group.addWidget(btn4)

        examples = QTextEdit()
        examples.setPlainText("Примеры номеров:\n"
                              "+7 123 456-78-90\n"
                              "8(123)4567890\n"
                              "+1 (123) 456-7890\n"
                              "123-4567\n"
                              "+44 20 1234 5678")
        examples.setReadOnly(True)
        group.addWidget(examples)

        layout.addLayout(group)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Задание 4")

    def create_tab5(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group = QVBoxLayout()
        group.addWidget(QLabel("Регулярное выражение для зарплаты:"))
        self.regex5 = QLineEdit(
            r"(?i)(?:(?:зарплата|з\/п|ставка|оплата|оклад|заработная плата)\s*:?\s*)?(?:от\s*\d{1,3}(?:\s?\d{3})*(?:\.\d{2})?\s*(?:до\s*\d{1,3}(?:\s?\d{3})*(?:\.\d{2})?)?|\$?\s*\d{1,3}(?:\s?\d{3})*(?:\.\d{2})?)(?:\s?руб\.?|\s?USD|\s?\$)?(?:\s*(?:в\s+|/)\s*(?:час|ч|день|недел[юя]|месяц|мес|год))?")
        group.addWidget(self.regex5)
        self.test5 = QLineEdit()
        group.addWidget(QLabel("Тестовая зарплата:"))
        group.addWidget(self.test5)
        btn5 = QPushButton("Проверить")
        btn5.clicked.connect(lambda: self.test_regex(self.regex5.text(), self.test5.text()))
        group.addWidget(btn5)

        examples = QTextEdit()
        examples.setPlainText("Примеры зарплат:\n"
                              "50000 руб.\n"
                              "от $1000 в месяц\n"
                              "2500 USD/месяц\n"
                              "зарплата: 150000\n"
                              "100-200 руб. в час\n"
                              "оклад 75000")
        examples.setReadOnly(True)
        group.addWidget(examples)

        layout.addLayout(group)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Задание 5")

    def test_regex(self, pattern, text):
        try:
            if re.fullmatch(pattern, text):
                QMessageBox.information(self, "Результат", "Строка соответствует регулярному выражению!")
            else:
                QMessageBox.warning(self, "Результат", "Строка НЕ соответствует регулярному выражению.")
        except re.error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в регулярном выражении: {str(e)}")

    def test_regex_long(self, pattern, text, min_length):
        try:
            if len(text) < min_length:
                QMessageBox.warning(self, "Результат", f"Строка должна быть не короче {min_length} символов")
            elif re.fullmatch(pattern, text):
                QMessageBox.information(self, "Результат", "Строка соответствует регулярному выражению!")
            else:
                QMessageBox.warning(self, "Результат", "Строка НЕ соответствует регулярному выражению.")
        except re.error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в регулярном выражении: {str(e)}")

    def test_regex_count(self, pattern, text, char, multiple):
        try:
            if re.fullmatch(pattern, text):
                count = text.count(char)
                if count % multiple == 0:
                    QMessageBox.information(self, "Результат", f"Строка соответствует!")
                else:
                    QMessageBox.warning(self, "Результат",
                                        f"Строка соответствует шаблону, но количество '{char}' ({count}) не кратно {multiple}.")
            else:
                QMessageBox.warning(self, "Результат", "Строка НЕ соответствует регулярному выражению.")
        except re.error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в регулярном выражении: {str(e)}")

    def test_regex_double(self, pattern, text):
        try:
            if re.fullmatch(pattern, text):
                zeros = text.count('0')
                ones = text.count('1')
                if zeros % 5 == 0 and ones % 2 == 0:
                    QMessageBox.information(self, "Результат", f"Строка соответствует (0: {zeros}, 1: {ones})!")
                else:
                    QMessageBox.warning(self, "Результат",
                                        f"Строка соответствует шаблону, но условия не выполнены (0: {zeros}, 1: {ones}).")
            else:
                QMessageBox.warning(self, "Результат", "Строка НЕ соответствует регулярному выражению.")
        except re.error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в регулярном выражении: {str(e)}")

    def test_balanced(self, text):
        zeros = text.count('0')
        ones = text.count('1')

        if zeros != ones:
            QMessageBox.warning(self, "Результат", f"Количество 0 ({zeros}) и 1 ({ones}) не совпадает.")
            return

        balance = 0
        for i, char in enumerate(text):
            if char == '0':
                balance += 1
            else:
                balance -= 1

            if abs(balance) > 2:
                QMessageBox.warning(self, "Результат",
                                    f"Префикс '{text[:i + 1]}' имеет разницу {abs(balance)} (порог 2).")
                return

        QMessageBox.information(self, "Результат", "Строка удовлетворяет всем условиям!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegexApp()
    window.show()
    sys.exit(app.exec_())