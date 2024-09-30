

import sys
import os

sys.path.append(os.path.join(os.getcwd()))

import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import time


import sys
import cv2
import random
import argparse
import numpy as np
import imutils
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from typing import List, Tuple

from impro.models import SCRFD, ArcFaceONNX
from impro.utils.helpers import draw_fancy_bbox, compute_similarity
from PIL import Image, ImageDraw, ImageFont
from threading import Timer, Lock
import onnxruntime  # For mask detection


# Global variables and locks
targets = []
colors = {}
targets_lock = Lock()

# Load mask detection model
mask_model = onnxruntime.InferenceSession("impro/models/mask_detector.onnx", None)
print('gogo',mask_model)

def parse_args():
    parser = argparse.ArgumentParser(description="Face Detection-and-Recognition with Mask Detection")
    parser.add_argument("--det-weight", type=str, default="impro/weights/det_10g.onnx", help="Path to detection model")
    parser.add_argument("--rec-weight", type=str, default="impro/weights/w600k_r50.onnx", help="Path to recognition model")
    parser.add_argument("--similarity-thresh", type=float, default=0.4, help="Similarity threshold between faces")
    parser.add_argument("--confidence-thresh", type=float, default=0.5, help="Confidence threshold for face detection")
    parser.add_argument("--npz-dir", type=str, default="impro/npz_files", help="Path to npz files directory")
    parser.add_argument("--source", type=str, default="0", help="Video file or video camera source. i.e 0 - webcam")
    parser.add_argument("--max-num", type=int, default=10, help="Maximum number of face detections from a frame")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    return parser.parse_args()

def setup_logging(level: str) -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), None), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def load_targets(npz_dir: str) -> List[Tuple[np.ndarray, str]]:
    targets = []
    for filename in os.listdir(npz_dir):
        if filename.endswith('.npz'):
            data = np.load(os.path.join(npz_dir, filename))
            feature_vector = data['feature_vector']
            name = data['name'].item()
            targets.append((feature_vector, name))
    return targets

def draw_text(image, text, position, font_path='impro/NanumGothicBold.ttf', font_size=20, color=(255, 0, 0)):
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    return np.array(img_pil)

def draw_corner_lines(im, intbox, color):
    cv2.line(im, (intbox[0], intbox[1]), (intbox[0], intbox[1]+10), color, 2)
    cv2.line(im, (intbox[0], intbox[1]), (intbox[0]+10, intbox[1]), color, 2)
    cv2.line(im, (intbox[2], intbox[1]), (intbox[2], intbox[1]+10), color, 2)
    cv2.line(im, (intbox[2], intbox[1]), (intbox[2]-10, intbox[1]), color, 2)
    cv2.line(im, (intbox[0], intbox[3]), (intbox[0], intbox[3]-10), color, 2)
    cv2.line(im, (intbox[0], intbox[3]), (intbox[0]+10, intbox[3]), color, 2)
    cv2.line(im, (intbox[2], intbox[3]), (intbox[2], intbox[3]-10), color, 2)
    cv2.line(im, (intbox[2], intbox[3]), (intbox[2]-10, intbox[3]), color, 2)

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10
    return 1

def detect_mask(face_img):
    if face_img.size == 0:
        return "Unknown"
    face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
    face_img = cv2.resize(face_img, (128, 128))  # Adjust to model's required size
    face_img = face_img.astype(np.float32) / 255.0
    face_img = face_img.reshape(1, 128, 128, 3)  # Adjust to model's required shape
    y_pred = mask_model.run(['dense_1'], {'conv2d_input': face_img})
    prediction = np.argmax(y_pred)
    return "O" if prediction == 0 else "X"

def frame_processor(frame: np.ndarray, detector, recognizer, params) -> np.ndarray:
    # frame = imutils.resize(frame, width=1000)  # Resize frame
    bboxes, kpss = detector.detect(frame, input_size=(640, 640), thresh=params.confidence_thresh, max_num=params.max_num)
    global targets, colors
    with targets_lock:
        for bbox, kps in zip(bboxes, kpss):
            x1, y1, x2, y2, score = bbox.astype(np.int32)
            embedding = recognizer(frame, kps)
            max_similarity = 0
            best_match_name = "Unknown"
            for target, name in targets:
                similarity = compute_similarity(target, embedding)
                if similarity > max_similarity and similarity > params.similarity_thresh:
                    max_similarity = similarity
                    best_match_name = name
            intbox = [x1, y1, x2, y2]
            face_img = frame[y1:y2, x1:x2]
            mask_status = detect_mask(face_img)
            if best_match_name != "Unknown":
                color = colors.get(best_match_name, (255, 0, 0))
                text = f"{best_match_name} ({mask_status})"
                frame = draw_text(frame, text, (x1, y1-30), color=color)
                draw_corner_lines(frame, intbox, color)
            else:
                name = '방문자'
                text = f"{name} ({mask_status})"
                frame = draw_text(frame, text, (x1, y1-30), color=(255, 0, 0))
                draw_corner_lines(frame, intbox, (255, 0, 0))
    return frame

def update_targets(npz_dir: str) -> None:
    global targets, colors
    with targets_lock:
        targets = load_targets(npz_dir)
        colors = {
            name: (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
            for _, name in targets
        }


class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage, float)

    targets = []
    colors = {}
    detector = None
    recognizer = None

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.running = True

        params = parse_args()
        self.params = params
        print("args")
        print(params)
        self.detector = SCRFD(params.det_weight)
        self.recognizer = ArcFaceONNX(params.rec_weight)

        self.targets = load_targets(params.npz_dir)
        print(len(self.targets))
        self.colors = {
            name: (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
            for _, name in targets
        }


    def run(self):
        start_time = time.time()
        frame_count = 0
        while self.running:
            ret, frame = self.cap.read()
            if ret:

                frame = frame_processor(frame=frame, detector=self.detector, recognizer=self.recognizer, params=self.params)

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


class VideoLabel(QWidget):

    def update_image(self, qt_image, fps):
        # Update the QLabel with the new image
        scaled_image = qt_image.scaled(self.camera_label.size(), Qt.IgnoreAspectRatio) # Qt.IgnoreAspectRatio - 비율무시100/100 Qt.KeepAspectRatio
        self.camera_label.setPixmap(QPixmap.fromImage(scaled_image))
        # Update the FPS label
        self.fps_label.setText(f"FPS: {fps:.2f}")

    def face_recog_init(self):
        print("WEFzzz !!")
        # args = parse_args()
        
    def __init__(self, parent=None):
        super().__init__(parent)

        self.face_recog_init()

        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.start()


        # Create a QLabel to display the video
        self.camera_label = QLabel(self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: white;")
        self.camera_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) # 윈도우 사이즈를 줄일때 카메라부분이 같이 줄어들게함

        # Create a layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


        # 플로팅 UI들 세팅(레이아웃 세팅후에 세팅)
        self.fps_label = QLabel(self)
        # self.fps_label.move(10,10)
        self.fps_label.setText(f"FPS: ")

        self.fps_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 128);
            color: white;
            padding: 5px;
            border-radius: 5px;
        """)


class VideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.move(1920 *2, 0)

        # video
        self.video_label = VideoLabel(self)

        self.bottom_label = QLabel("Bottom Section", self)
        self.bottom_label.setAlignment(Qt.AlignCenter)


        layout = QVBoxLayout()
        layout.addWidget(self.video_label,1)  # Top half
        layout.addWidget(self.bottom_label,1)  # Bottom half
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


    def __aainit__(self):
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
