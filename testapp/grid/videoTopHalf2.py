import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QSizePolicy

class VideoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.move(1920 *2, 0)

        # Setup the QLabel to display the video frames (no fixed size)
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)  # Center the video
        self.video_label.setStyleSheet("background-color: black;")  # Black background for video

        # 화면을 줄일때 크기가 같이 줄어들게함
        self.video_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Placeholder label for the bottom half (optional)
        self.bottom_label = QLabel("Bottom Section", self)
        self.bottom_label.setAlignment(Qt.AlignCenter)
        # self.bottom_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a layout and add the video label and the bottom label
        layout = QVBoxLayout()
        layout.addWidget(self.video_label,1)  # Top half
        layout.addWidget(self.bottom_label,1)  # Bottom half
        layout.setContentsMargins(0, 0, 0, 0)

        # Set stretch factors: top half (video) gets 1, bottom gets 1
        # layout.setStretch(0, 1)  # Top half
        # layout.setStretch(1, 1)  # Bottom half

        self.setLayout(layout)

        # Create a QTimer to control the frame updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)  # 0 is the default camera

        # Start the timer to get frames at 30 FPS (1000/30 ms interval)
        self.timer.start(33)

    # width든 height든 먼저 맞는쪽에 100% 사이즈맞춤
    def update_frame2(self):
        # Read frame from OpenCV
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape
            aspect_ratio = w / h

            # Get the label size
            label_width = self.video_label.width()
            label_height = self.video_label.height()
            label_aspect_ratio = label_width / label_height

            # Fit the frame to the label while maintaining the aspect ratio
            if aspect_ratio > label_aspect_ratio:
                # Width fits first, scale height to maintain the aspect ratio
                new_width = label_width
                new_height = int(new_width / aspect_ratio)
            else:
                # Height fits first, scale width to maintain the aspect ratio
                new_height = label_height
                new_width = int(new_height * aspect_ratio)

            # Resize the frame to fit within the QLabel
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Convert the frame to QImage and set it to the label
            bytes_per_line = 3 * new_width
            qt_image = QImage(resized_frame.data, new_width, new_height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            self.video_label.setPixmap(pixmap)

    # 무조건 100%, 100% 스트레치
    def update_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()
 
        if ret:
            # Convert the frame from BGR (OpenCV format) to RGB (Qt format)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to fit the video label while maintaining aspect ratio
            label_width = self.video_label.width()
            label_height = self.video_label.height()
            resized_frame = cv2.resize(rgb_frame, (label_width, label_height), interpolation=cv2.INTER_AREA)

            # Get image height, width, and number of channels
            height, width, channel = resized_frame.shape

            # Create QImage from the resized frame
            qimg = QImage(resized_frame.data, width, height, 3 * width, QImage.Format_RGB888)

            # Convert QImage to QPixmap and set it in the QLabel
            self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def update_frame_origin(self):
        ret, frame = self.cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qt_image = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        # Release the camera when the widget is closed
        self.cap.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the VideoWidget
    video_widget = VideoWidget()
    video_widget.show()

    # Run the application loop
    sys.exit(app.exec_())
