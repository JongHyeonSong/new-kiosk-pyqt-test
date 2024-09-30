import PyQt5.QtWidgets
import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

import os



from qt_material import apply_stylesheet

from compoments.WebShortCutWidget import WebShortCutWidget
# from testapp.grid.compoments.WebShortCutWidget import WebShortCutWidget

from compoments.camWidget import CamWidget

class MainWidget(qtw.QWidget):
    WIDTH = 1920
    globalSignal  = qtc.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.initUI()

        # self.show()
        # self.showFullScreen() #
        self.showMaximized()
        # self.loadStyleSheet()


        self.globalSignal.connect(lambda x: print('zzzz global'))

    def initUI(self):
        self.move(self.WIDTH*2, 0)
        self.setWindowTitle('Simple')

        self.layout = qtw.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        label1 = qtw.QLabel("hello world")
        label1.setStyleSheet("border: 1px solid black;")
        # self.layout.addWidget(label1)

        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #123456;  color: red;")

        self.camWidget = qtw.QWidget()
        l1 = qtw.QVBoxLayout()
        # for _ in range(12):
        #     l1.addWidget(qtw.QLabel("hello"))
        
        # self.camWidget.setLayout(l1)
        self.camWidget.setStyleSheet("background-color: #12ccff;  color: red;")


        self.middleLay = qtw.QWidget()
        self.middleLay.setStyleSheet("background-color: #9f34ff;  color: red;")

        self.middleLay.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        second_layout = qtw.QVBoxLayout()
        button = qtw.QPushButton('Full Size Button', self)
        button.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        second_layout.addWidget(button)
        self.middleLay.setLayout(second_layout)

        # second_layout.setContentsMargins(10, 0, 0, 0)

   
        self.videoWidget = qtw.QWidget()
        self.videoWidget.setStyleSheet("background-color: #1234ff;  color: red;")


        scroll_area = qtw.QScrollArea(self)
        scroll_widget = qtw.QWidget()

        m_layout = qtw.QVBoxLayout()


        for _ in range(1000):
            m_layout.addWidget(qtw.QLabel("hello"))



        
        scroll_widget.setLayout(m_layout)
        scroll_area.setWidget(scroll_widget)
        
        self.layout.addWidget(self.camWidget, 4)



        self.webShortCutWidget = WebShortCutWidget()
        self.layout.addWidget(self.webShortCutWidget, 1)




        self.hi = qtw.QWidget()
        self.hi.setStyleSheet("background-color: #929212;  color: red;")



        self.camWidget2 = qtw.QWidget()
        self.camWidget2.setStyleSheet("background-color: #12f2f2;  color: red;")

        # self.layout.addWidget(self.hi, 3)
        self.layout.addWidget(CamWidget(), 3)
        # self.layout.addWidget(self.videoWidget)



        # self.layout.addWidget(scroll_area, 3)


        self.btn1 = qtw.QPushButton("bt1 22", self)


    def loadStyleSheet(self):
        qss_path = os.path.join(os.getcwd(), 'testapp', 'grid','utils', 'file.qss')
        qss_file = qtc.QFile(qss_path)
        qss_file.open(qtc.QFile.ReadOnly | qtc.QFile.Text)
        qss_stream = qtc.QTextStream(qss_file)
        self.setStyleSheet(qss_stream.readAll())
        qss_file.close()
        # dir_path = os.path.dirname(os.path.realpath(__file__))

        # qss_path = os.path.join(self.base_path, 'ressources', 'qss', 'style.qss')
        # qss_path = os.path.join(os.getcwd(), 'testapp', 'grid','utils', 'file.qss')
        
        # with open(qss_path, 'r') as file:
        #     self.setStyleSheet(file.read())        




if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWidget()
    # apply_stylesheet(app, theme='light_pink.xml') # 스타일 적용
    
   
    sys.exit(app.exec_())
