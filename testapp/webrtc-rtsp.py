import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap

class RTSPPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        print("GOGOGOOG")
        
        self.setWindowTitle("RTSP Stream Player")
        self.setGeometry(100, 100, 800, 600)

        # Create a QLabel to display the video frames
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(800, 600)

        # Create a layout and add the video label to it
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)

        # Create a container widget and set its layout
        container = QWidget()
        container.setLayout(layout)

        # Set the container as the central widget of the main window
        self.setCentralWidget(container)

        # Open the RTSP stream using OpenCV
        self.cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv002.stream")

        # Set up a QTimer to call the update_frame method periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update every 20 ms (50 FPS)

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to QImage format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # Display the frame in the QLabel
                self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        # Release the video capture when the window is closed
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = RTSPPlayer()
    player.show()
    sys.exit(app.exec_())


# import cv2
# cap = cv2.VideoCapture("rtsp://localhost:8554/mystream")

# while(cap.isOpened()):
#     ret, frame = cap.read()
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
