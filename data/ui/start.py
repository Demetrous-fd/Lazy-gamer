#!/urs/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot, QUrl, QObject, pyqtSignal, QThread
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
import settings
import sys


URL1 = "https://cdn1.epicgames.com/d5241c76f178492ea1540fce45616757/offer/EGS_HolidaySale2020_DoG_AlienIsolation_1920x1080_Teaser-R-1920x1080-2d7e1be9cc7c6583832158bc4214c981.jpg"
URL2 = "https://cdn1.epicgames.com/d5241c76f178492ea1540fce45616757/offer/EGS_HolidaySale2020_DoG_21_1920x1080_Teaser-1920x1080-dae036b682dfe04fc8dcde8ffb3fa0c3.jpg"


@pyqtSlot()
def run_on_complete():
    pass


class WorkThread(QThread):

    def __init__(self, ui_s, func):
        super().__init__()
        self.ui_s = ui_s
        self.func = func

    def run(self):
        self.func()



class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = uic.loadUi("main.ui")
        self.ui.show()

        self.ui_s = uic.loadUi("settings.ui")
        self.set()

        self.manager1 = QNetworkAccessManager()
        self.manager2 = QNetworkAccessManager()
        self.manager1.finished.connect(self.now_image)
        self.manager2.finished.connect(self.next_image)
        self.load_images()

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

    def settings_task(self, func):
        self.thread = WorkThread(self.ui_s, func)
        self.thread.start()

    def show_settings(self):
        self.settings_task(self.load_settings)
        self.ui_s.show()

    def close_settings(self):
        self.settings_task(self.save_settings)
        self.ui_s.close()

    def save_settings(self):
        radiobuttons = [self.ui_s.btn_edge, self.ui_s.btn_chrome]
        for btn in radiobuttons:
            if btn.isChecked():
                browser = btn.text().lower().split(" ")[-1]
                settings.update_setting("Settings", "browser", browser)
                break
        if self.ui_s.startup.isChecked():
            settings.update_setting("Settings", "startup", "True")
        else:
            settings.update_setting("Settings", "startup", "False")

    def load_settings(self):
        if settings.get_setting("Settings", "browser") == "chrome":
            self.ui_s.btn_chrome.setChecked(True)
        else:
            self.ui_s.btn_edge.setChecked(True)
        if settings.get_setting("Settings", "startup") == "True":
            self.ui_s.startup.setChecked(True)

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
