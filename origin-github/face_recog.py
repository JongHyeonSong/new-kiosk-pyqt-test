import threading

import os
import cv2
import random
import argparse
import numpy as np
import imutils
import logging
import time
from typing import Union, List, Tuple
from models import SCRFD, ArcFaceONNX
from utils.helpers import draw_fancy_bbox, compute_similarity
from PIL import Image, ImageDraw, ImageFont
from threading import Timer, Lock
import onnxruntime  # For mask detection

class FaceRecog:
    targets = []
    # colors = {}
    targets_lock = threading.Lock()
    params = None
    
    def __init__(self):
        self.params = self.parse_args()
        self.mask_model = onnxruntime.InferenceSession("impro/models/mask_detector.onnx", None)

        self.detector = SCRFD(self.params.det_weight)
        self.recognizer = ArcFaceONNX(self.params.rec_weight)
        self.__update_targets()

    def parse_args(self):
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

    def update_targets(self ):
        print('update_targets')
        self.__update_targets()
        
    def __update_targets(self):
        with self.targets_lock:
            self.targets = self.__load_targets(self.params.npz_dir)
            self.colors = {
                name: (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                for _, name in self.targets
        }
    def __load_targets(self, npz_dir: str) -> List[Tuple[np.ndarray, str]]:
        targets = []
        for filename in os.listdir(npz_dir):
            if filename.endswith('.npz'):
                data = np.load(os.path.join(npz_dir, filename))
                feature_vector = data['feature_vector']
                name = data['name'].item()
                targets.append((feature_vector, name))
        return targets
    
    def load_npz(self):
        pass

    def __detect_mask(self, face_img):
        if face_img.size == 0:
            return "Unknown"
        face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
        face_img = cv2.resize(face_img, (128, 128))  # Adjust to model's required size
        face_img = face_img.astype(np.float32) / 255.0
        face_img = face_img.reshape(1, 128, 128, 3)  # Adjust to model's required shape
        y_pred = self.mask_model.run(['dense_1'], {'conv2d_input': face_img})
        prediction = np.argmax(y_pred)
        return "O" if prediction == 0 else "X"
        pass


    # 
    """
    Processes a video frame to detect faces and returns a list of dictionaries containing face details.

    Args:
        frame (np.ndarray): A NumPy array representing the image frame to process.
    """
    def face_processor(self, frame:np.ndarray):
        # if(os.getenv("SHOW_WEBCAM") == "Y"):
        #     return result

        # frame = imutils.resize(frame, width=1000)
        bboxes, kpss = self.detector.detect(frame, input_size=(640, 640), thresh=self.params.confidence_thresh, max_num= self.params.max_num)
        result = []
        for bbox, kps in zip(bboxes, kpss):
            x1, y1, x2, y2, score = bbox.astype(np.int32)
            embedding = self.recognizer(frame, kps)
            max_similarity = 0
            best_match_name = None
            for target, name in self.targets:
                similarity = compute_similarity(target, embedding)
                if similarity > max_similarity and similarity > self.params.similarity_thresh:
                    max_similarity = similarity
                    best_match_name = name
            intbox = [x1, y1, x2, y2]
            face_img = frame[y1:y2, x1:x2]
            mask_status = self.__detect_mask(face_img)

            result.append({ "match_id" : best_match_name, "mask_status": mask_status, "rect_pos": intbox})
        return result