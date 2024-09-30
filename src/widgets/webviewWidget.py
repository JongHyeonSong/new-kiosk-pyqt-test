import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

import components
from util.globalSignal import GlobalSignalProxy

class WebviewWidget(QWidget):
    closeBtnSignal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webview")
        self.initUi()

        GlobalSignalProxy().webLinkSignal.connect(lambda url: self.webEngineComponent.replaceUrl(url))

        # test용
        self.styleSheet = "background-color: pink;"
        self.setAttribute(Qt.WA_StyledBackground, True)

    def initUi(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


        self.webEngineComponent = components.WebEngineComponent()
        layout.addWidget(self.webEngineComponent)

        # 우상단 닫기 버튼
        self.floatingCloseBtn = QPushButton("닫!기!", self)
        self.floatingCloseBtn.setStyleSheet("background-color: red; color: white;")
        self.floatingCloseBtn.clicked.connect(self.handleFloatingCloseBtn)
        # css로 한방에 안되나봄 리사이즈마다 계산해서 입력
        self.resizeEvent = lambda evt: self.setPositionFloatCloseBtn()

    def setPositionFloatCloseBtn(self):
        leftPosition = self.width() - self.floatingCloseBtn.width() - 10
        self.floatingCloseBtn.move(leftPosition, 10)

    def handleFloatingCloseBtn(self):
        self.closeBtnSignal.emit()
    
    def releaseWebview(self):
        pass
        # self.close()
        
