
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from widgets import WebcamWidget
from widgets import WebLinkWidget
from widgets import BottomWidget

from dotenv import load_dotenv
# load .env
load_dotenv()
# print(os.environ.get('MODE'))


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebView and MP4 Player")
        self.initUI()


    def initUI(self):
        self.move(1920*2, 0)
        # self.move(0, 0)
        self.showMaximized()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #123456;  color: red;")

        self.layout.addWidget(WebcamWidget(), 4)
        self.layout.addWidget(WebLinkWidget(), 1)
        self.layout.addWidget(BottomWidget(), 3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())