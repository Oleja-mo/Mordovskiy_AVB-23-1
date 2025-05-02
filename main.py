import sys
from PyQt5 import QtWidgets
from AlarmClockWindow import Ui_Dialog
import datetime
from PyQt5.QtCore import QTimer
import winsound


class myWindow(QtWidgets.QMainWindow):
    def update_time(self):
        print(f'isAlarm: {self.isAlarm}, rec_A: {self.rec_A}, play: self.play')
        self.dt_now = datetime.datetime.now()
        self.setTime()
        if  ((self.isAlarm==False and self.rec_A==False and
            ((int(self.dt_now.hour) + self.hrs) % 24)==self.a_hrs and
            (int(self.dt_now.minute) + self.min) % 60==self.a_mins) and
            int(self.dt_now.second) == self.sec):
            self.isAlarm = True
        elif self.isAlarm==True:
            winsound.PlaySound("*", winsound.SND_ALIAS | winsound.SND_ASYNC)

            print('ALARM')


    def setTime(self):
        self.ui.text.setPlaceholderText(
                f'{(int(self.dt_now.hour) + self.hrs) % 24:02}:{(int(self.dt_now.minute) + self.min) % 60:02}:{int(self.dt_now.second):02}')

    def setA_Time(self):
        self.ui.AlarmTime.setPlaceholderText(
                f'{self.a_hrs:02}:{self.a_mins:02}')

    def H(self):
        if self.rec_A == False:
            self.hrs = (self.hrs + 1) % 24
            self.update_time()
        else:
            self.a_hrs = (self.a_hrs + 1) % 24
            self.setA_Time()


    def M(self):
        if self.rec_A == False:
            self.min = (self.min + 1) % 60
            self.update_time()
        else:
            self.a_mins = (self.a_mins + 1) % 60
            self.setA_Time()



    def A(self):
        if self.isAlarm == True:
            self.isAlarm = False
            print('OK')
        else:
            if self.rec_A == False:
                self.rec_A = True
                self.a_hrs = (int(self.dt_now.hour) + self.hrs) % 24
                self.a_mins = (int(self.dt_now.minute) + self.min) % 60
                self.setA_Time()
                font = self.ui.AlarmTime.font()
                font.setUnderline(True)
                self.ui.AlarmTime.setFont(font)
            else:
                self.rec_A = False
                font = self.ui.AlarmTime.font()
                font.setUnderline(False)
                self.ui.AlarmTime.setFont(font)



    def __init__(self, *args, **kwargs):
        self.dt_now = datetime.datetime.now()
        self.hrs = 0
        self.min = 0
        self.a_hrs = -1
        self.a_mins = -1
        self.sec = 0
        self.rec_A = False
        self.isAlarm = False
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


app = QtWidgets.QApplication([])
application = myWindow()
application.show()
sys.exit(app.exec_())
