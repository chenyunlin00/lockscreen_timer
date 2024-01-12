# -*- coding:utf-8 -*-
import time
from ctypes import *
from PyQt5 import QtWidgets, QtCore, QtGui
from threading import Thread

import main_ui as ui
# pyuic5.exe -x .\main.ui -o main_ui.py
__author__ = 'Evan'




class Main(QtWidgets.QDialog, ui.Ui_Dialog, Thread):
    sigShowLCD = QtCore.pyqtSignal(int)
    sigDisableBtnOK = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnOK.clicked.connect(self.startLock)

        self.sigShowLCD.connect(self.lcdNumber.display)
        self.sigDisableBtnOK.connect(self.btnOK.setDisabled)
        self.thread: UpdateThread = None
        self.running = False
        self.lcdNumber.setStyleSheet(
            "border: 1px solid green; color: green; background: black;"
        )
        self.setWindowTitle("锁屏倒计时")
        # self.btnCancel.clicked.connect(self.onBtnCancel)


    def startLock(self) -> None:
        self.sigDisableBtnOK.emit(True)
        self.running = True
        t = UpdateThread(self, self.spinBox.value())
        t.start()
        self.thread = t


    def onBtnCancel(self) -> None:
        self.running = False
        self.sigDisableBtnOK.emit(False)
        self.thread.join()



    def close_windows(self, close_time: int) -> None:
        """
        倒计时锁屏
        :param close_time: 锁屏倒计时间
        :return:
        """
        if close_time <= 0:
            raise ValueError('close time小于等于0，请重新输入')

        while int(close_time) > 0 and self.running:
            print('倒计时: {}'.format(close_time))
            time.sleep(1)
            self.sigShowLCD.emit(close_time)
            close_time -= 1
        if self.running:
            user32 = windll.LoadLibrary('user32.dll')
            user32.LockWorkStation()
            self.sigDisableBtnOK.emit(False)

    def close(self):
        pass

class UpdateThread(Thread):
    def __init__(self, mainClass: Main, closeTime: int):
        super().__init__()
        self.mainClass = mainClass
        self.closeTime = closeTime

    def run(self):
        self.mainClass.close_windows(self.closeTime)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
    window.setWindowFlags(window.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
    window.show()
    sys.exit(app.exec_())
    #close_windows(close_time=3)
