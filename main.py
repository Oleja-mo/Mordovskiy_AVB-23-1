import sys
from PyQt5 import QtWidgets
from AlarmClockWindow import Ui_Dialog
import datetime
from PyQt5.QtCore import QTimer
from db_logger import DBLogger


class myWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        self.dt_now = datetime.datetime.now()
        self.hrs = 0
        self.min = 0
        self.a_hrs = -1
        self.a_mins = -1
        self.sec = 0
        self.rec_A = False
        self.isAlarm = False

        self.logger = DBLogger()
        self.logger.log_event(event_type="APP_START")

        super(myWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushHRS.clicked.connect(self.H)
        self.ui.pushMIN.clicked.connect(self.M)
        self.ui.pushALARM.clicked.connect(self.A)
        self.setTime()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def closeEvent(self, event):
        self.logger.log_event(event_type="APP_EXIT")
        self.logger.close()
        super().closeEvent(event)

    def update_time(self):
        self.dt_now = datetime.datetime.now()
        self.setTime()
        if ((self.isAlarm == False and self.rec_A == False and
             ((int(self.dt_now.hour) + self.hrs) % 24 == self.a_hrs and
              (int(self.dt_now.minute) + self.min) % 60 == self.a_mins) and
             int(self.dt_now.second) == self.sec)):
            self.isAlarm = True
            self.logger.log_event(
            event_type="ALARM_ON",
            current_time=f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}",
            alarm_time=f"{self.a_hrs:02}:{self.a_mins:02}",
            alarm_state=self.isAlarm,
            recording_alarm=self.rec_A
        )
        elif self.isAlarm == True:
            self.ui.text.setPlaceholderText('ALARM!')

    def setTime(self):
        current_time = f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}"
        self.ui.text.setPlaceholderText(current_time)

        # Логирование изменения времени (например, раз в минуту для уменьшения записей)

    def setA_Time(self):
        alarm_time = f"{self.a_hrs:02}:{self.a_mins:02}"
        self.ui.AlarmTime.setPlaceholderText(alarm_time)
        return alarm_time

    def H(self):
        self.logger.log_event(
            event_type="BUTTON_PRESSED",
            button_pressed="HOURS",
            current_time=f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}",
            alarm_state=self.isAlarm,
            recording_alarm=self.rec_A)
        if self.rec_A == False:
            self.hrs = (self.hrs + 1) % 24
            self.update_time()
        else:
            self.a_hrs = (self.a_hrs + 1) % 24
            alarm_time = self.setA_Time()

    def M(self):
        self.logger.log_event(
            event_type="BUTTON_PRESSED",
            button_pressed="MINUTES",
            current_time=f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}",
            alarm_state=self.isAlarm,
            recording_alarm=self.rec_A)
        if self.rec_A == False:
            self.min = (self.min + 1) % 60
            self.update_time()
        else:
            self.a_mins = (self.a_mins + 1) % 60
            alarm_time = self.setA_Time()

    def A(self):
        if self.isAlarm == True:
            self.isAlarm = False
            self.logger.log_event(
                event_type="ALARM_OFF",
                button_pressed="ALARM",
                current_time=f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}",
                alarm_time=f"{self.a_hrs:02}:{self.a_mins:02}",
                alarm_state=self.isAlarm,
                recording_alarm=self.rec_A
            )
        else:
            if self.rec_A == False:
                self.rec_A = True
                self.a_hrs = (int(self.dt_now.hour) + self.hrs) % 24
                self.a_mins = (int(self.dt_now.minute) + self.min) % 60
                alarm_time = self.setA_Time()
                font = self.ui.AlarmTime.font()
                font.setUnderline(True)
                self.ui.AlarmTime.setFont(font)
                self.logger.log_event(
                    event_type="ALARM_REC_STARTED",
                    button_pressed="ALARM",
                    current_time=f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}",
                    alarm_time=alarm_time,
                    alarm_state=self.isAlarm,
                    recording_alarm=self.rec_A
                )
            else:
                self.rec_A = False
                font = self.ui.AlarmTime.font()
                font.setUnderline(False)
                self.ui.AlarmTime.setFont(font)
                self.logger.log_event(
                    event_type="ALARM_REC_FINISHED",
                    button_pressed="ALARM",
                    current_time=f"{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}",
                    alarm_time=f"{self.a_hrs:02}:{self.a_mins:02}",
                    alarm_state=self.isAlarm,
                    recording_alarm=self.rec_A
                )


app = QtWidgets.QApplication([])
application = myWindow()
application.show()
sys.exit(app.exec_())