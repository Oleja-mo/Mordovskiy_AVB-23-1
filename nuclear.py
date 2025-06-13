import sys
import time

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QGroupBox, QRadioButton, QTextEdit, QSlider)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette

isCritical = False

class ReactorCore:

    def __init__(self):
        self.active = False
        self.power_percent = 50
        self.max_power = 1000.0

    def get_current_power(self):
        """Текущая мощность в МВт"""
        return self.max_power * (self.power_percent / 100)

    def set_active(self, active):
        self.active = active

    def set_power(self, percent):
        self.power_percent = max(0, min(100, percent))  # Ограничение 0-100%


class PrimaryCoolantLoop:
    """Внутренний водный контур"""

    def __init__(self):
        self.state = "normal"  # normal / critical / emergency
        self.water_temp = 20.0  # °C
        self.heat_capacity = 500.0  # Теплоёмкость контура

    def update(self, reactor_power, energy_absorption, reactor_active, turbine_active, delta_time):
        global isCritical
        if reactor_active:
            # Тепло от реактора к контуру
            heat_input = reactor_power * delta_time * 50
        else:
            heat_input = 0
            # Отведение тепла турбиной (если она активна)
        if turbine_active:
            heat_output = energy_absorption * delta_time * 50 * self.water_temp / 300
        else:
            heat_output = 0

            # Итоговое изменение температуры
        delta_temp = ((heat_input - heat_output) / self.heat_capacity) * (not isCritical)
        self.water_temp += delta_temp
        self.water_temp = max(20.0 + 99999979*isCritical, self.water_temp - 0.5 * delta_time)  # Замедленное остывание

        # Проверка состояния
        if self.water_temp > 400.0 or isCritical:
            self.state = "emergency"
            isCritical = True
        elif self.water_temp > 300.0:
            self.state = "critical"
        else:
            self.state = "normal"


class SecondaryCoolantLoop:
    """Внешний контур (турбина)"""

    def __init__(self):
        self.active = False
        self.energy_absorption = 0.0  # МВт

    def update(self, reactor_power, delta_time):
        if self.active and reactor_power > 0:
            self.energy_absorption = min(reactor_power, 600.0)  # Лимит турбины
        else:
            self.energy_absorption = 0.0

    def set_active(self, active):
        self.active = active


class NuclearPlantSimulator(QMainWindow):
    """Главное окно симулятора АЭС"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("АЭС Симулятор")
        self.setGeometry(100, 100, 800, 600)

        # Инициализация компонентов
        self.reactor = ReactorCore()
        self.primary_loop = PrimaryCoolantLoop()
        self.secondary_loop = SecondaryCoolantLoop()
        self.mode = "auto"  # auto / manual
        self.time_elapsed = 0.0

        # Создание интерфейса
        self.init_ui()

        # Таймер обновления (теперь 0.3 сек)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(300)  # 300 мс = 0.3 сек

    def init_ui(self):
        # Главный контейнер
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Левая панель (управление)
        left_panel = QGroupBox("Управление")
        left_layout = QVBoxLayout()

        # Режим работы
        mode_group = QGroupBox("Режим работы")
        mode_layout = QVBoxLayout()
        self.auto_radio = QRadioButton("Автоматический")
        self.manual_radio = QRadioButton("Ручной")
        self.auto_radio.setChecked(True)
        mode_layout.addWidget(self.auto_radio)
        mode_layout.addWidget(self.manual_radio)
        mode_group.setLayout(mode_layout)

        # Ползунок мощности реактора
        self.power_slider = QSlider(Qt.Horizontal)
        self.power_slider.setRange(0, 100)
        self.power_slider.setValue(50)
        self.power_slider.valueChanged.connect(self.set_reactor_power)

        # Кнопки управления
        self.reactor_btn = QPushButton("Запустить реактор")
        self.reactor_btn.setCheckable(True)
        self.turbine_btn = QPushButton("Включить турбину")
        self.turbine_btn.setCheckable(True)
        self.emergency_btn = QPushButton("АВАРИЙНАЯ ОСТАНОВКА")
        self.reset_btn = QPushButton("Сброс аварии")

        left_layout.addWidget(mode_group)
        left_layout.addWidget(QLabel("Мощность реактора (%):"))
        left_layout.addWidget(self.power_slider)
        left_layout.addWidget(self.reactor_btn)
        left_layout.addWidget(self.turbine_btn)
        left_layout.addWidget(self.emergency_btn)
        left_layout.addWidget(self.reset_btn)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # Правая панель (информация)
        right_panel = QGroupBox("Состояние АЭС")
        right_layout = QVBoxLayout()

        # Индикаторы
        self.reactor_status = QLabel("Реактор: ВЫКЛЮЧЕН")
        self.primary_loop_status = QLabel("Внутренний контур: НОРМА")
        self.secondary_loop_status = QLabel("Турбина: ВЫКЛЮЧЕНА")

        # Параметры
        self.power_label = QLabel("Мощность: 0 МВт")
        self.temp_label = QLabel("Температура: 20 °C")

        # Лог событий
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        right_layout.addWidget(self.reactor_status)
        right_layout.addWidget(self.primary_loop_status)
        right_layout.addWidget(self.secondary_loop_status)
        right_layout.addWidget(self.power_label)
        right_layout.addWidget(self.temp_label)
        right_layout.addWidget(QLabel("Лог событий:"))
        right_layout.addWidget(self.log)
        right_panel.setLayout(right_layout)

        # Сборка интерфейса
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)

        # Подключение кнопок
        self.reactor_btn.clicked.connect(self.toggle_reactor)
        self.turbine_btn.clicked.connect(self.toggle_turbine)
        self.emergency_btn.clicked.connect(self.emergency_shutdown)
        self.reset_btn.clicked.connect(self.reset_plant)
        self.auto_radio.toggled.connect(self.set_auto_mode)
        self.manual_radio.toggled.connect(self.set_manual_mode)

    def toggle_reactor(self):
        """Переключение состояния реактора"""
        self.reactor.set_active(not self.reactor.active)
        status = "запущен" if self.reactor.active else "остановлен"
        self.log.append(f"[Оператор] Реактор {status}.")

    def toggle_turbine(self):
        """Переключение состояния турбины"""
        self.secondary_loop.set_active(not self.secondary_loop.active)
        status = "включена" if self.secondary_loop.active else "выключена"
        self.log.append(f"[Оператор] Турбина {status}.")

    def set_reactor_power(self, value):
        """Установка мощности реактора"""
        self.reactor.set_power(value)
        self.log.append(f"[Оператор] Мощность реактора: {value}%")

    def emergency_shutdown(self):
        global isCritical
        """Аварийная остановка"""
        self.reactor.set_active(False)
        self.primary_loop.state = "emergency"
        isCritical = True
        self.log.append("[АВАРИЯ] Реактор аварийно заглушен!")

    def reset_plant(self):
        """Сброс аварии"""
        global isCritical
        if self.primary_loop.state == "emergency":
            isCritical = False
            self.primary_loop.state = "normal"
            self.primary_loop.water_temp = 20.0  # Сбрасываем температуру до 20°C
            self.log.append("[Оператор] Авария сброшена. Температура восстановлена до 20°C.")

    def set_auto_mode(self, checked):
        """Установка автоматического режима"""
        if checked:
            self.mode = "auto"
            self.log.append("[Система] Включен автоматический режим.")

    def set_manual_mode(self, checked):
        """Установка ручного режима"""
        if checked:
            self.mode = "manual"
            self.log.append("[Система] Включен ручной режим.")

    def update_simulation(self):
        delta_time = 0.3  # Фиксированный интервал 0.3 сек
        self.time_elapsed += delta_time

        # Обновление компонентов
        reactor_power = self.reactor.get_current_power()
        self.secondary_loop.update(reactor_power, delta_time)
        self.primary_loop.update(
            reactor_power=reactor_power,
            energy_absorption=self.secondary_loop.energy_absorption,
            reactor_active=self.reactor.active,
            turbine_active=self.secondary_loop.active,
            delta_time=delta_time
        )

        # Автоматический режим: проверка аварий
        if self.mode == "auto":
            self.auto_safety_checks()

        # Обновление интерфейса
        self.update_ui()

    def auto_safety_checks(self):
        """Проверка безопасности в автоматическом режиме"""
        if self.reactor.active:
            if self.primary_loop.state == "normal":
                new_power = min(100, self.reactor.power_percent + 1)
                self.reactor.set_power(new_power)
                self.power_slider.setValue(new_power)
                self.log.append("[Авто] Увеличение мощности реактора!")
            elif self.primary_loop.state == "critical":
                new_power = max(1, self.reactor.power_percent - 1)
                self.reactor.set_power(new_power)
                self.power_slider.setValue(new_power)
                self.log.append("[Авто] Снижение мощности из-за перегрева!")
                if not self.secondary_loop.active:
                    self.secondary_loop.set_active(True)
            elif self.primary_loop.state == "emergency":
                self.emergency_shutdown()

    def update_ui(self):
        """Обновление интерфейса"""
        # Реактор
        reactor_text = "Реактор: " + ("АКТИВЕН" if self.reactor.active else "ВЫКЛЮЧЕН")
        self.reactor_status.setText(reactor_text)
        self.reactor_btn.setText("Остановить реактор" if self.reactor.active else "Запустить реактор")

        # Внутренний контур
        loop_state = self.primary_loop.state
        if loop_state == "normal":
            loop_text = "Внутренний контур: НОРМА"
            color = QColor(0, 200, 0)  # Зеленый
        elif loop_state == "critical":
            loop_text = "Внутренний контур: КРИТИЧЕСКОЕ СОСТОЯНИЕ!"
            color = QColor(255, 165, 0)  # Оранжевый
        else:
            loop_text = "Внутренний контур: АВАРИЯ!!!"
            color = QColor(255, 0, 0)  # Красный

        self.primary_loop_status.setText(loop_text)
        self.primary_loop_status.setStyleSheet(f"color: {color.name()};")

        # Турбина
        turbine_text = "Турбина: " + ("АКТИВНА" if self.secondary_loop.active else "ВЫКЛЮЧЕНА")
        self.secondary_loop_status.setText(turbine_text)
        self.turbine_btn.setText("Выключить турбину" if self.secondary_loop.active else "Включить турбину")

        # Параметры
        self.power_label.setText(f"Мощность: {self.reactor.get_current_power():.1f} МВт")
        self.temp_label.setText(f"Температура: {self.primary_loop.water_temp:.1f} °C")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulator = NuclearPlantSimulator()
    simulator.show()
    sys.exit(app.exec_())