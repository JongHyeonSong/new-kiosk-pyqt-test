import sys
import cv2
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QTextEdit


class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage, float)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.running = True

    def run(self):
        start_time = time.time()
        frame_count = 0
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to RGB format
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # Calculate FPS
                frame_count += 1
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time if elapsed_time > 0 else 0

                self.change_pixmap_signal.emit(qt_image, fps)
    
    def stop(self):
        self.running = False
        self.wait()  # Wait for the thread to finish
        self.cap.release()


class CameraFeedWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the label to show the camera feed
        self.camera_label = QLabel(self)
        self.camera_label.setFixedHeight(300)  # Half of the window height

        # Create a label to show the FPS
        self.fps_label = QLabel(self)

        # Create a QTimer to update the camera feed
        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.start()

        # Create buttons and response display area
        self.button1 = QPushButton('Send to hi.com/button1')
        self.button2 = QPushButton('Send to hi.com/button2')
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)

        # Connect buttons to functions
        self.button1.clicked.connect(self.send_request_1)
        self.button2.clicked.connect(self.send_request_2)

        # Set up the layout
        camera_layout = QVBoxLayout()
        camera_layout.addWidget(self.camera_label)
        camera_layout.addWidget(self.fps_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        response_layout = QVBoxLayout()
        response_layout.addLayout(button_layout)
        response_layout.addWidget(self.response_display)

        main_layout = QVBoxLayout()
        main_layout.addLayout(camera_layout)
        main_layout.addLayout(response_layout)

        self.setLayout(main_layout)

    def update_image(self, qt_image, fps):
        # Update the QLabel with the new image
        scaled_image = qt_image.scaled(self.camera_label.size(), Qt.KeepAspectRatio)
        self.camera_label.setPixmap(QPixmap.fromImage(scaled_image))
        # Update the FPS label
        self.fps_label.setText(f"FPS: {fps:.2f}")

    def send_request_1(self):
        self.send_request("http://hi.com/button1")

    def send_request_2(self):
        self.send_request("http://hi.com/button2")

    def send_request(self, url):
        try:
            response = requests.get(url)
            self.response_display.setText(f"Response from {url}:\n{response.text}")
        except Exception as e:
            self.response_display.setText(f"Error: {str(e)}")

    def closeEvent(self, event):
        # Stop the camera thread when the widget is closed
        self.camera_thread.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CameraFeedWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())
