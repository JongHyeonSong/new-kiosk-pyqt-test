import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from components.webEngineComponent import WebEngineComponent

class WebViewDialog(QDialog):
    def __init__(self, url):
        super().__init__()
        self.url = url

        self.setWindowTitle("WebView")

        self.move(1920*2, 0)
        self.resize(1080, 1920)

        self.initUi()

        # 반드시 ui세팅하고 나서 실행해야 함
        self.showFullScreen()


    def initUi(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


        self.webEngineView = WebEngineComponent(self.url)
        # QWebEnginePage 객체가 navigation 훅을 감지해서 여기서 달아야함..
        self.webEngineView.webPage.customUrlSignal.connect(lambda: self.close())
        layout.addWidget(self.webEngineView)

        # layout.addWidget(self.getWebview(self.url))
        # layout.addWidget(self.getWebview("https://www.naver.com"))

        # 우상단 끄기 버튼 추가
        floatingCloseBtn = QPushButton("close", self)
        floatingCloseBtn.move(100, 100)
        floatingCloseBtn.clicked.connect(lambda evt: self.showFullScreen())
        floatingCloseBtn.move(self.width() - floatingCloseBtn.width() - 10, 10)
        floatingCloseBtn.clicked.connect(self.handleFloatingCloseBtn)
        
    def handleFloatingCloseBtn(self):
        # 웹엔진을 끄고, Dialog 닫기
        self.webEngineView.close()
        self.close()
    
    def handleConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"Console: {message} (line: {lineNumber}, source: {sourceID})")
