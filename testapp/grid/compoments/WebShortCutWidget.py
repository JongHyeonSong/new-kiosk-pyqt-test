import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os

class WebShortCutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        icon1 = os.path.join(os.getcwd(), 'testapp', 'grid', 'resources','bt_call.png')  # Update with the correct path to img1
        icon2 = os.path.join(os.getcwd(), 'testapp', 'grid', 'resources','bt_call_hover.png')  # Update with the correct path to img1

        # icon1 = os.path.normpath(icon1)
        print(os.path.normpath(icon1))

        # pixmap = QPixmap(icon1) # QPixmap 생성
        # pixmap = pixmap.scaled(100, 100, Qt.IgnoreAspectRatio) # 이미지 크기 변경

        
        # icon = QIcon() # QIcon 생성
        # icon.addPixmap(pixmap) #아이콘에 이미지 설정

        button2 = QPushButton("")
        button2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # # button2.setStyleSheet("border: none;")

        # button2.setIcon(icon)
        # button2.setIconSize(QSize(100, 100)) #Pushbutton의 아이콘 크기 설정
        # button2.setStyleSheet("background-color: red")

        str = f"background-image: url('{icon1}'); background-repeat: no-repeat; background-position: center center;"
        print(str)
        # button2.setStyleSheet("background-image: url('C:\Users\user\Desktop\project\company\new-kiosk-project\new-kiosk-pyqt-test\testapp\grid\resources\bt_call.png'); background-repeat: no-repeat; background-position: center center;")
        # button2.setStyleSheet('background-image: url("./testapp/grid/img.png"); background-repeat: no-repeat; background-position: center center;')
        button2.setContentsMargins(0, 0, 0, 0)

        image_path1 = os.path.join(os.getcwd(), 'testapp', 'grid', 'bt_weather.png')
        # button1.setIcon(QIcon(image_path1))

        # layout.setAlignment(Qt.AlignTop)
        # layout.setDirection(QHBoxLayout.RightToLeft)
        # layout.setGeometry(QRect(0, 0, 100, 100))

        layout.addWidget(button2)
        layout.addWidget(QPushButton("hello"))
        layout.addWidget(QPushButton("hello"))
        # layout.addWidget(QPushButton("hello"))

        layout.setContentsMargins(0, 0, 0, 0)

        self.icon11 = icon1.replace("\\", "/")
        self.icon22 = icon2.replace("\\", "/")

        self.widget = QLabel()
        self.widget.setPixmap(QPixmap(self.icon11))
        # self.widget.setScaledContents(True)
        # self.setCentralWidget(self.widget)
        self.origin_photo = True  # 추가
        # self.widget.mousePressEvent = self.photo_toggle  # 
        
        self.widget.setScaledContents(True)
        self.widget.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.widget)

        self.widget.mousePressEvent = lambda event: self.widget.setPixmap(QPixmap(self.icon22))  # 추가
        self.widget.mouseReleaseEvent = lambda event: self.widget.setPixmap(QPixmap(self.icon11))  # 추가
        # self.widget.mouseReleaseEvent = self.photo_toggle2  # addition

    def photo_toggle(self, event):  # 추가
        print(event)
        # return
        if self.origin_photo:
            self.widget.setPixmap(QPixmap(self.icon11))
            self.origin_photo = False
        else:
            self.widget.setPixmap(QPixmap(self.icon22))
            self.origin_photo = True

class IconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.setStyleSheet("QPushButton { border: none; }")


# print(QSizePolicy.Fixed) #0
# print(QSizePolicy.Minimum) #1
# print(QSizePolicy.Maximum) #4
# print(QSizePolicy.Preferred) #5
# print(QSizePolicy.MinimumExpanding) #3
# print(QSizePolicy.Expanding) #7
# print(QSizePolicy.Ignored) #13