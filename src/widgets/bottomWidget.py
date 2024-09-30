import sys
import os

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import util

import shutil

from widgets.mediaWidget import MediaWidget
from widgets.webviewWidget import WebviewWidget

from util.globalSignal import GlobalSignalProxy
# from components.webEngineView import WebEngineView
# from widgets import WebviewWidget
# from widgets import Abc


class BottomWidget(QWidget):

    def testUi(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: red;')

    def initUi(self):
        # listen S key
        # self.shortcut_s = QShortcut(QKeySequence("S"), self)
        # self.shortcut_s.activated.connect(self.changeToNextStack)

        # 웹링크 클릭시 스택을 웹뷰(1번) 으로 변경
        GlobalSignalProxy().webLinkSignal.connect(lambda url: self.changeStack(1))
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create bottom half with stacked widget
        self.stack = QStackedWidget()

        self.webviewWidget = WebviewWidget()
        self.webviewWidget.closeBtnSignal.connect(lambda: self.changeStack(0))

        self.stack.addWidget(MediaWidget())
        self.stack.addWidget(self.webviewWidget)

        layout.addWidget(self.stack)

    def changeStack(self, index):
        self.stack.setCurrentIndex(index)
        
    def changeToNextStack(self):
        # if index over then set to 0
        self.stack.setCurrentIndex((self.stack.currentIndex() + 1) % self.stack.count())
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        # self.testUi()

        # self.stack.setCurrentIndex(1)
