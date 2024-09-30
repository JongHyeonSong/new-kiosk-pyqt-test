import sys

from PyQt5.QtWidgets import *

class WebLinkImageComponent(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: pink;")
        self.setFixedSize(100, 100)
        self.setText("WebLinkImage")

