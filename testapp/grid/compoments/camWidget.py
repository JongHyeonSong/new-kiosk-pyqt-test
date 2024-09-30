import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os

from utils.globalSignal import GlobalSignalProxy
class CamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):

        self.setStyleSheet("background-color: #12f2f2;  color: red;")
        


    def hihi(self):
        GlobalSignalProxy().signal.emit(99)
        GlobalSignalProxy().signal.connect(lambda x: print(x))
        print(99)
