import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import requests

class RequestThread(QThread):
    request_complete = pyqtSignal(str)

    def run(self):
        try:
            response = requests.get('http://sjhtest.musicen.com/ping/delay/5')
            result = f"Status Code: {response.status_code}\n\nResponse:\n{response.text}"
        except requests.RequestException as e:
            result = f"Error: {str(e)}"
        self.request_complete.emit(result)

class RequestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = QPushButton('Send Request')
        self.button.clicked.connect(self.send_request)
        layout.addWidget(self.button)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle('POST Request to hello.com')
        self.setGeometry(300, 300, 300, 200)

    def send_request(self):
        self.button.setEnabled(False)
        self.result_display.setText("Sending request...")
        self.thread = RequestThread()
        self.thread.request_complete.connect(self.handle_response)
        self.thread.start()

    def handle_response(self, result):
        self.result_display.setText(result)
        print(result)  # This will print the result to the console as well
        self.button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RequestWindow()
    window.show()
    sys.exit(app.exec_())