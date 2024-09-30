import sys
import asyncio
import aiohttp
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, QObject

class AsyncioThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        self.loop.run_forever()
class AsyncWorker(QObject):
    
    result_signal = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self.thread = AsyncioThread()
        self.thread.start()

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status
                text = await response.text()
                return f"Status: {status}\n\nResponse:\n{text}"

    def send_request(self, url, cb):
        asyncio.run_coroutine_threadsafe(self._send_request(url, cb), self.thread.loop)

    async def _send_request(self, url, cb):
        result = await self.fetch(url)
        print(999, cb)
        cb(1234)
        self.result_signal.emit(url, cb)
async def async_func1():
    print("Hello")
class RequestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = AsyncWorker()
        self.worker.result_signal.connect(self.handle_response)
        self.initUI()

    def cb1(self, data):
        print("11", data)
        
    def cb2(self, data):
        print("22", data)

    def initUI(self):
        layout = QVBoxLayout()

        self.btnA = QPushButton('Send Request to a.com')
        self.btnA.clicked.connect(lambda: self.send_request('http://sjhtest.musicen.com/ping/delay/1', self.cb1))
        layout.addWidget(self.btnA)

        self.btnB = QPushButton('Send Request to b.com')
        self.btnB.clicked.connect(lambda: self.send_request('http://sjhtest.musicen.com/ping/delay/3', self.cb2))
        layout.addWidget(self.btnB)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle('Asyncio Requests')
        self.setGeometry(300, 300, 300, 250)

    def send_request(self, url, cb):
        self.result_display.setText(f"Sending request to {url}...")
        self.worker.send_request(url, cb)

    def handle_response(self, url, cb):
        # self.result_display.setText(f"Response from {url}:\n{result}")
        # print(f"Response from {url}:\n{result}")
        cb(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RequestWindow()
    window.show()
    sys.exit(app.exec_())