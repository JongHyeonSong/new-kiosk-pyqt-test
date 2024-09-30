
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

import util
from util.globalSignal import GlobalSignalProxy
import widgets
# print(resource_path(""))

class WebLinkLabel(QLabel):
    click_signal = pyqtSignal()

    def __init__(self, img1, img2, parent=None):

        self.url1 = util.resource_path(img1)
        self.url2 = util.resource_path(img2)

        super().__init__(parent)

        self.setPixmap(QPixmap(self.url1))

        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # 마우스 클릭시 이미지 토글
        self.mousePressEvent = lambda event: self.setPixmap(QPixmap(self.url2))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setPixmap(QPixmap(self.url1))
            self.click_signal.emit()

        # Qlabel 기본 기능을 한다는데 정확히 뭔지는 모르겠음
        super().mouseReleaseEvent(event)



class WebLinkWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        # self.openWebview()

    def initUi(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.link1 = WebLinkLabel(("images/bt_weather.png"), ("images/bt_weather_hover.png"))
        self.link2 = WebLinkLabel(("images/bus_and_subway.png"), ("images/bus_and_subway_hover.png"))
        self.link3 = WebLinkLabel(("images/bt_dust.png"), ("images/bt_dust_hover.png"))
        self.link4 = WebLinkLabel(("images/bt_call.png"), ("images/bt_call_hover.png"))
        # self.link5 = layout.addWidget(WebLinkLabel(util.resource_path("images/bt_call.png"), util.resource_path("images/bt_call_hover.png")))
      
        layout.addWidget(self.link1)
        layout.addWidget(self.link2)
        layout.addWidget(self.link3)
        layout.addWidget(self.link4)

        self.link1.click_signal.connect(lambda: self.openBottomWebview(util.server_url() + "/signagemenu/weather.html?appId=DailySafe_c2f92656ff474a9ea4e2dfb7d738fc93"))
        self.link2.click_signal.connect(lambda: self.openBottomWebview(util.server_url() + "/signagemenu/traffic.html?appId=DailySafe_c2f92656ff474a9ea4e2dfb7d738fc93"))
        self.link3.click_signal.connect(lambda: self.openBottomWebview(util.server_url() + "/signagemenu/dust.html?appId=DailySafe_c2f92656ff474a9ea4e2dfb7d738fc93"))
        
        self.link4.click_signal.connect(lambda: self.openDialogWebView(util.server_url() + "/kiosk/index.html"))
        # self.link4.click_signal.connect(lambda: self.openDialogWebView("http://127.0.0.1:8080/scheme.html"))
    
    def openBottomWebview(self, url):
        GlobalSignalProxy().webLinkSignal.emit(url)

    def openDialogWebView(self, url):
        # self.capture_thread.stop()  # Release the camera
        self.webviewDialog = widgets.WebViewDialog(url)

        # 다이알로그 끝나는 훅 두가지, 하나는 finished 시그널, 하나는 exec_()의 블락킹 메소드
        # self.webview.finished.connect(self.webview_dialog_closed)
        self.webviewDialog.exec_()
        print("웹뷰 다이얼로그 꺼짐")



