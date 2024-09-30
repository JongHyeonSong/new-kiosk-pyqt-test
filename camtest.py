import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class FaceCamViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QLabel to display the webcam feed
        self.image_label = QLabel(self)
        self.image_label.resize(640, 480)

        # Layout to organize the widget
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Create a QTimer to update the feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms (approx. 33 FPS)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame from BGR (OpenCV default) to RGB for Qt
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to QImage
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Display the image in the QLabel
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        # Release the webcam on close
        self.cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceCamViewer()
    window.setWindowTitle("!!F 2 2 2acecam Viewerrr")
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
