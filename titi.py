import sys
import cv2
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Camera and API Call')
        self.setGeometry(100, 100, 640, 780)

        layout = QVBoxLayout()

        # Camera feed label
        self.camera_label = QLabel(self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label)

        # API call button
        self.api_button = QPushButton('Make API Call', self)
        self.api_button.clicked.connect(self.make_api_call)
        layout.addWidget(self.api_button)

        # API result label
        self.api_label = QLabel(self)
        self.api_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.api_label)

        self.setLayout(layout)

        # Initialize camera
        self.cap = cv2.VideoCapture(0)

        # Set up timer for camera feed update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.camera_label.setPixmap(pixmap.scaled(640, 480, Qt.KeepAspectRatio))

    def make_api_call(self):
        self.api_label.setText("Making API call...")
        try:
            response = requests.get('http://sjhtest.musicen.com/ping/delay/1')  # Replace with your API endpoint
            if response.status_code == 200:
                data = response.json()
                self.api_label.setText(f"API Result: {data}")
            else:
                self.api_label.setText(f"API Error: Status code {response.status_code}")
        except Exception as e:
            self.api_label.setText(f"API Error: {str(e)}")

    def closeEvent(self, event):
        self.cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    ex.show()
    sys.exit(app.exec_())