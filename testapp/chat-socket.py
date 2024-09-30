import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import socketio

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

        # self.sc = SocketClient(self)

        self.sc.chatSignal.connect(self.from_QThread)

        self.btn1.clicked.connect(self.send_msg)
        self.btn2.clicked.connect(self.soct_connect)
    def from_QThread(self,msg):
        self.addwer('[남] %s'%msg)

    def send_msg(self):

        print("SENDING???")
        curr_msg = self.type.text()
        self.sc.send_msg("GOGO -sing"+curr_msg)
        a=3


    # @pyqtSignal(str)
    def addwer(self,msg):
        self.result_display.append(msg)
    
    def soct_connect(self):
        print(self.sc.is_run)

        if(not self.sc.is_run):
            self.sc.start(1)
        print("SOCK!!")

    def initUi(self):
        layout = QVBoxLayout()
        
        topLayout = QHBoxLayout()
        layout.addLayout(topLayout, 3)


        self.textbox = QTextBrowser()

        topLayout.setContentsMargins(10,10,10,10)

        self.btn1 = QPushButton('btn1')
        self.btn2 = QPushButton('btn2')
        topLayout.addWidget(self.btn1)
        topLayout.addWidget(self.btn2)

        self.button = QPushButton('Send Request')
        layout.addWidget(self.button)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # self.type = QTextEdit()
        self.type = QLineEdit()
        self.type.returnPressed.connect(self.send_request)
        self.type.setMaximumSize(500,100)

        self.send_btn = QPushButton('Send')
        layout.addWidget(self.type)
        layout.addWidget(self.send_btn)

        self.send_btn.clicked.connect(self.send_request)

        self.setLayout(layout)
        self.setWindowTitle('POST Request to hello.com')
        self.setGeometry(300, 300, 300, 200)


        self.move(1920*2, 0)
        self.resize(500,500)
    
    def send_request(self, *li):
        print(li)
        txt = self.type.text()

        # self.result_display.setText("Sending request...")
        # self.result_display.setText('[나] %s'%txt)

        self.addwer('[나] %s'%txt)

        print("SEDED", txt)

    def keyPressEvent(self, e):
        print(e.key())


class SocketClient(QThread):
    chatSignal = pyqtSignal(str)
    # sio = socketio.Client()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.is_run = False

    def run(self):
        self.is_run = True

        # host = "ws://localhost:3300"
        host = 'http://localhost:3300'

        sio = socketio.Client()
        sio.connect('http://localhost:3300')
        sio.wait()
        # SocketClient.sio.on('tester', self.recieve)
        # SocketClient.sio.connect(host)
        # SocketClient.sio.wait()

        print("thread GOGO")

    def recieve(self, msg):
        print("RERE")
        # print("MSG", msg)   
        # # self.parent.addwer(msg)
        # self.chatSignal.emit(msg)
        
    def send_msg(self, msg):
        SocketClient.sio.emit('chat_message', msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())