import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray

class RequestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_response)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.btnA = QPushButton('Send Request to a.com')
        self.btnA.clicked.connect(lambda: self.send_request('http://sjhtest.musicen.com/ping/delay/5'))
        layout.addWidget(self.btnA)

        self.btnB = QPushButton('Send Request to b.com')
        self.btnB.clicked.connect(lambda: self.send_request('http://sjhtest.musicen.com/ping/delay/2'))
        layout.addWidget(self.btnB)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle('POST Requests to a.com and b.com')
        self.setGeometry(300, 300, 300, 250)

    def send_request(self, url):
        sender = self.sender()
        sender.setEnabled(False)
        self.result_display.setText(f"Sending request to {url}...")
        
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)
        # self.network_manager.post(request, QByteArray())

    def handle_response(self, reply):
        url = reply.url().toString()
        if reply.error() == QNetworkReply.NoError:
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            response_text = reply.readAll().data().decode()
            result = f"Response from {url}:\nStatus Code: {status_code}\n\nResponse:\n{response_text}"
        else:
            result = f"Error from {url}: {reply.errorString()}"

        self.result_display.setText(result)
        print(result)  # This will print the result to the console as well
        
        # Re-enable both buttons
        self.btnA.setEnabled(True)
        self.btnB.setEnabled(True)
        
        reply.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RequestWindow()
    window.show()
    sys.exit(app.exec_())