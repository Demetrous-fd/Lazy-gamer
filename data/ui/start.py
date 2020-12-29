#!/urs/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
import settings
import sys



URL1 = "https://cdn1.epicgames.com/d5241c76f178492ea1540fce45616757/offer/EGS_HolidaySale2020_DoG_AlienIsolation_1920x1080_Teaser-R-1920x1080-2d7e1be9cc7c6583832158bc4214c981.jpg"
URL2 = "https://cdn1.epicgames.com/d5241c76f178492ea1540fce45616757/offer/EGS_HolidaySale2020_DoG_21_1920x1080_Teaser-1920x1080-dae036b682dfe04fc8dcde8ffb3fa0c3.jpg"


class taskThread(QtCore.QObject):
    running = False
    threadSignal = QtCore.pyqtSignal(int)
    threadFinish = QtCore.pyqtSignal()

    # метод, который будет выполнять алгоритм в другом потоке
    def save_settings(self):
        radiobuttons = [self.ui_s.btn_edge, self.ui_s.btn_chrome, self.ui_s.btn_yandex, self.ui_s.btn_firefox]
        for btn in radiobuttons:
            if btn.isChecked():
                browser = btn.text().lower().split(" ")[-1]
                settings.update_setting("settings", "browser", "edge")
                break
        print(self.ui_s.startup.isChecked())
        if self.ui_s.startup.isChecked():
            settings.update_setting("settings", "startup", "True")
        else:
            settings.update_setting("settings", "startup", "False")



class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.start()
        self.set()

        self.manager1 = QNetworkAccessManager()
        self.manager2 = QNetworkAccessManager()
        self.manager1.finished.connect(self.now_image)
        self.manager2.finished.connect(self.next_image)
        self.load_images()

    def start(self):
        self.ui = uic.loadUi("main.ui")
        self.ui_s = uic.loadUi("settings.ui")
        self.ui.show()

    def set(self):
        # main.ui
        #   buttons
        self.ui.btn_auth.clicked.connect(lambda: self.click())
        self.ui.btn_settings.clicked.connect(lambda: self.show_settings())
        self.ui.btn_get_game.clicked.connect(lambda: self.click())
        self.ui.btn_check.clicked.connect(lambda: self.click())

        # settings.ui
        self.ui_s.pushButton.clicked.connect(lambda: self.close_settings())

    def click(self):
        print("AGA")

    def show_settings(self):
        self.ui_s.btn_edge.setChecked(True)
        self.ui_s.startup.setChecked(True)
        self.ui_s.show()

    def save_settings(self):
        radiobuttons = [self.ui_s.btn_edge, self.ui_s.btn_chrome, self.ui_s.btn_yandex, self.ui_s.btn_firefox]
        for btn in radiobuttons:
            if btn.isChecked():
                browser = btn.text().lower().split(" ")[-1]
                settings.update_setting("settings", "browser", "edge")
                break
        print(self.ui_s.startup.isChecked())
        if self.ui_s.startup.isChecked():
            settings.update_setting("settings", "startup", "True")
        else:
            settings.update_setting("settings", "startup", "False")


    def close_settings(self):
        # self.save_settings()
        self.ui_s.close()

    def get_settings(self):
        print(self.ui_s.QradioButton.text())

    # Todo: Удалить и сделать нормально
    # -------------------------------------------------
    def load_images(self):
        self.start_request_now_image()
        self.start_request_next_image()

    def start_request_now_image(self, url=URL1):
        request = QNetworkRequest(QUrl(url))
        self.manager1.get(request)

    def start_request_next_image(self, url=URL2):
        request = QNetworkRequest(QUrl(url))
        self.manager2.get(request)

    @pyqtSlot(QNetworkReply)
    def now_image(self, reply):
        target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
        if reply.error():
            print("error: {}".format(reply.errorString()))
            return
        elif target:
            newUrl = reply.url().resolved(target)
            self.start_request_now_image(newUrl)
            return
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())
        self.ui.now.setScaledContents(True)
        self.ui.now.setPixmap(pixmap)

    @pyqtSlot(QNetworkReply)
    def next_image(self, reply):
        target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
        if reply.error():
            print("error: {}".format(reply.errorString()))
            return
        elif target:
            newUrl = reply.url().resolved(target)
            self.start_request_next_image(newUrl)
            return
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())
        self.ui.next.setScaledContents(True)
        self.ui.next.setPixmap(pixmap)
    # -------------------------------------------------


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()
