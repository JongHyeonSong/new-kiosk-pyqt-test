
import sys
import cv2
import os
import time
import random
import argparse
import numpy as np
import imutils
import logging
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from threading import Timer, Lock
import onnxruntime  # For mask detection
import debugpy

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

sys.path.append(os.path.join(os.getcwd(), "impro"))
from face_recog import FaceRecog


class WebcamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # if os DISALBE_WEBCAM is true
        # if(os.getenv("SHOW_WEBCAM") == "Y"):
        #     self.initUi()
        # else:
        # self.testUi()

        self.initUi()


    def initUi(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # layout = QVBoxLayout()
        # layout.setContentsMargins(0,0,0,0)
        # self.setLayout(layout)
        # layout.addWidget(QPushButton("test", self))


        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.start()

        # Create a QLabel to display the video
        self.cameraSnapshotLabel = QLabel(self)
        self.cameraSnapshotLabel.setAlignment(Qt.AlignCenter)
        self.cameraSnapshotLabel.setStyleSheet("background-color: white;")
        self.cameraSnapshotLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) # 윈도우 사이즈를 줄일때 카메라부분이 같이 줄어들게함

        layout.addWidget(self.cameraSnapshotLabel)

        # 플로팅 UI들 세팅(레이아웃 세팅후에 세팅 해야 공중에뜸)
        self.fps_label = QLabel(self)
        # self.fps_label.move(10,10)
        self.fps_label.setText(f"FPS: ")

        self.fps_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 128);
            color: white;
            padding: 5px;
            border-radius: 5px;
        """)

    def testUi(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        layout.addWidget(QPushButton("test", self))
    
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #ac3ccc;')


    def update_image(self, qt_image, fps):
        # Update the QLabel with the new image
        scaled_image = qt_image.scaled(self.cameraSnapshotLabel.size(), Qt.IgnoreAspectRatio) # Qt.IgnoreAspectRatio - 비율무시100/100 Qt.KeepAspectRatio
        self.cameraSnapshotLabel.setPixmap(QPixmap.fromImage(scaled_image))
        # Update the FPS label
        self.fps_label.setText(f"FPS: {fps:.2f}")

    def face_recog_init(self):
        print("WEFzzz !!")
        # args = parse_args()
        
    def videolabel_reload(self):
        print('videolabel_reload')
        self.camera_thread.reload()


class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage, float)

    targets = []
    colors = {}
    detector = None
    recognizer = None

    def reload(self):
        print('reload')

        self.face_recog.update_targets()

    def __init__(self):
        super().__init__()

        # self.faceRecog = FaceRecog()

        self.cap = cv2.VideoCapture(0)
        self.running = True

        self.face_recog = FaceRecog()

    def draw_text(self, image, text, position, font_path='impro/NanumGothicBold.ttf', font_size=20, color=(255, 0, 0)):
        img_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill=color)
        return np.array(img_pil)

    def run(self):
        # debugpy.debug_this_thread()
        
        start_time = time.time()
        frame_count = 0
        while self.running:
            ret, frame = self.cap.read()
            print(frame)
            if ret:
                # re = self.face_recog.face_processor(frame)
                # print(re)
                # for user in re:
                #     pos = user.get("rect_pos")
                #     if(user.get("match_id") is not None):
                #         frame = self.draw_text(frame, user.get('mask_status') + ' hi ' + user.get('match_id'), (pos[0], pos[1]), color=(255,0,0))
                #     else:
                #         frame = self.draw_text(frame, user.get('mask_status') + ' hi ' + "NONO", (pos[0], pos[1]), color=(255,0,0))

                #     pass

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
