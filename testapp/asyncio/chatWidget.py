import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socketio
from managers import *
from PyQt5.QtCore import pyqtSignal, QObject

class ChatWidget(QWidget):

    lins = []
    def __init__(self):
        super().__init__()
        self.initUI()

        self.th = Thr()

        self.th.message_received.connect(self.wow)

        self.th.start()

        print("(((())))")
        
        
        
        # self.sio = socketio.Client()
        # self.sio.connect('http://localhost:3300')

        # self.webSocketManager = WebSocketManager()
        # self.webSocketManager.hook.connect(self.wow)
        # self.sio.on("message", self.wow)

        # self.result_signal.connect
        # self.sig = pyqtSignal()
        # self.sig.connect(lambda x:print('hihi'))
        # pyqtSignal().connect

        # @self.sio.event
        # def message(data):
        #     print('I received a message!')
        #     # self.sig.emit('goso')
        #     # print(self.drawEdit())

    def wow(self, data):
        print("??")
        print(data)
        self.lins.append(data)

        self.drawEdit()
        
    def initUI(self):
        # self.wsManager = WebSocketManager()

        self.move(1920 *2, 0)
        self.resize(500,500)
        self.setWindowTitle('Asyncio')

        # make input
        self.input = QLineEdit(self, placeholderText="input")
        # set input initial vlaue
        self.input.setText('test')

        # make big input to add many line
        self.inputs = QTextEdit(self)
        
        self.btn2 = QPushButton('query 222', self)
        self.btn2.clicked.connect(self.inputClick)

        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.btn2)
        layout.addWidget(self.inputs)

        self.setLayout(layout)



    def inputClick(self):
        inputTxt = self.input.text()

        self.th.sio.emit('message', inputTxt)

        # self.wsManager.ggg("abc", lambda x:print(x))

        # self.drawEdit()

    def drawEdit(self):
        # self.inputs.append(txt)
        # self.input.clear()
        self.inputs.clear()

        # itera all lines and add to edit using lanbda

        for line in self.lins:
            # print('zz',line)
            self.inputs.append(line)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatWidget()
    ex.show()
    sys.exit(app.exec_())