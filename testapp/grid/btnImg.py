import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class IconButtonApp(QWidget):
    def __init__(self):
        super().__init__()

        self.move(1920*2, 0)
        icon1 = os.path.join(os.getcwd(), 'testapp', 'grid', 'resources','bt_call.png')  # Update with the correct path to img1
        icon2 = os.path.join(os.getcwd(), 'testapp', 'grid', 'resources','bt_call_hover.png')  # Update with the correct path to img2


        pixmap = QPixmap(icon1) # QPixmap 생성
        pixmap = pixmap.scaled(1001, 1001, Qt.IgnoreAspectRatio) # 이미지 크기 변경

        
        icon = QIcon() # QIcon 생성
        icon.addPixmap(pixmap) #아이콘에 이미지 설정


        self.button = QPushButton("", self)
        self.button.setFont(QFont("Helvetica", 20)) #Pushbutton font 설정
        self.button.setIcon(icon) #Pushbutton에 아이콘 설정
        self.button.setIconSize(QSize("100%", 500)) #Pushbutton의 아이콘 크기 설정


        self.button.setStyleSheet("background-color: red")

        layout = QGridLayout()


        self.button.setSizePolicy(1,1)




        layout.addWidget(self.button)

        self.setLayout(layout)

        self.showMaximized()
      
# Main application loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IconButtonApp()
    # window.show()  # Show window in full size
    sys.exit(app.exec_())
